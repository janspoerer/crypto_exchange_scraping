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

driver = webdriver.Chrome("/home/janspoerer/code/janspoerer/crypto_exchange_scraping/chromedriver")
driver.get("https://www.cryptocompare.com/exchanges/#/overview")

# Load mapping for country alpha three codes to allow conversion from country name to country code
with open('country_mappings.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('country_mappings_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        country_mappings_dict = {rows[0]:rows[1] for rows in reader}

def find_url(exchange):
    # To Dos:
    link = exchange.find_element_by_css_selector('.name .ng-binding').get_attribute("href")
    time.sleep(float(decimal.Decimal(random.randrange(100, 200))/100)) #  Random

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)
    result = driver.find_element_by_css_selector('#col-body img , #header-profile .btn').get_attribute("href")
    driver.execute_script("window.close();")

    # Make sure parent window is selected
    driver.switch_to.window(driver.window_handles[0])

    return result

for x in range(1, 12):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

exchanges = driver.find_elements_by_class_name("item-list")

full_list = []

for exchange in exchanges:
    results = {}

    results["name"] = exchange.find_element_by_class_name("ng-binding").text

    country_name = exchange.find_element_by_css_selector('.feature-values .ng-binding').text
    if country_name in country_mappings_dict:
        results["country"] = country_mappings_dict[country_name]
    else:
        results["country"] = "Country not identified"
    print(results["country"])

    results["url"] = find_url(exchange)

    full_list.append(results)

print(full_list)
print(len(full_list))

keys = full_list[0].keys()
with open('exchanges.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(full_list)
