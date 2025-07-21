from datetime import datetime
import pandas as pd 
from loguru import logger 
import yfinance as yf

class Client:
	def __init__(self,
				 ticker : str,
				 start_date : datetime,
				 end_date : datetime = None,
				 period : str = ""):
		
		self.ticker = ticker
		self.start_date = start_date
		self.end_date = datetime.now() if None else end_date
		self.period = period
		logger.info(f'Creating Yahoo Client')
		self.client = yf.Ticker(ticker)

	def fetch(self) -> pd.DataFrame:
		logger.info(f"Starting fetch {self.ticker} prices")
		if self.period == "":
			df = self.client.history(start = self.start_date, end=self.end_date)
		df = self.client.history(start = self.start_date, end=self.end_date)

		return df

	def fetch_financials(self) -> pd.DataFrame:
		logger.info(f'Fetch financials for {self.ticker}')
		return self.client.financials

	def fetch_options(self) -> {}:
		logger.info(f'Fetch options for {self.ticker}')
		'''
			return dictionary
			{Expiration_Date : (call_DataFrame, put_DataFrame)}
		'''
		call_put = {}
		for d in self.client.options:
			options = self.client.option_chain(d)
			call_put[d] = (options.calls,options.puts)
		return call_put

