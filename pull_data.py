import numpy
import pandas
import json
import requests
from datetime import datetime
import time
from multiprocessing import Process
import sys

from StationStatus import *
from StationInfo import *



#station_status is the dynamically changing information of interest
# Load this information every minute, and send it to the StationStatus object

def pull_data(status):
	while True:
		#print("Pulling data from BlueBikes")
		response = requests.get(bluebikes_url['station_status'])
		station_status_raw = json.loads(response.text)

		ttl = station_status_raw['ttl']
		update_time = int(time.time())
		status.update(station_status_raw, write_previous = False)
		if int(time.time()) < update_time + ttl:
			time.sleep( update_time + ttl - int(time.time()) )

# Print out live status about a specified set of stations in a readable text file
def select_status(s_names):
	while True:
		#print("Updating the status of select stations")
		# Load the files and create a smaller one
		station_info = pd.read_csv('station_info.csv')
		station_status = pd.read_csv('current_dataframe.csv')
		
		f = open("SelectStatus.txt","w+")
		for s in s_names:
			#print(s)
			s_id = station_info[station_info['name'] == s]['station_id'] 
			s_id = int(s_id.values[0])
			#print(s_id)
			row = station_status[station_status['station_id'] == s_id]
			bikes = row['num_bikes_available']
			docks = row['num_docks_available']
			f.write("Station name : " + s + '\n')
			f.write("Number of bikes : %d\n" %(bikes) )
			f.write("Number of docks : %d\n\n" %(docks) )
		f.close()
		time.sleep(10)

	return None

if __name__ == '__main__':
	response = requests.get("https://gbfs.bluebikes.com/gbfs/gbfs.json")
	bluebikes = json.loads(response.text)
	bluebikes = bluebikes['data']['en']['feeds']

	# Extract all the URLs needed for the specific json datastream
	bluebikes_url = {}
	for item in bluebikes:
		bluebikes_url[item['name']] = item['url']

	# system_region: breakdown into Boston, Hingham, QUincy etc
	# system_alerts: special info like valet service unavailable at a station
	# station_information: static list of stations, capacities and locations
	# system_information: company name, url, etc
	# station_status: number of bikes and docks at each station

	# one time pull of the station information
	response = requests.get(bluebikes_url['station_information'])
	station_information_raw = json.loads(response.text)
	station_information = StationInfo(station_information_raw)
	station_information.save()


	# We want to run both of these simultaneously

	station_status = StationStatus()
	station_list = ['MIT Vassar St', 'MIT at Mass Ave / Amherst St', 'Nashua Street at Red Auerbach Way']
	
	p1 = Process(target = pull_data, args = (station_status,))
	p2 = Process(target = select_status, args = (station_list,))
	p1.start()
	p2.start()
	p1.join()
	p2.join()

	#pull_data(station_status)
	#select_status(station_list)