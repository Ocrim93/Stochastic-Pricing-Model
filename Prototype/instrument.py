from loguru import logger
import os 
from datetime import datetime, timedelta
from typing import Union
import pandas as pd
from .measure import Measure as M

def create_folder(path : str):
	if not os.path.exists(path):
		logger.info(f'creation folder {path}')
		os.makedirs(path)

def change_date_formatting(cob : Union[datetime,str] , formatting_from :str , formatting_to : str) -> str:
	if isinstance(cob, str):
		cob = datetime.strptime(cob,formatting_from)
	cob = cob.strftime(formatting_to)
	return cob

def formatting_input(args) -> dict:
	args_map = {}
	for t in args._get_kwargs():
		args_map[t[0]] = t[1]
	return args_map

def business_date(date : str):
	date = datetime.strptime(date, "%d/%m/%Y") if date != None else datetime.now() 
	shift = timedelta(days = 0)
	#check if Saturday
	if date.strftime("%w") == '6':
		shift = timedelta(days = 1)
	#check if Sunday
	if date.strftime("%w") == '0':
		shift = timedelta(days = 2)
	cob = date - shift
	return datetime(cob.year,cob.month,cob.day)

def check_missing_dates(dataset : pd.DataFrame, freq : str):
	end_date = dataset[M.DATE].to_list()[-1]
	start_date = dataset[M.DATE].to_list()[0]

	date_range = pd.date_range(start=start_date, end=end_date, freq = freq)
	date_range_df = pd.DataFrame(data = { M.DATE : date_range})

	missing_dates = date_range_df[~date_range_df[M.DATE].isin(dataset[M.DATE].to_list()) ]
	#check that two datasets have the same length 
	if not missing_dates.empty:
		logger.warning(f'missing date, n {len(missing_dates)}')
		print(missing_dates)
	merged = dataset.merge(date_range_df, how = 'inner', on = M.DATE)
	return merged

def cleaning_data(data: pd.DataFrame, columns: list = [], freq = 'B'):
	df = data.copy()
	for col in columns:
		if sum(data[col].isna()) > 1:
			logger.warning(f'forwardfill and backfill {col} - {sum(data[col].isna()) }')
			df[col].ffill(inplace = True).bfill(inplace = True)
	df.sort_values(by = M.DATE, ignore_index= True, ascending = True,inplace = True)
	return check_missing_dates(df, freq)









