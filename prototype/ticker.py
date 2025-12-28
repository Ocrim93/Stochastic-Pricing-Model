import pandas as pd 
from loguru import logger 

class Ticker:

	__cache = {}
	_loaded  = False
	assetClassMap = {}
	
	def __init__(self, io : str, key : str ):
		self.io = io

		data = self.load_or_get_cache(key)
		for k,_ in data.items():
			setattr(self.__class__, k,k)
		self.__class__._loaded  = True

	def load_or_get_cache(self, key : str):
		if key in self.__class__.__cache:
			return self.__class__.__cache[key]
		else:
			df = pd.read_csv(self.io)	
			n = len(df)
			
			logger.info(f'loading {key}, n. {n}')
			
			df_dict = df.to_dict()
			self.__class__.__cache[key] = { df_dict['Ticker'][i] : df_dict['Currency'][i]   for i in range(n) }
			self.__class__.assetClassMap.update( { df_dict['Ticker'][i] : key   for i in range(n) }) 

			return self.__class__.__cache[key]

