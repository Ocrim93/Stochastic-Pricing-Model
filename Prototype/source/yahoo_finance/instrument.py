from  .yahoo_measure import map_to_formating, ticker_map
import pandas as pd
from prototype.measure import Measure


def formatting_data(data : pd.DataFrame, key : str,  column_set : list = []  ):
	df = data.reset_index()
	column_map = map_to_formating(key)
	df = df.rename(columns = column_map)
	
	df = df[[col for col in column_map.values() if col in df.columns]]
	if column_set != []:
		df = df[column_set]
	df[Measure.DATE] = pd.to_datetime(df[Measure.DATE])
	return df

def get_ticker(ticker : str):
	return ticker_map(ticker)
