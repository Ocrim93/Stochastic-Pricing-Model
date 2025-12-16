from __future__ import annotations
from loguru import logger
from .instrument import create_folder,cleaning_data,build_business_dates_dataset,applying_fx_spot,compute_pct_change,build_pair_dataset
from .plotInstrument import Plot
from .measure import Measure as M
from .source.yahoo_finance.client import YahooClient
from plotly.offline import  iplot
from prototype.portfolio_simulation.portfolio import Portfolio
from prototype.volatility_surface.volatilitySurface import VolatilitySurface
from .interestRate import RiskFreeRate, Treasury
from .timeHelper import  TimeHelper 
import yaml

class Action():

	@staticmethod
	def get_client(ticker, start_date, end_date, source, FX_flag = False, **kwargs ):
		if source == 'yahoo':
			return YahooClient( ticker, start_date , end_date, FX_flag, **kwargs)
		logger.warning(f'no source found : {source}')

	@staticmethod
	def get_current_price(ticker, source, **kwargs):
		client = Action.get_client(ticker, TimeHelper.business_date(), TimeHelper.business_date(), source)
		return client.fetch_current_price()

	@staticmethod
	def get_price(ticker,
				  start_date,
				  end_date,
				  source,
				  reporting_currency,
				  frequency, 
				  columns,
				  FX_flag,
				  **kwargs
				  ):

		client = Action.get_client(ticker, start_date, end_date, source, FX_flag, **kwargs)

		data = client.fetch_price()
		ticker_currency = client.fetch_currency()

		if ticker_currency != reporting_currency:
			fx_df = Action.get_client(f"{ticker_currency}{reporting_currency}",
										start_date,
										end_date,
										source,
										FX_flag = True).fetch_price()

		logger.info(f'start cleaning data for {ticker}')
		data = cleaning_data(data, start_date, end_date, columns = columns, frequency=frequency)
		if ticker_currency != reporting_currency:
			logger.info(f'start cleaning data for FX_SPOT')
			fx_df = cleaning_data(fx_df, start_date, end_date, columns = [M.CLOSE,M.OPEN,M.LOW,M.HIGH], drop_columns = [M.VOLUME], frequency = frequency)
			data = applying_fx_spot(data, fx_df, columns = [col for col in columns if col != M.VOLUME])
		
		return data[[M.DATE]+columns]

	def __init__(self, args : dict ):
		method = getattr(self,args['action'])

		args['start_date'] = TimeHelper.business_date(args['start_date'])
		args['end_date'] = TimeHelper.business_date(args['end_date'])
			
		logger.info(f"star_date : {args['start_date'].date()} end_date : {args['end_date'].date()} ")
		
		self.args = args
		self.base_folder_output = f'{args["output"]}/{args["action"]}'
		method()

	def _client(self):
		return Action.get_client(self.args['ticker'], self.args['start_date'], self.args['end_date'],self.args['source'])

	def _price(self, columns : list, FX_flag : bool = False, **kwargs ):
		return Action.get_price( self.args['ticker'], 
							     self.args['start_date'],
							     self.args['end_date'],
							     self.args['source'],
							     self.args['currency'],
							     self.args['frequency'],
							     columns,
							     FX_flag,
								 **kwargs)

	def price(self):
		if 'FX_' in self.args['ticker']:
			self.args['ticker'] =  self.args['ticker'].split('_')[1]
			self.args['currency'] = self.args['ticker'][3:]
			FX_flag = True
		else:
			FX_flag = False
			
		self.folder_output = f'{self.base_folder_output}/{self.args["ticker"]}'
		self.filename = f"{self.args['ticker']}_({self.args['currency']})_"+\
						f"{self.args['start_date'].date()}_"+\
						f"{self.args['end_date'].date()}_"+\
						f"{self.args['frequency']}_{self.args['source']}"

		data = self._price(columns = [M.CLOSE,M.OPEN,M.LOW,M.HIGH,M.VOLUME], FX_flag = FX_flag)
		
		compute_pct_change(data, M.CLOSE, self.args['frequency'])

		if self.args['save']:
			price_fig,pct_fig =  Plot.price(data,self.filename) 
			
			self.save_data(data)
			self.save_plot(price_fig, PLOT=self.args['plot'])
			self.save_plot(pct_fig, PLOT=self.args['plot'])

	def pair(self):
		self.folder_output = f'{self.base_folder_output}/{self.args["ticker"]}'
		self.filename = f"{self.args['ticker']}_"+\
						f"{self.args['start_date'].date()}_"+\
						f"{self.args['end_date'].date()}_"+\
						f"{self.args['frequency']}_{self.args['source']}"

		asset_num = self.args['ticker'].split('-')[0]
		asset_den = self.args['ticker'].split('-')[1]

		self.args['ticker'] = asset_num
		data_num = self._price(columns = [M.CLOSE])
		self.args['ticker'] = asset_den
		data_den = self._price(columns = [M.CLOSE])
		
		data = build_pair_dataset(data_num,data_den)
		compute_pct_change(data, M.CLOSE, self.args['frequency'])

		if self.args['save']:
			price_fig,pct_fig =  Plot.pair(data,self.filename) 
			
			self.save_data(data)
			self.save_plot(price_fig, PLOT=self.args['plot'])
			self.save_plot(pct_fig, PLOT=self.args['plot'])


	def financials(self):
		self.folder_output = f'{self.base_folder_output}/{self.args["ticker"]}'
		self.filename = f"{self.args['ticker']}_{self.args['source']}"

		client = self._client()
		data = client.fetch_financials()
		
		if self.args['save'] : 
			self.save_data(data)

	def portfolio(self):
		with open(self.args['portfolio_io'], "r") as file:
			config = yaml.safe_load(file)
		budget = config['budget'] or 0
		budget_per_frequency = config['budget_per_frequency'] or 0
		risk_free_rate_source = config['risk_free_rate_source']
		frequency = config['frequency'] 
		target_portfolio_return = config['target_portfolio_return']

		self.args['frequency'] = 'B'
		reporting_currency = self.args['currency']

		df_map = {}
		weight_map = {}
		for asset in config['asset']:
			if asset['weight'] == 0 :
				continue
			self.args['ticker'] = asset['name']
			self.args['source'] = asset['source']

			
			df_map[asset['name']] = self._price([M.CLOSE])
			weight_map[asset['name']] = asset['weight'] if  asset['weight'] != None else 1/len(config['asset'])

		risk_free_rate = RiskFreeRate(reporting_currency)
		risk_free_rate_price =  Action.get_current_price(risk_free_rate.name,risk_free_rate_source)
								
		portfolio = Portfolio( df_map,
							   weight_map,
							   self.args['start_date'],
							   self.args['end_date'],
							   frequency,
							   risk_free_rate.value(risk_free_rate_price),
							   target_portfolio_return,
							   budget,
							   budget_per_frequency)

		self.filename = f"{'_'.join(weight_map)}_({reporting_currency})"
		self.folder_output = f'{self.base_folder_output}/{self.filename}'

		if self.args['save'] : 
			self.save_data(portfolio.data)
			self.save_data(portfolio.efficient_frontier_data,'Efficient_Frontier')

			asset_fig, pnl_fig = Plot.portfolio(portfolio.data, weight_map, portfolio.starting_date, self.filename)
			self.save_plot(asset_fig, PLOT=self.args['plot'])
			self.save_plot(pnl_fig, PLOT=self.args['plot'])


	def volatility_surface(self):
		
		self.args['start_date'] = TimeHelper.business_date()
		self.args['end_date'] = TimeHelper.business_date()

		self.folder_output = f'{self.base_folder_output}/{self.args["ticker"]}/{self.args["start_date"].date()}'
		self.filename = f"{self.args['ticker']}_{self.args['source']}"
		
		client = self._client()
		options = client.fetch_options()
		
		spot_price = client.fetch_current_price()
		ticker_currency = client.fetch_currency()
		
		risk_free_rate = RiskFreeRate(ticker_currency)
		risk_free_rate_price =  Action.get_current_price(risk_free_rate.name,self.args['source'])
		r = risk_free_rate.value(risk_free_rate_price)

		risk_free_rate = Treasury(ticker_currency)
		risk_free_rate_price =  Action.get_current_price(risk_free_rate.name,self.args['source'])
		r = risk_free_rate.value(risk_free_rate_price)

		dividend = client.fetch_dividend_yield()
		
		vol = VolatilitySurface( self.args['ticker'],
					 			 options, 
					 			 TimeHelper.change_date_formatting(self.args['start_date'],'','%d/%m/%Y'),
					 			 spot_price,
					 			 r,
					 			 dividend)
		vol.run()
		if self.args['save']:
			for call_put in vol.IV_data:
				self.save_data(vol.IV_data[call_put], name = call_put)

	def save_data(self,data , name: str = '' ):
		create_folder(self.folder_output)
		if data.empty:
			logger.warning(f'empty data, not saved, {self.filename}_{name}')
		else:
			logger.info(f'saving data {self.filename} {name}')
			data.to_csv(f'{self.folder_output}/{self.filename}_{name}.csv')

	def save_plot(self,figure, extension = 'html', PLOT = False):
		filename = figure.layout['title']['text'].replace(' ', '_')
		if PLOT:
			logger.info(f'plotting data {filename}')
			iplot(figure)
		logger.info(f'save plot {filename}')
		figure.write_html(f'{self.folder_output}/{filename}.{extension}')

