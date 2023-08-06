EASYFACTORLENS
##############

This lib can make IC test by data download from Ricequant.

Usage:

**step1**:Download 'download_data_from_ricequant.ipynb' from https://pan.baidu.com/s/1JOHi4w7nAypfIHKW_v1tng,

password:6666

**step2**:Download data from https://www.ricequant.com

**step3**:Set your parameters.

eg:

logger_path = './factor_logs.log'   # your log path

factor_info = "anything about your factor"

data_file = r'C:\Users\Administrator\Desktop\ricequant_local_alphalens\data'    # your data file path

predict_periods = (1, 5, 10)    # your factor predict periods

**step4**:Run analysis engine in your script.