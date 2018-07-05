'''
	Developed by Raiu
'''
# encoding=utf8

import json
import csv
import math
import requests


# find woeid from => https://www.flickr.com/places/info/
API_KEY = 'faac20e291025ba6bdc0331ff92c63ee'
url = 'https://api.flickr.com/services/rest/'
template_url = 'https://farm%s.staticflickr.com/%s/%s_%s.jpg'


class Flickr_API_Class:
	# set initial properties
	def __init__(self, woe_id, date_from, date_to):
		self.woe_id = woe_id
		self.date_from = date_from
		self.date_to = date_to

		self.titles = ['owner', 'owner_is_from', 'date_taken', 'time_taken', 'latitude', 'longitude', 'url']
		self.c_page_number = 1
		self.properties = {
			'api_key'        :  API_KEY,
			'format'         : 'json',
			'nojsoncallback' : '1',
			'method'         : 'flickr.photos.search',
			'woe_id'         :  self.woe_id,
			'has_geo'        : '1',
			'sort'           : 'date-posted-asc',
			'min_taken_date' :  self.date_from,
			'max_taken_date' :  self.date_to,
			'extras'         : 'geo, date_taken',
			'per_page'       : '250',    # 250 is Max
			'page'           :  self.c_page_number
		}

		self.request  = requests.get(url, params=self.properties)
		self.response = self.request.json()
		self.total    = int(self.response['photos']['total'])
		# print(total)
		self.max_page = math.ceil(self.total / 250)
		print(self.request)
		print(json.dumps(self.response, sort_keys=True, indent=2))


	def search(self, page):
		self.c_page_number = page
		self.request  = requests.get(url, params=self.properties)
		self.response = self.request.json()
		print(self.request)
		print(json.dumps(self.response, sort_keys=True, indent=2))


	def make_csv(self, output_file_name):
		self.c_page_number = 1
		self.place = ''
		self.user_list = []
		self.location_list = []

		with open(output_file_name + '.csv', 'w') as output_file:
			writer = csv.writer(output_file)
			writer.writerow(self.titles)

		while self.c_page_number <= self.max_page:
			print("Making %d in %d" % (self.properties['page'], self.max_page))
			data_list = []
			self.request = requests.get(url, params=self.properties)
			self.response = self.request.json()

			for i in self.response['photos']['photo']:
				data_set = []
				now_user_id = i['owner']
				date_taken  = i['datetaken'][:10]
				time_taken  = i['datetaken'][10:]
				lat         = i['latitude']
				lon         = i['longitude']
				img_url     = template_url % (i['farm'], i['server'], i['id'], i['secret'])

				if(now_user_id not in self.user_list):
					self.user_list.append(now_user_id)
					self.properties2 = {
						'api_key'        : API_KEY,
						'format'         : 'json',
						'method'         : 'flickr.people.getinfo',
						'nojsoncallback' : '1',
						'user_id'        : now_user_id
					}
					self.request2  = requests.get(url, params=self.properties2)
					self.response2 = self.request2.json()
					if 'location' in self.response2['person']:
						place = self.response2['person']['location']['_content']
						if(place == ''):
							place = 'Not Found'
					else:
						place = 'Not Found'
					self.location_list.append(place)
				else:
					index = self.user_list.index(now_user_id)
					print(str(len(self.location_list)) + ":" + str(index))
					place = self.location_list[index]

				data_set = [now_user_id, place, date_taken, time_taken, lat, lon, img_url]
				data_list.append(data_set)
				# print(data_list)


			with open(output_file_name + '.csv', 'a') as output_file:
				writer = csv.writer(output_file)
				writer.writerows(data_list)

			self.c_page_number += 1
			self.properties = {
				'api_key'        :  API_KEY,
				'format'         : 'json',
				'nojsoncallback' : '1',
				'method'         : 'flickr.photos.search',
				'woe_id'         :  self.woe_id,
				'has_geo'        : '1',
				'sort'           : 'date-posted-asc',
				'min_taken_date' :  self.date_from,
				'max_taken_date' :  self.date_to,
				'extras'         : 'geo, date_taken',
				'per_page'       : '250',    # 250 is Max
				'page'           :  self.c_page_number
			}


API = Flickr_API_Class("test", "2345853", '2015-08-20 00:00:00', '2016-08-30 00:00:00')
API.make_csv("test")


