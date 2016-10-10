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
    url ="https://jobs.theguardian.com/employers/"+str(letter) 
    print(url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    data = {
        'tags' : [],
        'jobs' : []
    }
    for link in soup.find_all( class_="cf block lister"):
        ass = link.find_all(class_="lister__header")
    for i in range(0,len(ass)):
        data['tags'].append(ass[i].a.get_text() )
        try:
            data['jobs'].append(ass[i].small)
        except:
            data['jobs'] = "0"
    comp = pd.DataFrame( data )
    comp["jobs"] =comp["jobs"].apply(lambda x: str(x).replace("<small>","")[str(x).replace("<small>","").find(">")+1:str(x).replace("<small>","").find("</")].replace("jobs","").replace("job",""))
    comp["jobs"][comp["jobs"] == "Non"]=0
    return comp


    #code to run complist function over the neccessary pages and aggregate the data together. Result is a full list of company names
alph = range(1,226)

letlist = pd.DataFrame()
for let in alph:
    time.sleep(2)
    letlist = letlist.append(complist(let))

letlist = letlist.reset_index()
del letlist["index"]    

import datetime as dt    
date = dt.datetime.today().strftime("%d_%m_%Y")
date

letlist.to_csv("/home/mint/Documents/WP1/Data/Guardian/guardian"+date+".csv",encoding="utf-8")
