import requests
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
import time

# query the productList.txt for what to search. Will run this for each found
with open("productList.txt") as p:
    #Create an array for the stuffs
    productNum = []
    # For loop below opens and reads all lines in the file, and adds them to the array
    for item in map(str.strip, p):
        #print (item)
        with open("storesall.txt") as s:
            data = []
            for store in map(str.strip, s):
               # print (store)
                url = "https://www.lowes.com/pd/search/{}/pricing/{}".format(item, store)
                response = requests.get(url, timeout=None)
                soup = BeautifulSoup(response.content, "html.parser")
                jstext = soup.find('script', type="text/javascript").text
                pricesearch = re.search(r'\d+[.]\d*', jstext)
                qtysearch = re.search(r'\d+[:]\d*', jstext)
                if pricesearch:
                    price = pricesearch.group()
                    temp_dict = {'price': price}
                    temp_dict = {'item': item}
                    temp_dict = {'store': store}
                    temp_dict['price'] = price
                    temp_dict['item'] = item
                    if qtysearch:
                        qty = qtysearch.group()
                        temp_dict = {'qty': qty}
                        temp_dict['qty'] = qty
                    else
                        print(item, store, " None available..")
                    print(temp_dict.items())
                    data.append(temp_dict)
                else:
                   print(store, " Not Found...")
        #this saves the results once the loop is done to results.csv
        with open('results/{}_results.csv'.format(item), 'w') as outfile:
            f = csv.DictWriter(outfile, ['item', 'store', 'price'],
                            delimiter=',', lineterminator='\n')
            f.writeheader()
            f.writerows(data) # may be an error, and need to remove the productNum here
        #This takes the results and:
        #1)adds store info (city, state, zip, etc)
        #2)removes any blank lines (lines that dont have a price)
        #3)sorts by price (low to high)
        #4)output is saved as LowesResultsAll.csv, overwriting any existing file.
        first = pd.read_csv('results/{}_results.csv'.format(item))
        second = pd.read_csv('allstores.csv')
        first = first[pd.notnull(first['price'])]
        first.sort_values(["price"], inplace=True, ascending=True)  
        merged = pd.merge(first, second, how='left', on='store')
        merged.to_csv('results/{}_LowesResultsAll.csv'.format(item), index=False)
