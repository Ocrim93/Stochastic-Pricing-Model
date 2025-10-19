import yaml
import pandas as pd
from .instrument import fetch_client
from prototype.measure import Measure as column

class Portfolio:
	def __init__(self):
		with open("prototype/portfolio_settings.yaml", "r") as file:
			data = yaml.safe_load(file)
		self.__dict__.update(data)
		self.data = pd.DataFrame()

	def fetch_data(self):
		for asset in self.asset:
			client = fetch_client(asset['source'], asset['name'], self.start_date, self.end_date)
			if self.data.empty():
				self.data = s
			print(client.fetch())
