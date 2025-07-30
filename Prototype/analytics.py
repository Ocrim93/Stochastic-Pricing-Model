import numpy as np
import math
from scipy.stats import norm


class Analytics:

	def __init__():
		pass

	@staticmethod 
	def BSCall(S,K,sigma,r,q,T):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + r - q + 1/2*vol*vol)/vol
		d2 = d1 - vol
		return S*math.exp(-q*T)*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)

	@staticmethod 
	def BSPut(S,K,sigma,r,q,T):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + r-q + 1/2*vol*vol)/vol
		d2 = d1 - vol
		return  K*math.exp(-r*T)*norm.cdf(-d2) - S*math.exp(-q*T)*norm.cdf(-d1) 
	
	@staticmethod 
	def BSVega(S,K,sigma,r,q,T):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + r - q + 1/2*vol*vol)/vol
		return S*math.exp(-q*T) * norm.pdf(d1)* math.sqrt(T)