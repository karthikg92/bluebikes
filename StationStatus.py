import numpy as np 
import pandas as pd 


class StationStatus:

	def __init__(self):
		self.data = None
		self.last_updated = None

		return None

	def update(self, raw_data, write_previous = False):
		if raw_data['last_updated'] == self.last_updated:
			return None

		if write_previous == True:
			if self.data is not None:
				self.data.to_csv( str(self.last_updated) + '_dataframe.csv' , index = False)

		self.last_updated = raw_data['last_updated']
		station_list = raw_data['data']['stations']
		self.data = pd.DataFrame(station_list)
		#self.data.drop(['eightd_active_station_services'], axis = 1, inplace = True)
		self.data.to_csv(  'current_dataframe.csv' , index = False)
		#station_id 179 is the one next to Tang
		return None