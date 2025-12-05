"""Module to retrieve 
	risk free rate
"""

class InterestRate():
	def __init__(self, currency):
		self.currency = currency
		self.value = self._value
		
	
	@property
	def Treasury(self):
		return { 'USD' : 'IRX',
				 'EUR' : 'IRX',
				 'GBP' : 'IRX',
				 'CHF' : 'IRX',
				 'JPY' : 'IRX'}[self.currency]
	
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

	def _value(self,value):
		return value/100

class Treasury(InterestRate):

	def __init__(self, currency : str ):
		super().__init__(currency)

		self.name = getattr(super(),'Treasury')
		self.value = self._value

	@property
	def convention(self):
		return 'ACT/ACT'
		

class RiskFreeRate(InterestRate):

	def __init__(self, currency : str ):
		super().__init__(currency)

		self.name = getattr(super(),'OIS')
		self.value = self._value

	@property
	def convention(self):
		return 'ACT/360'
		
	def _value(self,value):
		return (100 - value)/100 
