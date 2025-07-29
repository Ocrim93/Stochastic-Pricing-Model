from  Module.yahoo_finance.yahoo_measure import map_to_formating
import pandas as pd
import os 

def formatting_data(data : pd.DataFrame, column_set : list = []  ):
	df = data.copy()
	df = df.reset_index()
	column_map = map_to_formating()
	df = df.rename(columns = column_map)
	
	df = df[[col for col in column_map.values() if col in df.columns]]
	if column_set != []:
		df = df[column_set]
	return df

