from loguru import logger
import pandas as pd 
from typing import Callable
import pandas as pd
from .measure import Measure
from datetime import datetime
from .analytics import Analytics, AnalyticsForward
from .instrument import expiration_in_year

class Volatility_Surface :

	@staticmethod
	def NewtonRaphson(target : float,
					  start : float ,
					  payoff_function : Callable, 
					  derivative : Callable,
					  accuracy : float,
					  stop : float = 1e6
					  ):
		y = payoff_function(start)
		x = start 
		while (abs(y-target) > accuracy) or stop < 0 :
			d = derivative(x)
			x += (target - y)/d
			y = payoff_function(x)
			stop -= 1
		return x



	def __init__(self,
				 ticker : str,
				 data : dict, 
				 business_date : str,
				 spot_price : float,
				 risk_free_rate : float = 0.,
				 dividend_yield : float = 0 ,
				 forward_flag : bool = False 
				 ):	
		"""
			data : {'call' : {'t_ex' : DataFrame },
					'put'  : {'t_ex' : DataFrame }}
		"""

		self.ticker = ticker
		self.data = data
		self.business_date = business_date
		self.S = spot_price
		self.r = risk_free_rate
		self.q = dividend_yield
		self.volatility_surface = {'call' : None, 'put' : None}
		self.analytics = AnalyticsForward if forward_flag else Analytics


	def compute_IV_per_strike(self,data : pd.DataFrame,
								  time_to_expiration : float,
								  c_p :  int  ):

		IVs = {}
		
		for row in data.itertuples():
			strike = row.STRIKE
			impl_vol_source = row.SOURCE_IMPLIED_VOLATILITY
			start = impl_vol_source
			target = row.LAST_PRICE
			#call
			if c_p ==0 :
				payoff = lambda vol :   self.analytics.BSCall(self.S,strike,vol,self.r,time_to_expiration,self.q)
			#put
			if c_p ==1 :
				payoff = lambda vol :  self.analytics.BSPut(self.S,strike,vol,self.r,time_to_expiration, self.q)
			vega = lambda  vol  :   Analytics.BSVega(self.S,strike,vol,self.r,time_to_expiration,self.q)
			IV = Volatility_Surface.NewtonRaphson(target,start, payoff, vega, 1e-3 )
			IVs[strike] = { Measure.IV :  IV, Measure.LAST_PRICE : target, Measure.SOURCE_IMPLIED_VOLATILITY : impl_vol_source }

		return IVs

	def compute(self, c_p):
		call_put = 'call' if c_p ==0 else 'put'
		logger.info(f'starting computation volatility surface - {call_put} ')
		datum = self.data[call_put]
		volatility_surface = {}
		for t_exp in datum.keys():
			logger.info(f'time to expiration {t_exp} - {call_put}')
			time_to_expiration = expiration_in_year(self.business_date,t_exp,convention='actual')
			volatility_surface[t_exp] = self.compute_IV_per_strike(datum[t_exp],time_to_expiration,c_p )
		
		return volatility_surface
	
	def run(self):	
		logger.info('starting computation volatility surface')

		self.volatility_surface['call'] = self.compute(0)
		for k,v in self.volatility_surface['call'].items():
			for i,j in v.items():
				print(k,i,j[Measure.IV], j[Measure.SOURCE_IMPLIED_VOLATILITY])
		#self.volatility_surface['put'] = self.compute(1)








		

