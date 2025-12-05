from loguru import logger
import os 
from datetime import datetime
import pandas as pd
from .measure import Measure as M
import numpy as np
from .ticker import Ticker
from zoneinfo import ZoneInfo
from .timeHelper import TimeHelper 

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
	M(Measure_io)
		
def formatting_input(args) -> dict:
	args_map = {}
	for t in args._get_kwargs():
		if t[0] in ['currency', 'ticker', 'frequency']:
			args_map[t[0]] = t[1].upper() if t[1] != None else None
		else:
			args_map[t[0]] = t[1]
	return args_map

def compute_volatility_log_pct(dataset: pd.DataFrame, column : str, frequency : str, convention : str ):
	time_factor = np.sqrt(TimeHelper.time_conversion(convention, frequency))
	
	dataset[M.LOG_PCT] = np.log(dataset[column].shift(periods=-1)/dataset[column])
	vol = dataset[M.LOG_PCT].std(ddof = 1)/time_factor
	return vol

def compute_pct_change(dataset: pd.DataFrame, column : str, frequency : str, convention : str = 'trading' ):
	time_factor = np.sqrt(TimeHelper.time_conversion(convention, frequency))

	logger.info(f'computing {M.PCT_CHANGE} and {M.LOG_PCT}')
	dataset[M.PCT_CHANGE] = dataset[column].pct_change(fill_method=None)
	logger.info(f'{M.PCT_CHANGE} mean : {dataset[M.PCT_CHANGE].mean():.3f} : std {dataset[M.PCT_CHANGE].std(ddof = 1)*100/time_factor:.3f} %')
	
	vol = compute_volatility_log_pct(dataset, column, frequency, convention )
	logger.info(f'{M.LOG_PCT} mean : {dataset[M.LOG_PCT].mean():.3f} : std {vol*100:0.2f} %')
	return vol

def applying_fx_spot(ticker_df : pd.DataFrame, fx_df : pd.DataFrame, columns : list):
	logger.info('applying fx spot')
	merging_data = ticker_df.merge(fx_df, how = 'inner', on = M.DATE, suffixes = ('_TICKER','_FX'))
	for col in columns:
		merging_data[col] = merging_data[f'{col}_TICKER']*merging_data[f'{col}_FX']

	logger.info(f'number of rows after fx splot {len(merging_data)}')
	merging_data = merging_data.drop(columns = [col for col in merging_data.columns if ('_TICKER' in col or '_FX' in col)], axis =1)
	return merging_data

def build_pair_dataset(num_df : pd.DataFrame, den_df : pd.DataFrame):
	pair_df = num_df.merge(den_df, how = 'inner' , on = M.DATE, suffixes = ('_num' , '_den') )
	pair_df[M.CLOSE] = pair_df[f'{M.CLOSE}_num']/pair_df[f'{M.CLOSE}_den']

	return pair_df[[M.DATE,M.CLOSE]]

def build_business_dates_dataset(start_date, end_date, freq = 'B') :

	date_range = pd.bdate_range(start=start_date, end=end_date, freq = (freq if 'W' not in freq else 'W'), tz = ZoneInfo(TimeHelper.TIME_ZONE))
	date_range_df = pd.DataFrame(data = { M.DATE : date_range})
	date_range_df[M.DATE] = date_range_df[M.DATE].apply(lambda x : x.date())
	
	if 'W' in freq: date_range_df[M.DATE] = TimeHelper.adjustementWeekFreq(date_range_df[M.DATE],freq)
	
	return date_range_df

def check_missing_dates(dataset : pd.DataFrame, start_date : datetime, end_date : datetime, freq : str):
	dataset[M.DATE] = pd.to_datetime(dataset[M.DATE],format = "%Y-%b-%d", utc = True)
	dataset[M.DATE] = dataset[M.DATE].apply(lambda x : x.astimezone(ZoneInfo(TimeHelper.TIME_ZONE)))
	dataset[M.DATE] = dataset[M.DATE].apply(lambda x : x.date())

	dataset.sort_values(by = M.DATE, ignore_index=True, ascending = True, inplace = True)

	date_range_df = build_business_dates_dataset(start_date, end_date, freq)
	missing_dates = date_range_df[~date_range_df[M.DATE].isin(dataset[M.DATE].to_list()) ]
	#check that two datasets have the same length 
	if not missing_dates.empty:
		logger.warning(f'missing date, n {len(missing_dates)}')
		print(missing_dates)
	merged = date_range_df.merge(dataset, how = 'left', on = M.DATE)
	merged['freq_date'] = np.where(merged[M.DATE].isin(date_range_df[M.DATE].to_list()),True,False)
	return merged

def cleaning_data(data: pd.DataFrame, start_date : datetime, end_date : datetime ,columns: list = [], drop_columns : list =[], frequency = 'B'):
	df = data.copy()
	df = df.drop(columns = drop_columns, axis = 1)
	df = check_missing_dates(df, start_date, end_date, frequency)
	for col in columns:
		if sum(df[col].isna()) > 0:
			logger.warning(f'forward and back fill, {col} n. {sum(df[col].isna()) }')
			df[col] = df[col].ffill().bfill()
	df = df[df['freq_date']]
	df = df.drop('freq_date', axis=1 )
	
	logger.info(f'cleaning completed, n. records: {len(df)}')
	return df

