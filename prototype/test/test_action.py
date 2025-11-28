from prototype.instrument import retrieve_ticker_from_csv
from prototype.action import Action
import pytest 

retrieve_ticker_from_csv()

base_args = {'action' : None,
		'ticker' : None,
		'start_date' : '01/04/2020',
		'end_date' :  '01/04/2025',
		'currency' : None,
		'frequency' : None,
		'source' : 'yahoo',
		'output' : None,
		'portfolio_io' : 'prototype/test/test_portfolio_settings.yaml',
		'save' : False,
		'plot' : False 
		}

def test_price():
	args = base_args.copy()
	args['action'] = 'price'
	args['ticker'] = 'SX5E'
	args['currency'] = 'EUR'
	args['frequency'] = 'B'
	try:
		Action(args)
	except Exception as e:
		pytest.fail(f"Unexpected exception raised: {e}")

def test_price_FX():
	args = base_args.copy()
	args['action'] = 'price'
	args['ticker'] = 'FX_EURUSD'
	args['frequency'] = 'B'
	try:
		Action(args)
	except Exception as e:
		pytest.fail(f"Unexpected exception raised: {e}")

def test_portfolio():
	args = base_args.copy()
	args['action'] = 'portfolio'
	args['currency'] = 'EUR'

	try:
		Action(args)
	except Exception as e:
		pytest.fail(f"Unexpected exception raised: {e}")

def test_financials():
	args = base_args.copy()
	args['action'] = 'financials'
	args['ticker'] = 'AAPL'

	try:
		Action(args)
	except Exception as e:
		pytest.fail(f"Unexpected exception raised: {e}")

def test_pair():
	args = base_args.copy()
	args['action'] = 'pair'
	args['ticker'] = 'SX5E-GC'
	args['currency'] = 'EUR'
	args['frequency'] = 'B'

	try:
		Action(args)
	except Exception as e:
		pytest.fail(f"Unexpected exception raised: {e}")

def test_volatility_surface():
	args = base_args.copy()
	args['action'] = 'volatility_surface'
	args['ticker'] = 'AAPL'

	try:
		Action(args)
	except Exception as e:
		pytest.fail(f"Unexpected exception raised: {e}")



		