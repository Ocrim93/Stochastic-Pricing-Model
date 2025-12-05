from abc import ABC, abstractmethod

class Client(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def fetch_price(self):
		pass

	@abstractmethod
	def fetch_options(self):
		pass

	@abstractmethod
	def fetch_current_price(self):
		pass