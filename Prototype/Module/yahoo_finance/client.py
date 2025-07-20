from datetime import datetime
import pandas as pd 
from loguru import logger 
import yfinance as yf

class Client:
	def __init__(self,
				 ticker : str,
				 start_date : datetime,
				 end_date : datetime = None):
		
		self.ticker = ticker
		self.start_date = start_date
		self.end_date = datetime.now() if None else end_date
		logger.info(f'Creating Yahoo Client')
		self.client = yf.Ticker(ticker)

	def fetch(self) -> pd.DataFrame:
		logger.info(f"Starting fetch {self.ticker} prices")
		df = self.client.history(start = self.start_date, end=self.end_date)

		return df
