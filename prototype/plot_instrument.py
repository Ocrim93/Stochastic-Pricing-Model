import pandas as pd
from .measure import Measure as M
from .plot_lib import create_figure, create_candlestick, adding_line, create_multiple_axes_figure,adding_vertical_line
from .instrument import datetime_to_timestamp
from datetime import datetime

class Plot:

	@staticmethod
	def price(data : pd.DataFrame, filename : str):
		fig_title = ' '.join(filename.split('_'))
	
		price_fig = create_candlestick(data,f"{fig_title}",M.DATE, M.CLOSE)
		price_fig = adding_line(price_fig, data, M.CLOSE, M.DATE,M.CLOSE)
	
		pct_fig = create_figure(data,f"{fig_title}",M.DATE,M.LOG_PCT)

		return price_fig,pct_fig

	@staticmethod
	def pair(data : pd.DataFrame, filename : str):
		fig_title = ' '.join(filename.split('_'))
	
		price_fig = create_figure(data,f"{fig_title}",M.DATE, M.CLOSE)
	
		pct_fig = create_figure(data,f"{fig_title}",M.DATE,M.LOG_PCT)

		return price_fig,pct_fig
	
	@staticmethod
	def portfolio(data : pd.DataFrame, weight_map : dict,  starting_date : datetime, filename : str ):
		
		starting_strategy_date = datetime_to_timestamp(starting_date)
		fig_title = ' '.join(filename.split('_'))
		
		pnl_fig = create_multiple_axes_figure(data,
											  fig_title+' PnL',
											  M.DATE,
											  [M.CASH,M.PnL,M.BALANCE],
											  M.PnL)
		pnl_fig = adding_vertical_line(pnl_fig,starting_strategy_date, 'starting')
		
		asset_fig = create_multiple_axes_figure(data,
												fig_title + ' Asset',
												M.DATE,
												weight_map,
												M.INDEX)
		asset_fig = adding_vertical_line(asset_fig,starting_strategy_date,'starting')

		return asset_fig, pnl_fig
	
	def __init__(self):
		pass
