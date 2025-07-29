from measure import Measure

measure_map =  {
		'Strike' : Measure.STRIKE ,
		'ImpliedVolatility' : Measure.IMPLIED_VOLATILITY ,
		'Bid' : Measure.BID,
		'Ask' : Measure.ASK ,
		'High' : Measure.HIGH,
		'Low' : Measure.LOW, 
		'Close' : Measure.CLOSE, 
		'currency' : Measure.CURRENCY,
		'Volume' : Measure.VOLUME,
		'openInterest' : Measure.OPEN_INTEREST ,
		'contractSize' : Measure.CONTRACT_SIZE,
		'lastPrice' : Measure.LAST_PRICE,
		'dividendYield' : Measure.DIVIDEND_YIELD,
		'Date' : Measure.DATE
	}

def map_to_formating():
	return measure_map

def map_from_formatting():
	return { v : k for k,v in measure_map.items() }