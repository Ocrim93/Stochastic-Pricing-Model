import pandas as pd 
from loguru import logger 

class Measure:

	__cache = {}
	_loaded = False

	def __init__(self, io : str, key : str = 'Measure' ):
		self.io = io
		self.key = key
		data = self.load_or_get_cache()
		for k,v in data.items():
			setattr(self.__class__, k,v) 
		self.__class__._loaded = True

	def load_or_get_cache(self):
		if self.key in self.__class__.__cache:
			return self.__class__.__cache[self.key]
		else:
			df = pd.read_csv(self.io)	
			n = len(df)
			
			logger.info(f'loading {self.key}, n. {n}')
			
			df_dict = df.to_dict()
			self.__class__.__cache[self.key] = { df_dict['Measure_key'][i] : df_dict['Measure_value'][i]   for i in range(n) }
			return self.__class__.__cache[self.key]