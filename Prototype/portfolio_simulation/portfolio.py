from .instrument import extract_dataset,extract_weight_dataset,rebalancing_dates,adding_quantity,adding_cash,adding_pnl
from loguru import logger
from prototype.measure import Measure as M
import datetime as dt


class Portfolio	:
	def __init__( self, 
				  data_map : dict, 
				  weight_map : dict,
				  start_date : dt.datetime,
				  end_date : dt.datetime,
				  frequency : str, 
				  budget : float = 0 ,
				  budget_per_frequency : float = 0
				  ):

		self.data = extract_dataset(data_map)
		self.weight = extract_weight_dataset(weight_map)
		self.base = 1 
		self.frequency = frequency
		rebalancing_dates(start_date, end_date, frequency, self.data)
		self.budget_per_frequency  =  budget/len(self.data[self.data[M.REBALANCING_DATE]]) if (budget_per_frequency == 0) else budget_per_frequency
		self.budget = budget_per_frequency*len(self.data[self.data[M.REBALANCING_DATE]])
		
		self.build_index()
		self.startegy()
		logger.info(f'cash invested : {self.budget:.2f} balance : {self.data.iloc[-1][M.BALANCE]:.2f} {M.PnL} : {self.data.iloc[-1][M.PnL]:.2f}' )
	
	def efficient_frontier(self):
		pass

	def compute_base(self):
		mean_per_asset = [self.data[asset].mean()  for asset in self.weight.columns]
		mean = sum(mean_per_asset)/len(mean_per_asset)
		base_exponent = 1
		while int(mean/10**base_exponent) > 0 :
			if int(mean/10**(base_exponent+1)) > 0:
				base_exponent += 1 
			else:
				break
		self.base = (10**base_exponent)
		logger.info(f'index base : {self.base}')
		return self.base

	def weighted_price_index(self):
		logger.info('computing dollar-weighted index')
		data = self.data 
		data[M.INDEX] = (data*self.weight.iloc[0]).sum(axis=1)
		
	def fixed_share_index(self):
		logger.info('computing fixed-share index') 
		data = self.data 
		base = self.compute_base()
		initial_prices = self.weight.iloc[0]/data.iloc[0]

		data[M.FIXED_SHARE_INDEX] = base*(data*initial_prices).sum(axis=1)

	def build_index(self):
		self.fixed_share_index()
		self.weighted_price_index()

	def startegy(self):
		logger.info(f'starting strategy with {self.budget_per_frequency:0.2f} per {self.frequency}')
		data = self.data
		
		quantity_df = (self.budget_per_frequency*self.weight.iloc[0]/data[data[M.REBALANCING_DATE]])[self.weight.columns]		
		quantity_df,data = adding_quantity(data, quantity_df)

		adding_cash(data, self.budget_per_frequency)
		adding_pnl(data,quantity_df)

		self.data = data.reset_index()

