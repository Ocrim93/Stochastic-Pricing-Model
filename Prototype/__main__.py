from argparse import ArgumentParser
from datetime import datetime 
from module.yahoo_finance.client import Yahoo_Client 
from instrument import create_folder, business_date
from risk_free_rate import Risk_Free_Rate
from volatility_surface import Volatility_Surface
from loguru import logger

parser = ArgumentParser()

parser.add_argument(
	"-t",
	"--ticker",
	required = True,
	action="store",
	help = "ticker symbol for Yahoo Finance source"
	)

parser.add_argument(
	"-a",
	"--action",
	required = True,
	action="store",
	help = "Action such as volatility_surface, financials, price"
	)

parser.add_argument(
	"-s",
	"--start",
	required = False,
	action="store",
	help = "Start Business date for Yahoo Finance source, format: %d%b%y"
	)

parser.add_argument(
	"-e",
	"--end",
	required = False,
	action="store",
	help = "End Business date for Yahoo Finance source"
	)

parser.add_argument(
	"--source",
	required = False,
	default = "yahoo",
	action="store",
	help = "Source. Choice between yahoo"
	)

parser.add_argument(
	"-o",
	"--output",
	required = False,
	action="store",
	default = './Output',
	help = "Output folder path"
	)

parser.add_argument(
	"--save",
	required = False,
	action="store",
	default = False,
	help = "Saving Flag"
	)

args = parser.parse_args()

ticker = args.ticker
start_date = datetime.strptime(args.start, "%d%b%Y") if args.start != None else datetime.now() 
end_date = datetime.strptime(args.end, "%d%b%Y") if args.end != None else datetime.now() 

start_date = business_date(start_date)
end_date = business_date(end_date)
logger.info(f'start_date : {start_date} ')
logger.info(f'end_date : {end_date} ')

if args.source == 'yahoo': 
	client = Yahoo_Client(ticker, start_date, end_date)

if args.action == 'volatility_surface':
	options = client.fetch_options()
	spot_price = client.fetch_current_price()
	
	ir_client = Yahoo_Client("SR1=F", start_date, end_date)
	risk_free_rate =  Risk_Free_Rate.SOFR(ir_client.fetch_current_price())
	dividend = client.fetch_dividend_yield()

	vol = Volatility_Surface( ticker,
				 			  options, 
				 			  start_date.strftime('%d-%m-%Y'),
				 			  spot_price,
				 			  risk_free_rate,
				 			  dividend)
	vol.run()

if args.action == 'financials':
	data = client.fetch_financials()

if args.action == 'price':
	data = client.fetch()
print(data)
if args.save :
	start = datetime.strftime(start_date,"%d%b%Y")
	end = datetime.strftime(end_date,"%d%b%Y")
	folder_output = f'{args.output}/{args.ticker}'
	create_folder(folder_output)
	filename = f'{ticker}_{args.action}_{start}-{end}_{args.source}'
	data.to_csv(f'{folder_output}/{filename}.csv')

