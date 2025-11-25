import pandas as pd
import numpy as np
from scipy.optimize import minimize
from prototype.measure import Measure as M
from loguru import logger


def log_pct_dataset(data : pd.DataFrame, assets : list ):
	log_pct_df = pd.DataFrame()
	for asset in assets:
		log_pct_df[asset] = np.log(data[asset].shift(-1)/data[asset])
		log_pct_df[asset] = log_pct_df[asset].dropna()
	return log_pct_df

class Efficient_Frontier():

	@staticmethod
	def portfolio_stats(weights : np.array, mu : np.array, cov : pd.DataFrame ):
		portfolio_return = np.dot(weights,mu)
		portfolio_vol = np.sqrt(np.dot(weights.T,np.dot(cov,weights)))

		return portfolio_return,portfolio_vol

	@staticmethod
	def minimize_vol(target_return: float, mu : np.array, cov : pd.DataFrame):
		n = len(mu)
		init_w = np.ones(n)/n

		constraints = (
			{"type": "eq" , "fun" : lambda w : np.sum(w)-1},
			{"type" : "eq" , "fun" : lambda w : np.dot(w,mu) - target_return}
			)
		bounds = tuple((-1,1) for _ in range(n))

		result = minimize(
					lambda w : Efficient_Frontier.portfolio_stats(w,mu,cov)[1],
					init_w,
					method = "SLSQP",
					bounds = bounds,
					constraints=constraints
			)
		return result

	def __init__(self, target_return : float,
					   cov : pd.DataFrame,
					   mu : np.array,
					   asset_names : list):

		self.target_return = np.linspace(min(mu),target_return,50)
		self.cov = cov
		self.mu = mu
		self.columns =  [M.PORTFOLIO_RETURN,M.PORTFOLIO_VOL] + asset_names
		self.data = pd.DataFrame(data = {col : [] for col in self.columns })

	def run(self):
		for r in self.target_return:
			result = Efficient_Frontier.minimize_vol(r,self.mu,self.cov)
			if result.success:
				portfolio_return,portfolio_vol = Efficient_Frontier.portfolio_stats(result.x,self.mu,self.cov)
				self.data.loc[len(self.data)] = [portfolio_return,portfolio_vol] + list(result.x)
			else:
				logger.warning(f' scipy.optimize.minimize failed for target {r}')

