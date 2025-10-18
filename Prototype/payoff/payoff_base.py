from abc import ABC, abstractmethod

class Payoff(ABC):
	
	@abstractmethod
	def payoff(self):
		pass

	@abstractmethod
	def delta(self):
		pass

	@abstractmethod
	def vega(self):
		pass

	@abstractmethod
	def gamma(self):
		pass