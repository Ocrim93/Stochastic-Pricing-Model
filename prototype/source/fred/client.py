"""
	Federal Reserve Bank of St. Louis 
		*** FRED ***
	https://fred.stlouisfed.org/
"""

import requests
from prototype.source.clientBase import Client 
from .utils import get_ticker, build_dataframe, last_price_and_date
from loguru import logger 
import pandas as pd


class FREDClient(Client):
	url = "https://api.stlouisfed.org/fred/series/observations"
	API_KEY = "0afd5ab34752fa5151ffcc9e6f6e8721"

	def __init__(self, ticker: str ):
		
		params = {
    				"series_id": get_ticker(ticker),
    				"api_key": self.__class__.API_KEY,
    				"file_type": "json"
				}
		self.ticker = ticker
		response = requests.get(self.__class__.url, params = params)
		response.raise_for_status()
		
		self.client = response
		self.data = pd.DataFrame()

	def fetch_price(self):
		values = self.client.json()['observations']
		data = build_dataframe(values)
		logger.info(f'fetch {self.ticker}, n. records {len(data)}' )
		self.data = data

		return data
	
	def fetch_current_price(self):
		if self.data.empty: df = self.fetch_price()
		else:  df = self.data

		closing_price, current_date = last_price_and_date(df)
		print(closing_price, current_date)
		logger.info(f"current closing price {self.ticker} : {closing_price:.2f} {current_date}")
		return closing_price

	def fetch_currency(self) -> str :
		return 'EUR'
	
	def fetch_options(self):
		pass
