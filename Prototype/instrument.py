from loguru import logger
import os 

LIST_SYMBOL = ['F','G','H','J','K','M','N','Q','U','V','X','Z']

def get_map_month_symbol(reverse = False ):
	if reverse:
		map_month_symbol = {  symbol : idx+1  for idx,symbol in  enumerate(LIST_SYMBOL)}
	else:
		map_month_symbol = { idx+1 : symbol for idx,symbol in  enumerate(LIST_SYMBOL)}
	return map_month_symbol

def create_folder(path : str):
	if not os.path.exists(path):
		logger.info(f'creation folder {path}')
		os.makedirs(path)
