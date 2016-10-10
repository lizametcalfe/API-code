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

import pandas as pd
import time
import sys

url ="https://jobsearch.direct.gov.uk/jobsearch/Browse.aspx?sc=em"
print(url)
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

#stop truncating of strings
pd.options.display.max_seq_items = 2000
pd.options.display.max_colwidth = 1000

N = 10000
#go up from here

def complist():
    url ="https://jobsearch.direct.gov.uk/jobsearch/Browse.aspx?sc=em"
    print(url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    data = {
        'website':[]
    }
    for links in soup.find_all(class_="browseJobsList"):
        ass = links.find_all("tr")
    for i in range(1,len(ass)):
        data['website'].append(ass[i].get_text())
    comp = pd.DataFrame( data )    
    comp["tags"] = comp["website"].apply(lambda x: str(x).replace("\n",""))
    comp["website"] = comp["tags"].apply(lambda x: str(x)[str(x).rfind('(')+1:str(x).rfind(')')])
    comp["tags"] = comp["tags"].apply(lambda x: str(x)[0:str(x).rfind('(')])
    return comp

the = complist()

import datetime as dt    
date = dt.datetime.today().strftime("%d_%m_%Y")

the.to_csv("/home/mint/Documents/WP1/Data/Universal/universal"+date+".csv",encoding="utf-8")
