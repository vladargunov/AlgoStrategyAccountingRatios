class OLSCFG:
    required_number_dates = 6
    decision_rule = 'median'


class LogRegCFG:
    required_number_dates = 6
    decision_rule = 'octile'
    penalty = 'l2'
    regularize_strength = 1.0


class NNCFG:
    required_number_dates = 6
    decision_rule = 'median'
    type_regression = True
    hidden_shape = 128
    learning_rate = 0.3
    momentum = 0.4
    val_size = 0.1
    batch_size = 30
    log_loss = True
    log_frequency = 50
    epochs = 3
    val_check_interval = 1.0
