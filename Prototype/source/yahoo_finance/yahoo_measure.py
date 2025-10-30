from prototype.measure import Measure
from prototype.ticker import Ticker
from collections import defaultdict
import pandas as pd 
from loguru import logger 

class Measure_map:

	def volatility_surface():
		  return {
				'strike' : Measure.STRIKE ,
				'impliedVolatility' : Measure.SOURCE_IMPLIED_VOLATILITY ,
				'bid' : Measure.BID,
				'ask' : Measure.ASK ,
				'lastPrice' : Measure.LAST_PRICE, 
				'currency' : Measure.CURRENCY,
				'volume' : Measure.VOLUME,
				'openInterest' : Measure.OPEN_INTEREST ,
				'contractSize' : Measure.CONTRACT_SIZE,
				'lastTradeDate' : Measure.DATE
			}

	def price():
		return  {
				'Date' : Measure.DATE,
				'Open' : Measure.OPEN,
				'High' : Measure.HIGH,
				'Low' : Measure.LOW, 
				'Close' : Measure.CLOSE, 
				'Volume' : Measure.VOLUME,
				'Dividends' : Measure.DIVIDENDS
			}

	def info():
		return  {
				'dividendYield' : Measure.DIVIDEND_YIELD
				}

class Yahoo_Ticker:
	__cache = {}
	__io = 'prototype/source/yahoo_finance/yahoo_measure.csv'

	def __init__(self):
		pass

	@classmethod
	def load_or_get_cache(cls):
		if cls.__cache  == {}:
			df = pd.read_csv(cls.__io)	
			n = len(df)
			
			logger.info(f'loading yahoo finance tickers, n. {n}')
			
			df_dict = df.to_dict()
			cls.__cache = { df_dict['Ticker'][i] : df_dict['Yahoo_Ticker'][i]   for i in range(n) }

			return cls.__cache
		else:
			return __cache

def map_to_formating(key : str , measure : str = None):
	if measure != None:
		return getattr(Measure_map,key)()[measure]
	return  getattr(Measure_map,key)()

def map_from_formatting(key : str, measure :str = None ):
	if measure != None:
		return { v : k for k,v in map_to_formating(key).items() }[measure]
	return  { v : k for k,v in map_to_formating(key).items() }

def ticker_map(ticker):
	t = defaultdict(lambda : ticker)

	t.update(Yahoo_Ticker.load_or_get_cache())
	return t[ticker]
			 