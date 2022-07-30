# OLS strategy
python trade.py -s OLSRatios -f monthly -d median -start 2020-07-01 --save_history
python trade.py -s OLSRatios -f monthly -d quartile -start 2020-07-01 --save_history
python trade.py -s OLSRatios -f monthly -d octile -start 2020-07-01 --save_history

# Logit method
python trade.py -s LogitRatios -f monthly -d median -start 2020-07-01 --save_history
python trade.py -s LogitRatios -f monthly -d quartile -start 2020-07-01 --save_history
python trade.py -s LogitRatios -f monthly -d octile -start 2020-07-01 --save_history

# NNReg method
python trade.py -s NNRatios -f monthly -d median -t regression -start 2020-07-01 --save_history
python trade.py -s NNRatios -f monthly -d quartile -t regression -start 2020-07-01 --save_history
python trade.py -s NNRatios -f monthly -d octile -t regression -start 2020-07-01 --save_history

# NNClass method
python trade.py -s NNRatios -f monthly -d median -t classification -start 2020-07-01 --save_history
python trade.py -s NNRatios -f monthly -d quartile -t classification -start 2020-07-01 --save_history
python trade.py -s NNRatios -f monthly -d octile -t classification -start 2020-07-01 --save_history
