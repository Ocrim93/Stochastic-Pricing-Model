from datetime import datetime, timedelta


LIST_SYMBOL = ['F','G','H','J','K','M','N','Q','U','V','X','Z']

def get_map_month_symbol(reverse = False ):
	if reverse:
		map_month_symbol = {  symbol : idx+1  for idx,symbol in  enumerate(LIST_SYMBOL)}
	else:
		map_month_symbol = { idx+1 : symbol for idx,symbol in  enumerate(LIST_SYMBOL)}
	return map_month_symbol

def expiration_in_year(date1 : datetime,
					   date2 : datetime,
					   formatting :str = '%d/%m/%Y',
					   convention : str = 'trading_days' ) -> float :
	date1 = datetime.strptime(date1, formatting)
	date2 = datetime.strptime(date2, formatting)
	days = (date2 - date1).days
	if convention == 'actual':
		y = days/360
	if convention == 'trading_days':
		y = days/252

	return y
