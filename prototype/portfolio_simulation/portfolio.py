from .instrument import extract_dataset,extract_weight_dataset,rebalancing_dates,adding_quantity,adding_cash,adding_pnl,compute_sharpe_ratio
from .efficientFrontier import log_pct_dataset, EfficientFrontier
from loguru import logger
from prototype.measure import Measure as M
import datetime as dt
from prototype.timeHelper import TimeHelper


class Portfolio	:

	def __init__( self, 
				  data_map : dict, 
				  weight_map : dict,
				  start_date : dt.datetime,
				  end_date : dt.datetime,
				  frequency : str, 
				  risk_free_rate : float,
				  target_portfolio_return : float = 0.2,
				  budget : float = 0 ,
				  budget_per_frequency : float = 0
				  ):

		self.data = extract_dataset(data_map)
		self.weight = extract_weight_dataset(weight_map)
		self.base = 1 
		self.frequency = frequency
		self.risk_free_rate = risk_free_rate
		self.target_portfolio_return = target_portfolio_return
		self.rate_of_return,self.volatility,self.sharpe_ratio = 0,0,0
		
		rebalancing_dates(start_date, end_date, frequency, self.data)
		self.starting_date = self.data[self.data[M.REBALANCING_DATE]].index[0]
		self.efficient_frontier()
		
		self.budget_per_frequency  =  budget/len(self.data[self.data[M.REBALANCING_DATE]]) if (budget_per_frequency == 0) else budget_per_frequency
		self.budget = self.budget_per_frequency*len(self.data[self.data[M.REBALANCING_DATE]]) 
		
		self.build_index()
		self.startegy()
		self.compute_sharpe_ratio()		
		
		self.investing_everything_at_t0()

		self.data.reset_index(inplace = True)

	def efficient_frontier(self):
		logger.info('compute capital market line')
		df = log_pct_dataset(self.data.copy(), self.weight.columns)
		cov = df.cov()/TimeHelper.time_conversion('trading', 'B')
		mean = df.mean()/TimeHelper.time_conversion('trading','B')
		eff_front = EfficientFrontier(self.target_portfolio_return,cov,mean,list(self.weight.columns))
		eff_front.run()

		self.efficient_frontier_data = eff_front.data

	def compute_sharpe_ratio(self):
		statistics_data = self.data[self.data.index >= self.starting_date]
		balance = statistics_data.iloc[-1][M.BALANCE]
		PnL = statistics_data.iloc[-1][M.PnL]

		self.rate_of_return,self.volatility,self.sharpe_ratio = compute_sharpe_ratio(statistics_data, self.risk_free_rate)
		
		logger.info(f'cash invested : {self.budget:.2f} | balance : {balance:.2f} | {M.PnL} : {PnL:.2f}')
		logger.info(f'average rate of return  {self.rate_of_return*100:0.3f} % | volatility : {self.volatility*100:.2f} %')
		logger.info(f'sharpe_ratio {self.sharpe_ratio:0.3f} | risk_free_rate : {self.risk_free_rate*100:.2f} %')

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
		self.data[M.INDEX] = (self.data*self.weight.iloc[0]).sum(axis=1)

	def fixed_share_index(self):
		logger.info('computing fixed-share index') 
		base = self.compute_base()
		initial_prices = self.weight.iloc[0]/self.data.iloc[0]

		self.data[M.FIXED_SHARE_INDEX] = base*(self.data*initial_prices).sum(axis=1)

	def build_index(self):
		self.fixed_share_index()
		self.weighted_price_index()
		self.data = self.data.astype({ M.FIXED_SHARE_INDEX : "float64",
									   M.INDEX : "float64"})

	def investing_everything_at_t0(self):
		logger.info(f'investing all at time {self.starting_date}')

		quantity_df = self.budget*self.weight.iloc[0]/self.data.loc[self.starting_date][self.weight.columns]
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

