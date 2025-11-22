"""Module to retrieve 
	risk free rate
"""

class Interest_Rate():
	def __init__(self, currency):
		self.currency = currency
		
	
	@property
	def Treasury(self):
		pass 
	
	@property
	def OIS(self):
		return { 'USD' : 'SOFR',
				 'EUR' : 'ESTER',
				 'GBP' : 'SONIA',
				 'CHF' : 'SARON',
				 'JPY' : 'TONAR'}[self.currency]

	@property
	def Repo(self):
		pass

class Risk_Free_Rate(Interest_Rate):

	def __init__(self, currency : str ):
		super().__init__(currency)

		self.name = getattr(super(),'OIS')
		self.value = self.ir_value

	@property
	def convention(self):
		return 'ACT/360'
		
	def ir_value(self,value):
		return (100 - value)/100 
