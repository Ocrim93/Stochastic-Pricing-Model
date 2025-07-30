from loguru import logger
import pandas as pd 
from typing import Callable
import pandas as pd
from measure import Measure
from datetime import datetime

class Volatility_Surface :

	@staticmethod
	def NewtonRaphson(target : float,
					  start : float ,
					  accuracy : float,
					  function : Callable, 
					  derivative : Callable
					  ):
		y = payoff_function(start)
		x = start 
		while (abs(y-target) > accuracy):
			d = derivative(x)
			x += (target - y)/d
			y = payoff_function(x)
		return x



	def __init__(self,
				 ticker : str,
				 data : dict, 
				 start_date : datetime
				 spot_price : float,
				 risk_free_rate : float = 0.,
				 dividend_yield : float = 0
				 ):	
		self.ticker = ticker
		self.data = data
		self.s = spot_price
		self.r = ticker
		self.q = dividend_yield
		self.volatility_surface = {}

	def compute(self):
		expirations = self.data.keys()
		df = pd.DataFrame()
		df[Measure.TIME_TO_MATURITY] = expirations
		df.set_index(Measure.TIME_TO_MATURITY , inplace= True)
		print(df)
