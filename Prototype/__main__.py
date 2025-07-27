from argparse import ArgumentParser
from datetime import datetime 
from Module.yahoo_finance.client import Yahoo_Client 
from instrument import create_folder
from risk_free_rate import Risk_Free_Rate

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
	default = "01Jan1990",
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

start_date = datetime.strptime(args.start, "%d%b%Y")
end_date = datetime.strptime(args.end, "%d%b%Y") if args.end != None else datetime.now() 
if args.source == 'yahoo': 
	client = Yahoo_Client(args.ticker, start_date, end_date)
if args.action == 'volatility_surface':
	ir_client = Yahoo_Client("SR1=F", end_date,end_date)
	r = Risk_Free_Rate.SOFR(ir_client.fetch()['CLOSE'])
	print(r)
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
	filename = f'{args.ticker}_{args.action}_{start}-{end}_{args.source}'
	data.to_csv(f'{folder_output}/{filename}.csv')

