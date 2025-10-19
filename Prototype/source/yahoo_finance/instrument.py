from  .yahoo_measure import map_to_formating, ticker_map
import pandas as pd
import os 
from datetime import datetime, timedelta


def formatting_data(data : pd.DataFrame, key : str,  column_set : list = []  ):
	df = data.copy()
	df = df.reset_index()
	column_map = map_to_formating(key)
	df = df.rename(columns = column_map)
	
	df = df[[col for col in column_map.values() if col in df.columns]]
	if column_set != []:
		df = df[column_set]
	return df

def formatting_ticker(ticker : str):
	return ticker_map()[ticker]

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
