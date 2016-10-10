
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
    url ="https://jobs.telegraph.co.uk/employers/"+str(letter) 
    print(url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    data = {
        'tags' : [],
        'job_no' : []
    }
    for links in soup.find_all( class_="cf block lister"):
        ass = links.find_all(class_ ="lister__header")
    for i in range(0,len(ass)):
        data['tags'].append(ass[i].a.get_text() )
        data["job_no"].append(ass[i].get_text('href'))
    comp = pd.DataFrame( data )
#    comp["tags"] = comp["tags"].apply(lambda x: x.encode('utf-8').strip())
#    comp["tags"] = comp["tags"].apply(lambda x: str(x).replace("\n","").replace("\n \n","").replace("(UK)","").replace("(SERVICES)","").replace("jobs","").replace("job",""))
    comp["job_no"]= comp["job_no"].map(lambda x: x[x.find("href"):x.rfind("jobs")].replace("jobs","").replace("job","").replace("href","").replace("jo",""))
#    comp["tags"]= comp["tags"].map(lambda x: x[0:x.rfind("(")])
    return comp


#code to run complist function over the neccessary pages and aggregate the data together. Result is a full list of company names
alph = range(1,17)

letlist = pd.DataFrame()
for let in alph:
    time.sleep(2)
    letlist = letlist.append(complist(let))

letlist = letlist.reset_index()
del letlist["index"]   

import datetime as dt    
date = dt.datetime.today().strftime("%d_%m_%Y")

letlist.to_csv("/home/mint/Documents/WP1/Data/Telegraph/telegraph"+date+".csv",encoding="utf-8")
