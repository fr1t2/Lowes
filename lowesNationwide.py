import requests
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
import time


with open("storesall.txt") as s:
    data = []
    for store in map(str.strip, s):
        url = "https://www.lowes.com/pd/search/999919858/pricing/{}".format(store)
        response = requests.get(url, timeout=None)
        soup = BeautifulSoup(response.content, "html.parser")
        jstext = soup.find('script', type="text/javascript").text
        pricesearch = re.search(r'\d+[.]\d*', jstext)
        price = pricesearch.group()
	
        temp_dict = {'price': price}
        temp_dict = {'store': store}

        temp_dict['price'] = price

        print(temp_dict.items())

        data.append(temp_dict)

#this saves the results once the loop is done to results.csv
with open('results.csv', 'w') as outfile:
    f = csv.DictWriter(outfile, ['store', 'price'],
                       delimiter=',', lineterminator='\n')
    f.writeheader()
    f.writerows(data)

#This takes the results and:
#1)adds store info (city, state, zip, etc)
#2)removes any blank lines (lines that dont have a price)
#3)sorts by price (low to high)
#4)output is saved as LowesResultsAll.csv, overwriting any existing file.
first = pd.read_csv('results.csv')
second = pd.read_csv('allstores.csv')

first = first[pd.notnull(first['price'])]

first.sort_values(["price"], inplace=True, ascending=True)  

merged = pd.merge(first, second, how='left', on='store')

merged.to_csv('LowesResultsAll.csv', index=False)
