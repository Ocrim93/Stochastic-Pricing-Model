from  Module.yahoo_finance.measure import measure_map
import pandas as pd
import os 

def formatting_data(data : pd.DataFrame, column_set : list = []  ):
	df = data.copy()
	column_map = measure_map()
	df = df.rename(columns = column_map)
	df = df[column_map.values()]
	df = df.sort_values
	if column_set != []:
		df = df[column_set]
	return df

