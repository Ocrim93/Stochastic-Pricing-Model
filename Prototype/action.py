from __future__ import annotations
from loguru import logger
from .instrument import create_folder,cleaning_data,business_date,build_business_dates_dataset,applying_fx_spot,compute_pct_change, datetime_to_timestamp
from .plot_lib import create_figure, create_candlestick, adding_line, create_multiple_axes_figure,adding_vertical_line
from .measure import Measure as M
from .source.yahoo_finance.client import Yahoo_Client
from plotly.offline import  iplot
from prototype.portfolio_simulation.portfolio import Portfolio 
import yaml


class Action():

	@staticmethod
	def get_client(ticker, start_date, end_date, source,**kwargs ):
		if source == 'yahoo':
			return Yahoo_Client( ticker, start_date , end_date, **kwargs)
		logger.warning(f'no source found : {source}')

	@staticmethod
	def get_price(ticker,
				  start_date,
				  end_date,
				  source,
				  reporting_currency,
				  frequency, 
				  columns
				  ):

		client = Action.get_client(ticker, start_date, end_date, source)

		data = client.fetch_price()
		ticker_currency = client.fetch_currency()

		if ticker_currency != reporting_currency:
			fx_df = Action.get_client(f"{ticker_currency}{reporting_currency}",
										start_date,
										end_date,
										source,
										FX_flag = True).fetch_price()

		logger.info(f'start cleaning data for {ticker}')
		data = cleaning_data(data,columns = columns, frequency=frequency)
		if ticker_currency != reporting_currency:
			logger.info(f'start cleaning data for FX_SPOT')
			fx_df = cleaning_data(fx_df, columns = [M.CLOSE,M.OPEN,M.LOW,M.HIGH], drop_columns = [M.VOLUME], frequency = frequency)
			data = applying_fx_spot(data, fx_df, columns = [col for col in columns if col != M.VOLUME])
		
		return data[[M.DATE]+columns]

	def __init__(self, args : dict ):
		method = getattr(self,args['action'])
		args['start_date'] = business_date(args['start_date'])
		args['end_date'] = business_date(args['end_date'])
		logger.info(f"star_date : {args['start_date'].date()} end_date : {args['end_date'].date()} ")
		
		self.args = args
		self.base_folder_output = f'{args["output"]}/{args["action"]}'
		method()

	def _client(self):
		return Action.get_client(self.args['ticker'], self.args['start_date'], self.args['end_date'],self.args['source'])

	def _price(self, columns : list):
		return Action.get_price( self.args['ticker'], 
							     self.args['start_date'],
							     self.args['end_date'],
							     self.args['source'],
							     self.args['currency'],
							     self.args['frequency'],
							     columns)

	def price(self):
		self.folder_output = f'{self.base_folder_output}/{self.args["ticker"]}'
		self.filename = f"{self.args['ticker']}_({self.args['currency']})_ \
						 {self.args['start_date'].date()}_\
						 {self.args['end_date'].date()}_\
						 {self.args['frequency']}_{args['source']}"

		data = self._price(columns = [M.CLOSE,M.OPEN,M.LOW,M.HIGH,M.VOLUME])
		
		compute_pct_change(data, M.CLOSE, self.args['frequency'])

		
		if self.args['save']: 
			fig_title = ' '.join(self.filename.split('_'))
			price_fig = create_candlestick(data,f"{fig_title}",M.DATE, M.CLOSE)
			price_fig = adding_line(price_fig, data, M.CLOSE, M.DATE,M.CLOSE)
			pct_fig = create_figure(data,f"{fig_title}",M.DATE,M.LOG_PCT) 
			
			self.save_data(data)
			self.save_plot(price_fig, PLOT=self.args['plot'])
			self.save_plot(pct_fig, PLOT=self.args['plot'])


	def financials(self):
		self.folder_output = f'{self.base_folder_output}/{self.args["ticker"]}'
		self.filename = f"{args['ticker']}_{args['source']}"

		client = self._client()
		data = client.fetch_financials()
		
		if self.args['save'] : 
			self.save_data(data)

	def portfolio(self):
		with open(self.args['portfolio_io'], "r") as file:
			config = yaml.safe_load(file)
		budget = config['budget'] or 0
		budget_per_frequency = config['budget_per_frequency'] or 0
		frequency = config['frequency'] 

		self.args['frequency'] = 'B'

		df_map = {}
		weight_map = {}
		for asset in config['asset']:
			if asset['weight'] == 0 :
				continue
			self.args['ticker'] = asset['name']
			self.args['source'] = asset['source']

			
			df_map[asset['name']] = self._price([M.CLOSE])
			weight_map[asset['name']] = asset['weight'] if  asset['weight'] != None else 1/len(config['asset'])

		portfolio = Portfolio( df_map,
				   weight_map,
				   self.args['start_date'],
				   self.args['end_date'],
				   frequency,
				   budget,
				   budget_per_frequency)

		self.filename = '_'.join(weight_map)
		self.folder_output = f'{self.base_folder_output}/{self.filename}'

		starting_strategy_date = portfolio.data.loc[portfolio.data[M.REBALANCING_DATE],M.DATE].values[0]
		starting_strategy_date = datetime_to_timestamp(starting_strategy_date)
	
		if self.args['save'] : 
			self.save_data(portfolio.data)

			fig_title = ' '.join(self.filename.split('_'))
			pnl_fig = create_multiple_axes_figure(portfolio.data,
												  fig_title+' PnL',
												  M.DATE,
												  [M.CASH,M.PnL,M.BALANCE],
												  M.PnL)
			pnl_fig = adding_vertical_line(pnl_fig,starting_strategy_date, 'starting')
			asset_fig = create_multiple_axes_figure(portfolio.data,
												  fig_title + ' Asset',
												  M.DATE,
												  weight_map,
												  M.INDEX)
			asset_fig = adding_vertical_line(asset_fig,starting_strategy_date,'starting')
			self.save_plot(pnl_fig, PLOT=self.args['plot'])
			self.save_plot(asset_fig, PLOT=self.args['plot'])


	def volatility_surface(self):
		client = self._client()
		options = client.fetch_options()
		spot_price = client.fetch_current_price()
	
		ir_client = client(Ticker.SOFR, start_date, end_date)
		risk_free_rate =  Risk_Free_Rate.SOFR(ir_client.fetch_current_price())
		dividend = client.fetch_dividend_yield()

		vol = Volatility_Surface( ticker,
					 			  options, 
					 			  start_date,
					 			  spot_price,
					 			  risk_free_rate,
					 			  dividend)
		vol.run()

	def save_data(self, data ):
		create_folder(self.folder_output)
		if data.empty:
			logger.warning(f'not saved empty, {self.filename}')
		else:
			logger.info(f'saving data {self.filename}')
			data.to_csv(f'{self.folder_output}/{self.filename}.csv')

	def save_plot(self,figure, extension = 'html', PLOT = False):
		filename = figure.layout['title']['text'].replace(' ', '_')
		if PLOT:
			logger.info(f'plotting data {filename}')
			iplot(figure)
		logger.info(f'save plot {filename}')
		figure.write_html(f'{self.folder_output}/{filename}.{extension}')

