import pandas as pd
from prototype.measure import Measure as M


def build_dataframe(values : list):
	dates = []
	ir = []
	for v in values:
		dates.append(v['date'])
		ir.append(float(v['value']))

	df = pd.DataFrame(data = { M.DATE : dates, M.CLOSE : ir })
	df[M.DATE] = pd.to_datetime(df[M.DATE], format='%Y-%m-%d')
	df.sort_values(by = M.DATE, ignore_index=True, ascending = True, inplace = True)

	return df

def last_price_and_date(data: pd.DataFrame):
	data = data.sort_values(by = M.DATE, ascending = False)
	closing_price = data[M.CLOSE].values[0]
	current_date = data[M.DATE].values[0]
	return closing_price,current_date