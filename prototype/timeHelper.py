from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Union

class TimeHelper():
	
	TIME_ZONE = 'Europe/London'

	@staticmethod
	def change_date_formatting(cob : Union[datetime,str] , formatting_from :str , formatting_to : str) -> str:
		if isinstance(cob, str):
			cob = datetime.strptime(cob,formatting_from)
		cob = cob.strftime(formatting_to)
		return cob

	@staticmethod
	def datetime_to_timestamp( dt : datetime):
		ts_int = int(datetime(dt.year, dt.month, dt.day).timestamp())*1e3
		return ts_int

	@staticmethod
	def business_date(date: str = None):
		date = datetime.strptime(date, "%d/%m/%Y") if date != None else datetime.now() - timedelta(days =1)
	
		shift = timedelta(days = 0)
		#check if Saturday
		if date.strftime("%w") == '6':
			shift = timedelta(days = 1)
		#check if Sunday
		if date.strftime("%w") == '0':
			shift = timedelta(days = 2)
		cob = date - shift
		return datetime(cob.year,cob.month,cob.day).astimezone(ZoneInfo(TimeHelper.TIME_ZONE))

	@staticmethod
	def time_conversion(convention : str, frequency : str):
		days = TimeHelper.days_in_year(convention)
		if convention == 'actual':
			if frequency == 'B': return 1/days
			if frequency == 'W': return TimeHelper.days_in_week(convention)/days
			if 'BM' in frequency: return TimeHelper.days_in_month(convention)/days
			if 'BQ' in frequency: return TimeHelper.days_in_quarter(convention)/days
			else : return 1
		if convention == 'trading':
			if frequency == 'B': return 1/days
			if frequency == 'W': return TimeHelper.days_in_week(convention)/days
			if 'BM' in frequency: return TimeHelper.days_in_month(convention)/days
			if 'BQ' in frequency: return TimeHelper.days_in_quarter(convention)/days
			else : return 1

	@staticmethod
	def adjustementWeekFreq(date_array, frequency : str):
		if frequency == 'WS':
			return date_array.apply(lambda x : x + timedelta(days = 1))
		if frequency == 'WE':
			return date_array.apply(lambda x : x + timedelta(days = 5))

	@staticmethod
	def days_in_year(convention : str):
		if convention == 'actual':
			return 365
		if convention == 'trading':
			return 252

	@staticmethod
	def days_in_quarter(convention : str):
		if convention == 'actual':
			return 90
		if convention == 'trading':
			return 21*3

	@staticmethod
	def days_in_month(convention : str):
		if convention == 'actual':
			return 30
		if convention == 'trading':
			return 21

	@staticmethod
	def days_in_week(convention : str):
		if convention == 'actual':
			return 7
		if convention == 'trading':
			return 5

