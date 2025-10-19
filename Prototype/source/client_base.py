from abc import ABC, abstractmethod

class Client(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def fetch(self):
		pass