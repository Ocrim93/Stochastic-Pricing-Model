from loguru import logger
import pandas as pd
import numpy as np
from .instrument import create_folder,cleaning_data,business_date,build_business_dates_dataset
from .plot_lib import create_figure
from .measure import Measure as M
from .source.yahoo_finance.client import Yahoo_Client
from plotly.offline import  iplot


class Action():

	@staticmethod
	def get_client(ticker, start_date, end_date, source,**kwargs ):
		if source == 'yahoo':
			return Yahoo_Client( ticker, start_date , end_date, **kwargs)
		logger.warning(f'no source found : {source}')

	def __init__(self, args : dict ):
		method = getattr(self,args['action'])
		args['start_date'] = business_date(args['start_date'])
		args['end_date'] = business_date(args['end_date'])
		logger.info(f"star_date : {args['start_date'].date()} end_date : {args['end_date'].date()} ")
		
		self.args = args
		self.folder_output = f'{args["output"]}/{args["action"]}/{args["ticker"]}'
		self.filename = f"{args['ticker']}_({self.args['currency']})_{args['start_date'].date()}_{args['end_date'].date()	}_{args['frequency']}_{args['source']}"
		
		create_folder(self.folder_output)
		method()

	def _client(self):
		return Action.get_client(self.args['ticker'], self.args['start_date'], self.args['end_date'],self.args['source'])

	def price(self):
		client = self._client()
		data = client.fetch_price()[[M.DATE,M.CLOSE]]
		currency = client.fetch_currency()
		
		if currency == self.args['currency']:
			fx_df = build_business_dates_dataset(self.args['start_date'],self.args['end_date'])
			fx_df[M.FX_SPOT] = np.full(len(fx_df),1)
		else:
			fx_df = Action.get_client(f"{self.args['currency']}{currency}",
										self.args['start_date'],
										self.args['end_date'],
										self.args['source'],
										FX_flag = True).fetch_price()[[M.DATE,M.CLOSE]]
			fx_df = fx_df.rename(columns = {M.CLOSE:M.FX_SPOT})

		logger.info(f'start cleaning data for {self.args["ticker"]}')
		data = cleaning_data(data,columns = [M.CLOSE], frequency = self.args['frequency'])
		logger.info(f'start cleaning data for FX_SPOT')
		fx_df = cleaning_data(fx_df,columns = [M.FX_SPOT], frequency = self.args['frequency'])

		data = data.merge(fx_df, how = 'inner', on = M.DATE)
		data[M.CLOSE_FX] = data[M.CLOSE]*data[M.FX_SPOT]

		data[M.PCT_CHANGE] = data[M.CLOSE_FX].pct_change(fill_method=None)*100
		fig_title = ' '.join(self.filename.split('_'))
		price_fig = create_figure(data,f"{fig_title} {M.CLOSE} ({self.args['currency']})",  M.DATE, M.CLOSE) 
		pct_fig = create_figure(data,f"{fig_title} {M.PCT_CHANGE}",  M.DATE,M.PCT_CHANGE,) 
		
		if self.args['save']: 
			self.save_data(data)
			self.save_plot(price_fig, PLOT=self.args['plot'])
			self.save_plot(pct_fig, PLOT=self.args['plot'])


	def financials(self):
		client = self._client()
		data = client.fetch_financials()
		
		if self.args['save'] : 
			self.save_data(data)

	def portfolio(self):
		io = 'prototype/portfolio_settings.yaml'
		with open(io, "r") as file:
			config = yaml.safe_load(file)

		# settings args 
		
		#portfolio = Portfolio()
		#portfolio.fetch_data()	
		#if self.args.save : self.save(data)

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

	def save_data(self, data : pd.DataFrame,):
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

