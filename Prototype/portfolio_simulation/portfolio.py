from .instrument import extract_dataset,extract_weight_dataset,rebalancing_dates,adding_quantity,adding_cash,adding_pnl,compute_sharpe_ratio
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
				  risk_free_rate : float,
				  budget : float = 0 ,
				  budget_per_frequency : float = 0
				  ):

		self.data = extract_dataset(data_map)
		self.weight = extract_weight_dataset(weight_map)
		self.base = 1 
		self.frequency = frequency
		self.risk_free_rate =risk_free_rate
		
		rebalancing_dates(start_date, end_date, frequency, self.data)
		self.starting_date = self.data[self.data[M.REBALANCING_DATE]].index[0]
		#self.data = self.data.loc[self.data.index >= self.starting_date]
		
		self.budget_per_frequency  =  budget/len(self.data[self.data[M.REBALANCING_DATE]]) if (budget_per_frequency == 0) else budget_per_frequency
		self.budget = self.budget_per_frequency*len(self.data[self.data[M.REBALANCING_DATE]]) 
		
		self.build_index()
		self.startegy()
		self.sharpe_ratio()		
		
		self.investing_everything_at_t0()

		self.data.reset_index(inplace = True)

	def efficient_frontier(self):
		pass

	def sharpe_ratio(self):
		statistics_data = self.data[self.data.index >= self.starting_date]
		balance = statistics_data.iloc[-1][M.BALANCE]
		PnL = statistics_data.iloc[-1][M.PnL]

		logger.info(f'cash invested : {self.budget:.2f} | balance : {balance:.2f} | {M.PnL} : {PnL:.2f}')
		sharpe_ratio = compute_sharpe_ratio(statistics_data, self.risk_free_rate)
		logger.info(f'sharpe_ratio {sharpe_ratio:0.3f} | risk_free_rate : {self.risk_free_rate*100:.2f} %')

	def compute_base(self):
		mean_per_asset = [self.data[asset].mean()  for asset in self.weight.columns]
		mean = sum(mean_per_asset)/len(mean_per_asset)
		base = 10
		base_exponent = 0
		while int(mean/base**base_exponent) > 0 :
			if int(mean/base**(base_exponent+1)) > 0:
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

	def investing_everything_at_t0(self):
		logger.info(f'investing all at time {self.starting_date}')

		quantity_df = self.budget/self.data.loc[self.starting_date][self.weight.columns]
		balance = (self.data*quantity_df).sum(axis=1).values[-1]
		logger.info(f'cash invested : {self.budget:.2f} | balance : {balance:.2f} | {M.PnL} : {balance - self.budget:.2f}' )

	def startegy(self):
		logger.info(f'starting strategy with {self.budget_per_frequency:0.2f} per {self.frequency}')
		data = self.data
		
		quantity_df = (self.budget_per_frequency*self.weight.iloc[0]/data[data[M.REBALANCING_DATE]])[self.weight.columns]		
		quantity_df,data = adding_quantity(data, quantity_df)

		adding_cash(data, self.budget_per_frequency)
		adding_pnl(data,quantity_df)

		self.data = data

