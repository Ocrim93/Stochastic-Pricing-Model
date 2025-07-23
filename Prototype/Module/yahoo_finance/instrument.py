from  Module.yahoo_finance.measure import measure_map
import pandas as pd
import os 

def formatting_options(data : pd.DataFrame):
	df = data.copy()
	column_map = measure_map()
	df = df.rename(columns = column_map)
	df = df[column_map.values()]
	return df

