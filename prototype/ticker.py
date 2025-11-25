import pandas as pd 
from loguru import logger 

class Ticker:

	__cache = {}
	_loaded  = False

	def __init__(self, io : str, key : str ):
		self.io = io
		self.key = key
		data = self.load_or_get_cache()
		for k,_ in data.items():
			setattr(self.__class__, k,k)
		self.__class__._loaded  = True

	def load_or_get_cache(self):
		if self.key in self.__class__.__cache:
			return __cache[self.key]
		else:
			df = pd.read_csv(self.io)	
			n = len(df)
			
			logger.info(f'loading {self.key}, n. {n}')
			
			df_dict = df.to_dict()
			self.__class__.__cache[self.key] = { df_dict['Ticker'][i] : df_dict['Currency'][i]   for i in range(n) }

			return self.__class__.__cache[self.key]

