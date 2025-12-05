from datetime import datetime, timedelta
from prototype.timeHelper import TimeHelper 
from prototype.measure import Measure as M
from loguru import logger
import time 
import pandas as pd

LIST_SYMBOL = ['F','G','H','J','K','M','N','Q','U','V','X','Z']

def get_map_month_symbol(reverse = False ):
	if reverse:
		map_month_symbol = {  symbol : idx+1  for idx,symbol in  enumerate(LIST_SYMBOL)}
	else:
		map_month_symbol = { idx+1 : symbol for idx,symbol in  enumerate(LIST_SYMBOL)}
	return map_month_symbol

def expiration_in_year(date1 : datetime,
					   date2 : datetime,
					   convention : str,
					   formatting :str = '%d/%m/%Y' ) -> float :
					   
	date1 = datetime.strptime(date1, formatting)
	date2 = datetime.strptime(date2, formatting)
	days = (date2 - date1).days

	return days/TimeHelper.days_in_year(convention)

def build_dataframe( IV_dict : dict ):
	df = pd.DataFrame()

	for t_exp, data in IV_dict.items():
		for strike,data_per_strike in data.items():
			d = { k : [v] for k,v in data_per_strike.items()}
			d[M.STRIKE] = [strike]
			d[M.SETTLEMENT_DATE] = [t_exp]
			temp_df  = pd.DataFrame(data=d)
			df = pd.concat([df,temp_df], ignore_index = True)
	df[M.SETTLEMENT_DATE] = pd.to_datetime(df[M.SETTLEMENT_DATE], format='%d/%m/%Y')
	return df

def timer(func):
	def inner(*args, **kwargs):
		start = time.time()
		result = func(*args, **kwargs)
		dt = time.time() -start
		mins, secs = dt//60 , round(dt%60,2)
		logger.info(f'operation took -> {mins } m {secs}')
		return result
	return inner

