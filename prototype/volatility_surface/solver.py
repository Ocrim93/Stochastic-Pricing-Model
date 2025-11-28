from typing import Callable
import math
from loguru import logger
from .instrument import timer

class Solver :

	@staticmethod
	def NewtonRaphson(target : float,
					  start : float ,
					  payoff_function : Callable, 
					  derivative : Callable,
					  accuracy : float,
					  stop : float 
					  ):
		y = payoff_function(start)
		x = start 
		while (abs(y-target) > accuracy) and stop > 0 :
			d = derivative(x)
			x += (target - y)/d
			y = payoff_function(x)
			stop -= 1
		return x

	@staticmethod
	def Bisection(target : float,
				  high : float ,
				  low : float,
				  payoff_function : Callable, 
				  accuracy : float,
				  stop: float
				  ):
		
		x = (high+low)/2
		y = payoff_function(x)
		while (abs(y-target) > accuracy) and stop > 0 :
			if (y > target):
				high = x 
			else :
				low = x
			x = (high+low)/2
			y = payoff_function(x)
			stop -= 1
		return x

	def __init__(self, cap : tuple = (0,3), accuracy : float = 1e-3, stop : float = 1e4):
		
		self.success = True
		self.up_cap = cap[1]
		self.down_cap = cap[0] 
		self.result = 0
		self.accuracy = accuracy
		self.stop = stop
		
	@timer
	def run(self,solver, *args):
		logger.info(f'{solver} starting')
		method = getattr(self.__class__, solver)
		x = method(*args, self.accuracy, self.stop)
		if math.isinf(x) :
			logger.warning(f'{solver} unsuccessfull') 
			self.success = False
		else:
			logger.info(f'{solver} success')
			self.success = True
			self.result = min(max(self.down_cap, x), self.up_cap)




