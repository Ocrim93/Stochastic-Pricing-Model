"""
	*** Euro Short-Term Rate ***
	
	Fetch Ester overnight reference rate

	from European Central Bank (ECB) 
"""

import requests
from prototype.source.clientBase import Client 
from .utils import build_dataframe, last_price_and_date
from loguru import logger 
import pandas as pd


class EsterClient(Client):
	url = "https://api.estr.dev/historical"

	def __init__(self):
		response = requests.get(self.__class__.url)
		response.raise_for_status()
		self.client = response
		self.data = pd.DataFrame()

	def fetch_price(self):
		data = self.client.json()
		df = build_dataframe(data)
		logger.info(f'fetch €STER, n. records {len(df)}' )
		self.data = df 
		return df
	
	def fetch_current_price(self):
		if self.data.empty: df = self.fetch_price()
		else:  df = self.data
		closing_price,current_date = last_price_and_date(df)
		logger.info(f' current closing price €STER: {closing_price:.2f} {current_date}')
		return closing_price

	def fetch_currency(self) -> str :
		return 'EUR'
	
	def fetch_options(self):
		pass
