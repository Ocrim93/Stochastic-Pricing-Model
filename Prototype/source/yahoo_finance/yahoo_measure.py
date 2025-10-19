from prototype.measure import Measure
from prototype.ticker import Ticker

class Measure_map:

	volatility_surface =  {
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

	price = {
			'Date' : Measure.DATE,
			'Open' : Measure.OPEN,
			'High' : Measure.HIGH,
			'Low' : Measure.LOW, 
			'Close' : Measure.CLOSE, 
			'Volume' : Measure.VOLUME,
			'Dividends' : Measure.DIVIDENDS
			
		}

	info = {
			'dividendYield' : Measure.DIVIDEND_YIELD
			}

def ticker_map():
	return { Ticker.SPX : '^SPX',
			 Ticker.SOFR : 'SR1=F'
			 }


def map_to_formating(key : str , measure : str = None):
	if measure != None:
		return getattr(Measure_map,key)[measure]
	return  getattr(Measure_map,key)

def map_from_formatting(key : str, measure :str = None ):
	if measure != None:
		return { v : k for k,v in map_to_formating(key).items() }[measure]
	return  { v : k for k,v in map_to_formating(key).items() }