from loguru import logger
import pandas as pd 
from prototype.measure import Measure as M
from datetime import datetime
from .analytics import Analytics, AnalyticsForward
from .instrument import expiration_in_year, build_dataframe
from .solver import Solver


class VolatilitySurface :

	def __init__(self,
				 ticker : str,
				 options_data : dict, 
				 business_date : str,
				 spot_price : float,
				 risk_free_rate : float = 0,
				 dividend_yield : float = 0 ,
				 forward_flag : bool = False 
				 ):	
		"""
			data : {'call' : {'t_ex' : DataFrame },
					'put'  : {'t_ex' : DataFrame }}
		"""

		self.business_date = business_date
		self.ticker = ticker
		self.options_data = options_data
		self.S = spot_price
		self.r = risk_free_rate
		self.q = dividend_yield
		self.IV_data = {'call' : None, 'put' : None}
		
		self.analytics = AnalyticsForward if forward_flag else Analytics

	def solver_IV(self,target,start, payoff, vega):
		solver = Solver()
			
		solver.run('NewtonRaphson',target,start, payoff, vega)
		if solver.success: 
			IV = solver.result
			solver_name = 'NewtonRaphson'
		else:
			solver.run('Bisection',target, 2,0, payoff)
			if solver.success :
				IV = solver.result
				solver_name = 'Bisection'
			else:
				IV = 0
				solver_name = 'None'
		return IV, solver_name

	def compute_IV_per_strike(self,data : pd.DataFrame,
								  time_to_expiration : float,
								  c_p :  int  ):

		IVs = {}
		for row in data.itertuples():
			strike = row.STRIKE
			impl_vol_source = row.SOURCE_IMPLIED_VOLATILITY
			start = 0.2
			target = row.LAST_PRICE
			target_ask = row.ASK
			target_bid = row.BID

			#call
			if c_p == 1 :
				payoff = lambda vol :   self.analytics.BSCall(self.S,strike,vol,self.r,time_to_expiration,self.q)
			#put
			if c_p == 2 :
				payoff = lambda vol :  self.analytics.BSPut(self.S,strike,vol,self.r,time_to_expiration, self.q)
			vega = lambda  vol  :   Analytics.BSVega(self.S,strike,vol,self.r,time_to_expiration,self.q)
			
			IV, solver_name = self.solver_IV(target,start, payoff, vega)
			ASK_IV, solver_name_ask = self.solver_IV(target_ask,start, payoff, vega)
			BID_IV, solver_name_bid = self.solver_IV(target_bid,start, payoff, vega)

			IVs[strike] = { M.IV : IV,
							M.ASK_IV : ASK_IV,
							M.BID_IV : BID_IV,
							M.SOURCE_IMPLIED_VOLATILITY: impl_vol_source,
							M.LAST_PRICE: target,
							M.BID: target_bid,
							M.ASK: target_ask,
							M.SOLVER_NAME : solver_name,
							M.CURRENCY : row.CURRENCY }
		return IVs

	def compute(self, c_p : int ):
		call_put = 'call' if c_p ==1 else 'put'
		logger.info(f'starting computation volatility surface - {call_put} ')
		datum = self.options_data[call_put]
		volatility_surface = {}

		for t_exp in datum.keys():
			logger.info(f'time to expiration {t_exp} - {call_put}')
			time_to_expiration = expiration_in_year(self.business_date,t_exp, convention='actual')
			volatility_surface[t_exp] = self.compute_IV_per_strike(datum[t_exp],time_to_expiration,c_p )
		
		return volatility_surface
	
	def run(self):	
		logger.info('starting computation volatility surface')

		self.IV_data['call'] = build_dataframe(self.compute(1))
		self.IV_data['put'] = build_dataframe(self.compute(2))






		

