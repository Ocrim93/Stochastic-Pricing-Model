import numpy as np
import math
from scipy.stats import norm


class Analytics:

	def __init__():
		pass

	@staticmethod 
	def BSCall(S,K,sigma,r,T,q):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + (r - q)*T + 1/2*vol*vol)/vol
		d2 = d1 - vol
		return S*math.exp(-q*T)*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)

	@staticmethod 
	def BSPut(S,K,sigma,r,T,q):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + (r - q)*T + 1/2*vol*vol)/vol
		d2 = d1 - vol
		return  K*math.exp(-r*T)*norm.cdf(-d2) - S*math.exp(-q*T)*norm.cdf(-d1) 

	@staticmethod 
	def BSDeltaCall(S,K,sigma,r,T,q):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + (r - q)*T + 1/2*vol*vol)/vol
		return  math.exp(-q*T)*norm.cdf(d1)

	@staticmethod 
	def BSDeltaPut(S,K,sigma,r,T,q):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + (r - q)*T + 1/2*vol*vol)/vol
		return  math.exp(-q*T)*(norm.cdf(d1) - 1 ) 

	@staticmethod 
	def BSVega(S,K,sigma,r,T,q):
		vol = sigma*math.sqrt(T)
		d1 = (math.log(S/K) + (r - q)*T + 1/2*vol*vol)/vol
		return S*math.exp(-q*T) * norm.pdf(d1)* math.sqrt(T)


class AnalyticsForward(Analytics):

	@staticmethod 
	def BSCall(F,K,sigma,r,T,*args):
		c = Analytics.BSCall(F,K,sigma,0,T,0)
		return c*math.exp(-r*T)

	@staticmethod 
	def BSPut(F,K,sigma,r,T,*args):
		p = Analytics.BSPut(F,K,sigma,0,T,0)
		return p*math.exp(-r*T)

	@staticmethod 
	def BSVega(F,K,sigma,r,T,*args):
		vega = Analytics.BSVega(F,K,sigma,0,T,0)
		return vega*math.exp(-r*T)

	@staticmethod 
	def BSDeltaCall(S,K,sigma,r,T,*args):
		delta = Analytics.BSDeltaCall(F,K,sigma,0,T,0)
		return delta*math.exp(-r*T)

	@staticmethod 
	def BSDeltaPut(S,K,sigma,r,T,*args):
		delta = Analytics.BSDeltaPut(F,K,sigma,0,T,0)
		return delta*math.exp(-r*T)

