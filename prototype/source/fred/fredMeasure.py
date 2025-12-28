from prototype.ticker import Ticker
from collections import defaultdict
import pandas as pd 
from loguru import logger 

class FREDTicker:
	__io = 'prototype/source/fred/fredMeasure_resources.csv'
	__cache = {}

	def __init__(self):
		pass

	@classmethod
	def load_or_get_cache(cls):
		if cls.__cache  == {}:
			df = pd.read_csv(cls.__io)	
			n = len(df)
			
			logger.info(f'loading fred tickers, n. {n}')
			
			df_dict = df.to_dict()
			cls.__cache = { df_dict['Ticker'][i] : df_dict['FRED_Ticker'][i]   for i in range(n) }

			return cls.__cache
		else:
			return cls.__cache

def ticker_map(ticker):
	t = defaultdict(lambda : ticker)

	t.update(FREDTicker.load_or_get_cache())
	return t[ticker]

			 