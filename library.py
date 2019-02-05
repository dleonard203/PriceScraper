import tinydb
import selenium
import time
import json
from tinydb import TinyDB, Query
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import plotly


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
with open('config.json', 'r') as j_in:
	config_data = json.load(j_in)

driver_loc = confid_data['chromedriver_path']
amazon_db = TinyDB('amazon.json')
#ebay_db = TinyDB('ebay.json')


class amazon_driver():
	def __init__(self):
		d = webdriver.Chrome(driver_loc)
		d.get("http://www.amazon.com")
		time.sleep(2)
		self.home = True
		self.search = False
		self.in_item_page = False
		self.driver = d

	def close(self):
		self.driver.close()

	def search_for(self, item):
		print(self.driver.current_url)
		assert self.home == True
		search_box = self.driver.find_element_by_name("field-keywords")
		search_box.clear()
		search_box.send_keys(item)
		search_box.send_keys(Keys.RETURN)
		time.sleep(2)
		self.home = False
		self.search = True

	def first_result(self):
		assert self.search == True
		for elem in self.driver.find_elements_by_tag_name("a"):
			attempts = 0
			if elem.get_attribute("class").find("a-link-normal a-text-normal") > -1: #s-access-detail-page  s-color-twister-title-link a-text-normal"
				while attempts < 5:
					try:
						elem.click()
					except:
						attempts += 1
		time.sleep(3)
		self.search = False
		self.in_item_page = True

	def get_price(self):
		# assert self.in_item_page == True
		# res = self.driver.find_element_by_id("priceblock_ourprice")
		# print(res.text)
		assert self.search == True
		dollars = self.driver.find_element_by_class_name("sx-price-whole").text
		cents = self.driver.find_element_by_class_name("sx-price-fractional").text
		whole_price = str(dollars) + '.' + str(cents)
		whole_price = whole_price.replace(',', '')
		print("result found!\n")
		print(whole_price)
		self.driver.close()
		return float(whole_price)
		

def scrape_amazon_for(item):
	driver = amazon_driver()
	driver.search_for(item)
	res = float(driver.get_price())
	#time.sleep(10)
	return res

# a_d = amazon_driver()
# a_d.search_for("super smash brothers melee")
# #a_d.first_result()
# a_d.get_price()
# time.sleep(10)
# a_d.close()

#scrape_amazon_for("super smash brothers melee")

#remove all illegal filename characters from string
def fileize_string(name):
	illegal_chars = ['\'', '\"', '[', ']', ':', '\\', '/', '*', '?', '<', '>', '|']
	for char in illegal_chars:
		name = name.replace(char, '')
	return name

############# Plotting ##########################
def make_time_series_chart(db, item):
	question = Query()
	result = db.search(question.item == item)
	if result != []:
		record = result[0]
		print('record: ' + str(record) + '\n')
		price_list = record['prices']
		dates = list(map(lambda x: x[0], price_list))
		prices = list(map(lambda x: x[1], price_list))
		data = [go.Scatter(x=dates, y=prices)]
		item = fileize_string(item)
		print('item: ' + item + '\n' + 'dates:' + str(dates) + '\n' + 'prices: ' + str(prices) + '\n')
		plotly.offline.plot(data, filename = item + ' prices over time.html')

def make_amazon_charts():
	for item in config_data['items']:
		
		print('item' + item + '\n')
		make_time_series_chart(amazon_db, item)