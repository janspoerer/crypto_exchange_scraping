from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup
# For sleeper
import time
# For random sleeper times
import random
# For decimal numbers
import decimal
# For permanent disk storage of results as CSV
import csv

driver = webdriver.Chrome("/home/janspoerer/code/janspoerer/scraping_deloitte_list/chromedriver")
driver.get("https://www2.deloitte.com/lu/en/pages/technology/articles/regtech-companies-compliance.html")

list_item_names = driver.find_elements_by_class_name("container-line")

full_list = []

for list_item_name in list_item_names:
    results = {}

    results["name"] = list_item_name.find_element_by_css_selector(".column1 a").text
    print(results["name"])

    results["country_name"] = list_item_name.find_element_by_css_selector('.country-img').get_attribute('title')
    print(results["country_name"])

    results["year"] = list_item_name.find_element_by_css_selector('.year').text
    print(results["year"])

    results["employees"] = list_item_name.find_element_by_css_selector('.employees').text
    print(results["employees"])

    full_list.append(results)

print(full_list)
print(len(full_list))

keys = full_list[0].keys()
with open('exchanges.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(full_list)
