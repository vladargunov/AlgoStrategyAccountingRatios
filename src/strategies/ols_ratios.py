import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

from src.strategies.base_strategy import BaseStrategy
from src.strategies.cfg import OLSCFG

from sklearn.preprocessing import StandardScaler

class OLSRatios(BaseStrategy):
    def __init__(self):
        """
        OLSRatios implements the trading strategy using the regression as
        outlined in the paper "Neural network forecasts of Canadian stock
        returns using accounting ratios", but done in the simplified form.

        Args:
        required_number_dates : specifies the required number of dates needed
        to for each evaluation step

        decision_rule : specifies how the portfolio is formed
        'median' <- all stocks returns which are forecasted above median are
        bought long, and all stocks forecasted below are sold short
        'quartile' <- all stocks are bought from the first quartile,
        and all the stocks sold are from the last quartile, the
        remaining are not entered into the portfolio
        'octile' <- the same strategy as for 'quartile' but using
        the octiles for decision rules

        train_interval : specifies the intervals when the linear
        regression must be trained before being evaluated, otherwise
        the pretrained regression is used

        Comment on data preprocessing: it is all scaled by StandardScaler
        before training and inference
        """
        super().__init__(required_number_dates=OLSCFG.required_number_dates)

        self.decision_rule = OLSCFG.decision_rule
        assert self.decision_rule in ['median', 'quartile', 'octile'], ('Warning,'
                                         'Decision rule is specified incorrectly!')
        self.reg = LinearRegression()

        self.train_interval = True

        self.column_y = 'return'
        self.columns_x = ['outstanding_share', 'turnover', 'pe', 'pe_ttm', 'pb',
                          'ps', 'ps_ttm', 'dv_ratio', 'dv_ttm', 'total_mv', 'qfq_factor']

    def __repr__(self):
        return '_'.join(['OLS', OLSCFG.decision_rule])


    def _prepare_data(self, strategy_data):
        new_df = pd.DataFrame(columns=strategy_data.columns)
        for ticker in strategy_data['ticker'].unique():
            current_df = strategy_data[strategy_data['ticker'] == ticker]
            current_df = current_df.sort_values(by=['date'])
            current_df['next_price'] = current_df['price'].diff().shift(-1)
            current_df['return'] = current_df.apply(lambda x: x['next_price'] / x['price'] - 1, axis=1)
            current_df = current_df.dropna()
            new_df = pd.concat([new_df, current_df])

        train_y = new_df[self.column_y]
        train_x = new_df[self.columns_x]

        # Normalise data
        self.scaler = StandardScaler()
        self.scaler.fit(train_x)

        return train_x, train_y


    def create_portfolio(self, strategy_data, available_tickers) -> dict:
        # If self.train_interval is true, then train the model
        if self.train_interval:
            train_x, train_y = self._prepare_data(strategy_data)
            self.reg.fit(train_x, train_y)
            self.train_interval = False

        # Perform the formation of the portfolio
        latest_date = max(strategy_data['date'].unique())
        latest_data = strategy_data[( strategy_data['date'] == latest_date ) &
                                    ( strategy_data['ticker'].isin(available_tickers) )].dropna()

        pred_x = latest_data[self.columns_x]
        # Normalise the input data
        pred_x = pd.DataFrame(self.scaler.transform(pred_x), columns=self.columns_x)

        pred_tickers = latest_data['ticker']

        preds = self.reg.predict(pred_x)
        preds = pd.DataFrame(preds, index=pred_tickers, columns=['prediction'])

        if self.decision_rule == 'median':
            upper_cutoff = np.median(preds)
            lower_cutoff = np.median(preds)

        elif self.decision_rule == 'quartile':
            upper_cutoff = np.quantile(preds, .75)
            lower_cutoff = np.quantile(preds, .25)

        elif self.decision_rule == 'octile':
            upper_cutoff = np.quantile(preds, .875)
            lower_cutoff = np.quantile(preds, .125)

        preds['prediction'] = [1 if x>upper_cutoff else -1 if x<lower_cutoff else 0 for x in preds['prediction']]

        # Count the values of long and short
        number_long = preds[preds['prediction'] == 1]['prediction'].shape[0]
        number_short = preds[preds['prediction'] == -1]['prediction'].shape[0]

        preds.loc[preds['prediction'] == 1, 'prediction'] = 1 / number_long
        preds.loc[preds['prediction'] == -1, 'prediction'] = -1 / number_short

        return preds.to_dict()['prediction']
