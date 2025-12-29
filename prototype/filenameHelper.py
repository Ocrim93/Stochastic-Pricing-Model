from .measure import Measure as M

class FileName:

	@staticmethod
	def price(base_folder_output
			  ,ticker
			  ,currency
			  ,start_date
			  ,end_date
			  ,frequency
			  ,source
			  ,is_interest_rate_flag):
		
		folder_output = f'{base_folder_output}/{ticker}'
		filename =  f"{ticker}_"+ (f"({currency})" if not is_interest_rate_flag else "_")+\
					f"{start_date}_"+\
					f"{end_date}_"+\
					f"{frequency}_{source}"

		return folder_output,filename

	@staticmethod
	def pair(base_folder_output
			 ,ticker
			 ,start_date
			 ,end_date
			 ,frequency
			 ,source):

		folder_output = f'{base_folder_output}/{ticker}'
		filename = f"{ticker}_"+\
				   f"{start_date}_"+\
				   f"{end_date}_"+\
				   f"{frequency}_{source}"

		return folder_output,filename

	@staticmethod
	def financials(base_folder_output
			  	  ,ticker
			  	  ,source):

		folder_output = f'{base_folder_output}/{ticker}'
		filename = f"{ticker}_{source}"

		return folder_output,filename

	@staticmethod
	def portfolio(base_folder_output
			  	  ,list_asset
			  	  ,currency
			  	  ,start_date
			  	  ,end_date):

		filename = f"{'_'.join(list_asset)}_({currency})"+\
				   f"{start_date}_"+\
				   f"{end_date}"		
		folder_output = f'{base_folder_output}/{filename}'
		
		return folder_output,filename

	@staticmethod
	def volatility_surface(base_folder_output
			  			   ,ticker
			  			   ,start_date
			  			   ,source):
		
		folder_output = f'{base_folder_output}/{ticker}/{start_date}'
		filename = f"{ticker}_{source}"

		return folder_output,filename
		
	
	def __init__(self):
		pass