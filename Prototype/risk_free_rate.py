"""Module to retrieve 
	risk free rate
"""

class Risk_Free_Rate():

	ir_map = {'USD' : ['SOFR']}

	def __init__(self, ARR : str = '', currency : str = '' ):
		self.ARR = ir_map[]
		
		
	@staticmethod
	def SOFR(value):
		return (100 - value)/100 
