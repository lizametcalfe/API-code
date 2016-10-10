import pandas as pd
import time
import sys

#stop truncating of strings
pd.options.display.max_seq_items = 2000
pd.options.display.max_colwidth = 1000

N = 10000
#go up from here

#take company names of website
import nltk   
from urllib.request import urlopen
from bs4 import BeautifulSoup

import re

def complist(letter):
    url ="http://www.reed.co.uk/recruiterdirectory?pageno="+str(letter) 
    print(url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    data = {
        'tags' : []
    }
    for link in soup.find_all( class_="employers"):
        ass= link.find_all( class_="subtitle")
    for i in range(0,len(ass)):
        data['tags'].append(ass[i].get_text() )
    comp = pd.DataFrame( data )
    comp["tags"] = comp["tags"].apply(lambda x: x.encode('utf-8').strip())
    comp["tags"] = comp["tags"].apply(lambda x: str(x).replace("\n","").replace("\n \n","").replace("(UK)","").replace("(SERVICES)","").replace("jobs","").replace("job",""))
    comp["no_jobs"]= comp["tags"].map(lambda x: x[x.rfind("(")+1:x.rfind(")")].replace("jobs","").replace("job",""))
    comp["tags"]= comp["tags"].map(lambda x: x[0:x.rfind("(")])
    return comp

#code to run complist function over the neccessary pages and aggregate the data together. Result is a full list of company names
alph = range(1,146)

letlist = pd.DataFrame()
for let in alph:
    time.sleep(5)
    letlist = letlist.append(complist(let))

letlist = letlist.reset_index()
del letlist["index"]   

import datetime as dt    
date = dt.datetime.today().strftime("%d_%m_%Y")

letlist.to_csv("/home/mint/Documents/WP1/Data/Reed/reed"+date+".csv",encoding="utf-8")
