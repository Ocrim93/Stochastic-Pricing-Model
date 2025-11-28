from datetime import datetime, timedelta
from prototype.instrument import days_in_year
from loguru import logger
import time 

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

	return days/days_in_year(convention)

def timer(func):
	def inner(*args, **kwargs):
		start = time.time()
		result = func(*args, **kwargs)
		dt = time.time() -start
		mins, secs = dt//60 , round(dt%60,2)
		logger.info(f'operation took -> {mins } m {secs}')
		return result
	return inner

