from datetime import datetime
import pandas as pd
from prototype.portfolio_simulation.portfolio import Portfolio 
import unittest 
from prototype.instrument import retrieve_ticker_from_csv

retrieve_ticker_from_csv()


data = pd.DataFrame(data = {'SPX' : [50,60,70,90,50,30,80] , 'SX5E' : [100,90,120,140,110,200 ,190]})
data['DATE'] = pd.date_range('01/01/2020', '01/09/2020', freq = 'B' )

data.loc[0,'DATE'] = datetime(2018,5,31)
data.loc[1,'DATE'] = datetime(2019,5,30)
data.loc[2,'DATE'] = datetime(2019,5,31)

data['DATE'].astype('datetime64[ns]')

spx = data[['DATE','SPX']] 
spx = spx.rename(columns = {'SPX' : 'CLOSE'})
sx5e = data[['DATE','SX5E']] 
sx5e = sx5e.rename(columns = {'SX5E' : 'CLOSE'})

df_map = {'SX5E' :sx5e, 'SPX': spx }
weight_map ={'SPX' : 0.3 , 'SX5E' : 0.7 }

p = Portfolio( df_map,
				weight_map,
				datetime(2018,5,31).date(),
				datetime(2020,1,9).date(),
				'BME',
				0,
				100)

class TestPortfolio(unittest.TestCase):


	def test_quantity(self):
		spx_q = p.data.iloc[-1]['SPX_Q']
		sx5e_q = p.data.iloc[-1]['SX5E_Q']

		assert (round(spx_q,6) == round(1.02857142857143,6))
		assert (round(sx5e_q,6) == round(1.28333333333333,6))

	def balance_test(self):
		assert data['CASH'][-1] == 200

	def balance_test(self):
		assert round(data['BALANCE'][-1],6) == round(326.119047619047,6)

	def pnl_test(self):
		assert round(data['PnL'][-1],6) == round(326.119047619047 - 200,6)

if __name__ == '__main__' :
	unittest.main()