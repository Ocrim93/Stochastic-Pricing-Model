from argparse import ArgumentParser
from .instrument import formatting_input,retrieve_ticker_from_csv
from .action import Action

parser = ArgumentParser()

parser.add_argument(
	"-a",
	"--action",
	required = True,
	action="store",
	help = "action such as volatility_surface, financials, price"
	)
parser.add_argument(
	"-t",
	"--ticker",
	required = False,
	action="store",
	help = "ticker symbol for Yahoo Finance source"
	)

parser.add_argument(
	"-s",
	"--start_date",
	required = False,
	action="store",
	help = "start business date for yahoo finance source, format: %d/%m/%y"
	)

parser.add_argument(
	"-e",
	"--end_date",
	required = False,
	action="store",
	help = "end business date for yahoo finance source, format: %d/%m/%y"
	)

parser.add_argument(
	"--currency",
	required = False,
	default = "USD",
	action="store",
	help = "FX reporting currency "
	)

parser.add_argument(
	"-f",
	"--frequency",
	required = False,
	default = "B",
	action="store",
	help = "time frequency of retrieving data "
	)

parser.add_argument(
	"--source",
	required = False,
	default = "yahoo",
	action="store",
	help = "source. choice between yahoo"
	)

parser.add_argument(
	"-o",
	"--output",
	required = False,
	action="store",
	default = './Output',
	help = "output folder path"
	)

parser.add_argument(
	"--save",
	required = False,
	action="store_true",
	default = True,
	help = "saving Flag"
	)

parser.add_argument(
	"--plot",
	required = False,
	action="store_true",
	default = False,
	help = "plotting Flag"
	)

args = parser.parse_args()

retrieve_ticker_from_csv()
action = Action(formatting_input(args))







