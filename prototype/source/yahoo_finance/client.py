"""
	***Yahoo source does not support historical option prices***
"""

import sys
from datetime import datetime
import pandas as pd 
from loguru import logger 
import yfinance as yf
from .instrument import formatting_data, get_ticker,set_date_boundaries
from .yahoo_measure import map_to_formating,map_from_formatting
from prototype.measure import Measure
from prototype.instrument import change_date_formatting
from prototype.source.client_base import Client 

class Yahoo_Client(Client):
	def __init__(self,
				 ticker : str,
				 start_date : datetime,
				 end_date : datetime,
				 period : str = '1d',
				 FX_flag : bool = False
				 ):
		self.ticker = ticker
		self.start_date = start_date
		self.end_date = end_date if start_date != end_date else None
		self.period = period
		logger.info(f'creating Yahoo Client')
		yahoo_ticker = get_ticker(ticker,FX_flag)
		try:
			self.client = yf.Ticker(yahoo_ticker)
		except Exception as e:
			logger.error(f'client error occured, {e}')
			sys.exit(f'{e} - {yahoo_ticker}')

	def fetch_price(self) -> pd.DataFrame:
		logger.info(f"fetch {self.ticker} prices, period {self.period}")
		df = self.client.history(start = self.start_date, end=self.end_date , interval = self.period)
		if df.empty:
			logger.warning(f" price {self.ticker} empty dataframe")
		formatted_df = formatting_data(df,'price')
		formatted_df = set_date_boundaries(formatted_df,self.start_date,self.end_date)
		logger.info(f'yahoo retrieved {self.ticker} {len(formatted_df)} records')
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
			t_exp = change_date_formatting(d, "%Y-%m-%d", "%d/%m/%Y")
			call_put['call'] = {t_exp :  formatting_data(options.calls, 'volatility_surface')}
			call_put['put'] = { t_exp :  formatting_data(options.puts,'volatility_surface')}
		
		return call_put

	def fetch_balancesheet(self):
		return self.client.balancesheet

	def fetch_cashflow(self):
		return self.client.cash_flow

	def fetch_current_price(self):
		df = self.fetch_price()
		df = df.sort_values(by = Measure.DATE, ascending = True)
		closing_price = df[Measure.CLOSE].values[0]
		logger.info(f' current closing price {self.ticker}: {closing_price:.2f} {self.end_date}')
		return closing_price

	def fetch_currency(self) -> str :
		currency = self.client.info[map_from_formatting('info',Measure.CURRENCY)]
		logger.info(f'fetch {self.ticker} currency {currency}')
		return currency

	def fetch_dividend_yield(self) -> float:
		try :
			dividend = self.client.info[map_from_formatting('info',Measure.DIVIDEND_YIELD)]
			logger.info(f'fetch {self.ticker} dividend yield {dividend}')
			return dividend
		except :
			logger.warning(f'{self.ticker} dividendYield not found')
			return 0
