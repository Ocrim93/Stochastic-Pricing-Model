from enum import Enum

class Measure(Enum):
	STRIKE = 'strike'
	IMPLIED_VOLATILITY = 'impliedVolatility'
	BID = 'bid'
	ASK = 'ask'
	CURRENCY = 'currency'
	VOLUME= 'volume'
	OPEN_INTEREST = 'openInterest'
	CONTRACT_SIZE = 'contractSize'
	LAST_PRICE = 'lastPrice'


def measure_map():
	s = {}
	for m in Measure:
		s[m.value] = m.name
	return s