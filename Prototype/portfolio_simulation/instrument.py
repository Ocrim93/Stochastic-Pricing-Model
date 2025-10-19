from prototype.source.yahoo_finance.client import Yahoo_Client 
from datetime import datetime
import pandas as pd

def fetch_client(source : str, ticker : str , start_date : datetime , end_date : datetime):
	if source == 'yahoo': 
		client = Yahoo_Client(ticker, start_date, end_date)

	return client

def formattind_dataframe():
	pass