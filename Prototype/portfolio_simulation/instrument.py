import pandas as pd
from prototype.measure import Measure as M
from loguru import logger
from  datetime import datetime 
import numpy as np
from prototype.instrument import compute_volatility_log_pct,days_in_year
import math 

def extract_dataset(data_map : dict):
	data = pd.DataFrame()
	for asset, df in data_map.items():
		if data.empty :
			data = df
		else:
			data = data.merge(df, how = 'inner', on = M.DATE)
		data.rename(columns = {M.CLOSE : asset}, inplace = True)
	data.set_index(M.DATE, inplace = True)

	return data

def extract_weight_dataset(weight_map : dict ):
	if sum([weight  for _, weight in weight_map.items()]) != 1 :
		logger.warning(f'weight sum not 1, given default: {1/len(weight_map):.03f}')
		weight_map  = { asset : 1/len(weight_map) for asset  in weight_map}
	return pd.DataFrame(data = { asset_name: [weight] for asset_name, weight in weight_map.items()})

def rebalancing_dates(start_date : datetime, end_date : datetime, frequency : str, data : pd.DataFrame):
	logger.info(f'rebalancing dates with freq : {frequency}')
	date_range = pd.bdate_range(start= start_date, end= end_date, freq = frequency)
	date_range = date_range.map(lambda x : x.date())
	data[M.REBALANCING_DATE] = np.where(data.index.isin(date_range), True, False)

def adding_quantity(data : pd.DataFrame, quantity_df : pd.DataFrame):
	for col in quantity_df.columns:
			quantity_df[col] = quantity_df[col].cumsum()
	quantity_df = data.index.to_frame().join(quantity_df, how = 'left')
	for asset in quantity_df.columns:
		quantity_df[asset] = quantity_df[asset].ffill()
		quantity_df[asset] = quantity_df[asset].fillna(0)

	quantity_df.set_index(M.DATE, inplace = True)

	data = data.merge(quantity_df,how ='left' ,suffixes = ('','_Q'), on = M.DATE)
	return quantity_df, data

def adding_cash(data :pd.DataFrame, budget_per_frequency : float):
	data.loc[data[M.REBALANCING_DATE], M.CASH] = budget_per_frequency
	data[M.CASH] = data[M.CASH].cumsum()
	data[M.CASH] = data[M.CASH].ffill()
	data[M.CASH] = data[M.CASH].fillna(0)


def adding_pnl(data : pd.DataFrame, quantity_df : pd.DataFrame):
	data[M.BALANCE] = 	(data*quantity_df).sum(axis=1) 
	data[M.PnL] = data[M.BALANCE] - data[M.CASH]
	
	data[M.PnL] = data[M.PnL].fillna(0)
	data[M.BALANCE] = data[M.BALANCE].fillna(0)

def compute_sharpe_ratio(data : pd.DataFrame, risk_free_rate : float):
	vol = compute_volatility_log_pct(data.copy(), M.BALANCE, 'B', 'trading')

	rate_of_return = math.pow(data.iloc[-1][M.BALANCE]/data.iloc[-1][M.CASH], len(data)/days_in_year('trading'))
	return (rate_of_return - risk_free_rate )/vol

