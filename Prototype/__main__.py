from argparse import ArgumentParser
from datetime import datetime 
from Module.yahoo_finance.client import Client 

parser = ArgumentParser()
parser.add_argument(
	"-t",
	"--ticker",
	required = True,
	action="store",
	help = "ticker symbol for Yahoo Finance source"
	)

parser.add_argument(
	"-s",
	"--start",
	required = True,
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
	"-o",
	"--output",
	required = False,
	action="store",
	default = './Output',
	help = "Output folder path"
	)

args = parser.parse_args()

start_date = datetime.strptime(args.start, "%d%b%y")
end_date = datetime.strptime(args.end, "%d%b%y") if args.end != None else None 
