from loguru import logger
import os 
from datetime import datetime, timedelta
from typing import Union
import pandas as pd
from .measure import Measure as M
import numpy as np
from .ticker import Ticker
from .measure import Measure
from zoneinfo import ZoneInfo

TIME_ZONE = 'Europe/London'

def create_folder(path : str):
	if not os.path.exists(path):
		logger.info(f'creation folder {path}')
		os.makedirs(path)

def retrieve_ticker_from_csv():
	Measure_io =  "prototype/input/Measure.csv"
	map_attribute = {'Index' :  "prototype/input/ticker/Index.csv",
					 'Equity' : "prototype/input/ticker/Equity.csv",
					 'InterestRate' : "prototype/input/ticker/InterestRate.csv"}

	for asset_class, path_file in map_attribute.items():
		Ticker(path_file,asset_class)
	Measure(Measure_io)
		
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
	return datetime(cob.year,cob.month,cob.day).astimezone(ZoneInfo(TIME_ZONE))

def build_business_dates_dataset(start_date, end_date, freq = 'B') :
	date_range = pd.date_range(start=start_date, end=end_date, freq = freq, tz = ZoneInfo(TIME_ZONE))
	date_range_df = pd.DataFrame(data = { M.DATE : date_range})
	date_range_df[M.DATE] = date_range_df[M.DATE].apply(lambda x : x.date())

	return date_range_df

def check_missing_dates(dataset : pd.DataFrame, freq : str):
	dataset[M.DATE] = pd.to_datetime(dataset[M.DATE],format = "%Y-%b-%d", utc = True)
	dataset[M.DATE] = dataset[M.DATE].apply(lambda x : x.astimezone(ZoneInfo(TIME_ZONE)))
	dataset[M.DATE] = dataset[M.DATE].apply(lambda x : x.date())

	dataset.sort_values(by = M.DATE, ignore_index=True, ascending = True, inplace = True)
	end_date = dataset[M.DATE].to_list()[-1]
	start_date = dataset[M.DATE].to_list()[0]

	date_range_df = build_business_dates_dataset(start_date, end_date, freq)
	missing_dates = date_range_df[~date_range_df[M.DATE].isin(dataset[M.DATE].to_list()) ]
	#check that two datasets have the same length 
	if not missing_dates.empty:
		logger.warning(f'missing date, n {len(missing_dates)}')
		print(missing_dates)
	merged = date_range_df.merge(dataset, how = 'left', on = M.DATE)
	merged['freq_date'] = np.where(merged[M.DATE].isin(date_range_df[M.DATE].to_list()),True,False)
	return merged

def cleaning_data(data: pd.DataFrame, columns: list = [], frequency = 'B'):
	df = data.copy()
	df = check_missing_dates(df, frequency)
	for col in columns:
		if sum(df[col].isna()) > 0:
			logger.warning(f'forward and back fill, {col} n. {sum(df[col].isna()) }')
			df[col] = df[col].ffill().bfill()
	df = df[df['freq_date']]
	df = df.drop('freq_date', axis=1 )
	
	logger.info(f'cleaning completed, n. records: {len(df)}')
	return df



