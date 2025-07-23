from loguru import logger
import os 

def create_folder(path : str):
	if not os.path.exists(path):
		logger.info(f'creation folder {path}')
		os.makedirs(path)
