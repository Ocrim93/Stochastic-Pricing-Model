from loguru import logger
import pandas as pd
from .instrument import create_folder,cleaning_data,business_date
from .plot_lib import create_figure
from .measure import Measure as M
from .source.yahoo_finance.client import Yahoo_Client
from plotly.offline import  iplot

class Action():

	def __init__(self, args : dict ):
		method = getattr(self,args['action'])
		args['start_date'] = business_date(args['start_date'])
		args['end_date'] = business_date(args['end_date'])
		logger.info(f"star_date : {args['start_date'].date()} end_date : {args['end_date'].date()} ")
		
		self.args = args
		self.folder_output = f'{args["output"]}/{args["action"]}/{args["ticker"]}'
		self.filename = f"{args['ticker']}_{args['start_date'].date()}.{args['end_date'].date()	}_{args['frequency']}_{args['source']}"
		create_folder(self.folder_output)
		method()

	def get_client(self):
		if self.args['source'] == 'yahoo': 
			return Yahoo_Client(self.args['ticker'], self.args['start_date'], self.args['end_date'])
		logger.warning(f'no source found : {self.args.source}')

	def price(self):
		client = self.get_client()
		data = client.fetch()

		data = cleaning_data(data,columns = [M.CLOSE], freq = self.args['frequency'])
		data[M.PCT_CHANGE] = data[M.CLOSE].pct_change()*100
		
		fig_title = self.filename
		price_fig = create_figure(data,f"{fig_title}_{M.CLOSE}",  M.DATE, M.CLOSE) 
		pct_fig = create_figure(data,f"{fig_title}_{M.PCT_CHANGE}",  M.DATE,M.PCT_CHANGE,) 
		
		if self.args['save']: 
			self.save_data(data)
			self.save_plot(price_fig, PLOT=self.args['plot'])
			self.save_plot(pct_fig, PLOT=self.args['plot'])


	def financials(self):
		client = self.get_client()
		data = client.fetch_financials()
		
		if self.args['save'] : 
			self.save_data(data)

	def portfolio(self):
		pass
		#portfolio = Portfolio()
		#portfolio.fetch_data()	
		#if self.args.save : self.save(data)

	def volatility_surface(self):
		client = self.get_client()
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

