class OLSCFG:
    required_number_dates = 6
    decision_rule = 'median'


class LogRegCFG:
    required_number_dates = 6
    decision_rule = 'octile'
    penalty = 'none'
    regularize_strength = .001


class NNCFG:
    required_number_dates = 6
    type_model = 'regression' # 'classification'
    decision_rule = 'median'
    hidden_shape = 128
    learning_rate = 1e-2
    momentum = 0.4
    val_size = 0.1
    batch_size = 128
    log_loss = True
    log_frequency = 50
    epochs = 3
    val_check_interval = 1.0
