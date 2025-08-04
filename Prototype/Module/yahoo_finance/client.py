"""
	***Yahoo source does not support historical option prices***
"""


from datetime import datetime
import pandas as pd 
from loguru import logger 
import yfinance as yf
from .instrument import formatting_data
from .yahoo_measure import map_to_formating,map_from_formatting
from measure import Measure
from instrument import chang_date_formatting

class Yahoo_Client:
	def __init__(self,
				 ticker : str,
				 start_date : datetime,
				 end_date : datetime,
				 period : str = ""):
		
		self.ticker = ticker
		self.start_date = start_date
		self.end_date = end_date if start_date !=end_date else None
		self.period = period
		logger.info(f'creating Yahoo Client')
		self.client = yf.Ticker(ticker)

	def fetch(self) -> pd.DataFrame:
		logger.info(f"starting fetch {self.ticker} prices")
		if self.period == "":
			df = self.client.history(start = self.start_date, end=self.end_date)
		df = self.client.history(start = self.start_date, end=self.end_date)
		if df.empty:
			logger.warning(f" price {self.ticker} empty dataframe")
		formatted_df = formatting_data(df,'price')
		return formatted_df

	def fetch_financials(self) -> pd.DataFrame:
		logger.info(f'fetch financials for {self.ticker}')
		return self.client.financials

	def fetch_options(self) -> {}:
		'''
			***Yahoo source does not support historical option prices***

			return dictionary
			{Expiration_Date : (call_DataFrame, put_DataFrame)} 
		'''
		logger.info(f'fetch options for {self.ticker}')
		call_put = {}
		for d in self.client.options:
			options = self.client.option_chain(d)
			t_exp = chang_date_formatting(d, "%Y-%m-%d", "%d-%m-%Y")
			call_put['call'] = {t_exp :  formatting_data(options.calls, 'volatility_surface')}
			call_put['put'] = { t_exp :  formatting_data(options.puts,'volatility_surface')}
		
		return call_put

	def fetch_current_price(self):
		df = self.fetch()
		df = df.sort_values(by = Measure.DATE, ascending = True)
		closing_price = df[Measure.CLOSE].values[0]
		logger.info(f' current closing price {self.ticker}: {closing_price} {self.start_date}')
		return closing_price

	def fetch_dividend_yield(self) -> float:
		try :
			logger.info(f'fetching {self.ticker} dividend yield')
			return self.client.info[map_from_formatting('info',Measure.DIVIDEND_YIELD)]
		except :
			logger.warning(f'{self.ticker} dividendYield not found')
			return 0
