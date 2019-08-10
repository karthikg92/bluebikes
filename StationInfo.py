import pandas as pd 

class StationInfo:

	def __init__(self, raw_data):
		self.last_updated = raw_data['last_updated']
		self.data = pd.DataFrame(raw_data['data']['stations'])
		#self.data.drop(['rental_url', 'external_id', 'eightd_station_services'], axis = 1, inplace = True)
		return None

	def save(self, fname = None):
		if fname:
			self.data.to_csv(fname, index = False)
		else:
			self.data.to_csv('station_info.csv', index = False)
		return None


