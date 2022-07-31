import argparse

from src.datamodule import DataModule
from src.portfolio import Portfolio
from src.simulator import Simulator

from src.strategies.ols_ratios import OLSRatios
from src.strategies.logit_ratios import LogitRatios
from src.strategies.nn_ratios import NNRatios

from src.strategies.cfg import OLSCFG, LogRegCFG, NNCFG


def main(strategy, frequency, decision_rule, type_model, initial_value,
         max_allocation_long, max_allocation_short, start_date,
         end_date, save_history, risk_free_rate):

    print(f'...{strategy}...')
    dm = DataModule()
    pf = Portfolio(initial_value=initial_value,
                   max_allocation_long=max_allocation_long,
                   max_allocation_short=max_allocation_short)

    if strategy == 'OLSRatios':
        OLSCFG.decision_rule = decision_rule
        sr = OLSRatios()

    elif strategy == 'LogitRatios':
        LogRegCFG.decision_rule = decision_rule
        sr = LogitRatios()

    elif strategy == 'NNRatios':
        NNCFG.decision_rule = decision_rule
        NNCFG.type_model = type_model
        sr = NNRatios()

    sm = Simulator(dm, pf, sr, frequency, start_date, end_date)

    sm.simulate()
    sm.compute_metrics(risk_free_rate=risk_free_rate)

    if save_history:
        sm.save_history()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-s','--strategy', default='OLSRatios', choices=['OLSRatios', 'LogitRatios', 'NNRatios'],
                        type=str, help='Choose a strategy')

    parser.add_argument('-f','--frequency', default='yearly', choices=['daily', 'weekly', 'monthly', 'yearly'],
                        type=str, help='Choose frequency')

    parser.add_argument('-d','--decision_rule', default='median', choices=['median', 'quartile', 'octile'],
                        type=str, help='Choose trading decision rule')

    parser.add_argument('-t','--type_model', default='regression', choices=['regression', 'classification'],
                        type=str, help='Choose model type for NNModel')

    parser.add_argument('--initial_value', default=100, type=int, help='Choose initial value of portfolio')

    parser.add_argument('-max_long','--max_allocation_long', default=100,
                            type=int, help='Choose maximum allocation for long position')

    parser.add_argument('-max_short','--max_allocation_short', default=100,
                            type=int, help='Choose maximum allocation for short position')

    parser.add_argument('-start','--start_date', default='2005-01-04',
                        type=str, help='Choose start date from 2005-01-04 to 2022-05-11')

    parser.add_argument('-end','--end_date', default='2022-05-11',
                        type=str, help='Choose end date from 2005-01-04 to 2022-05-11')

    parser.add_argument('-history', '--save_history', action='store_true')

    parser.add_argument('-rf','--risk_free_rate', default=.01,
                        type=float, help='Choose risk free rate')

    args = parser.parse_args()

    main(args.strategy, args.frequency, args.decision_rule, args.type_model,
         args.initial_value, args.max_allocation_long, args.max_allocation_short,
         args.start_date, args.end_date, args.save_history, args.risk_free_rate)
