from loguru import logger
import os 
from datetime import datetime, timedelta
from typing import Union

LIST_SYMBOL = ['F','G','H','J','K','M','N','Q','U','V','X','Z']

def get_map_month_symbol(reverse = False ):
	if reverse:
		map_month_symbol = {  symbol : idx+1  for idx,symbol in  enumerate(LIST_SYMBOL)}
	else:
		map_month_symbol = { idx+1 : symbol for idx,symbol in  enumerate(LIST_SYMBOL)}
	return map_month_symbol

def create_folder(path : str):
	if not os.path.exists(path):
		logger.info(f'creation folder {path}')
		os.makedirs(path)

def business_date(date : datetime = datetime.now()):
	#check if Saturday
	if date.strftime("%w") == '6':
		shift = timedelta(days = 1)
	#check if Sunday
	if date.strftime("%w") == '0':
		shift = timedelta(days = 2)
	cob = date - shift
	return datetime(cob.year,cob.month,cob.day)

def expiration_in_year(date1 : datetime,
					   date2 : datetime,
					   formatting :str = '%d-%m-%Y',
					   convention : str = 'trading_days' ) -> float :
	
	date1 = datetime.strptime(date1, formatting)
	date2 = datetime.strptime(date2, formatting)
	days = (date2 - date1).days
	if convention == 'actual':
		y = days/360
	if convention == 'trading_days':
		y = days/252

	return y

def chang_date_formatting(cob : Union[datetime,str] , formatting_from :str , formatting_to : str) -> str:
	if isinstance(cob, str):
		cob = datetime.strptime(cob,formatting_from)
	cob = cob.strftime(formatting_to)
	return cob