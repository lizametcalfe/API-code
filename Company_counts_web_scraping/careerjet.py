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

import fuzzywuzzy
from fuzzywuzzy import fuzz
import operator

#function to scrape the name of the companies and put them in a dataframe
def complist(letter):
    url = "http://www.careerjet.co.uk/jobs/"+letter+".html"  
    print(url)
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    data = {
        'tags' : []
    }
    for link in soup.find_all( id="heart"):
        ass = link.find_all("tr")    
    for i in range(0,len(ass)):
        data['tags'].append(ass[i].get_text() )
    comp = pd.DataFrame( data )
    comp["job_1"]= comp["tags"].map(lambda x: x[0:x.find("\n\n\n")].replace("\n",""))
    comp["job_2"]= comp["tags"].map(lambda x: x.rsplit('\n\n\n', 1)[-1].replace("\n\n","").replace("\n",""))
    comp1 = comp[["job_1"]]
    comp2 = comp[["job_2"]]
    comp1["job_no"]=comp1["job_1"].map(lambda x: x[x.rfind("(")+1:x.rfind(")")])
    comp2["job_no"]=comp2["job_2"].map(lambda x: x[x.rfind("(")+1:x.rfind(")")])
    comp1["job"]= comp1["job_1"].map(lambda x: x[0:x.rfind("(")])
    comp2["job"]= comp2["job_2"].map(lambda x: x[0:x.rfind("(")])
    del comp1["job_1"]
    del comp2["job_2"]
    comps = pd.concat([comp1,comp2],axis=0)
    return comps

#code to run complist function over the neccessary pages and aggregate the data together. Result is a full list of company names
alph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1']

letlist = pd.DataFrame()
for let in alph:
    time.sleep(2)
    letlist = letlist.append(complist(let))

letlist = letlist.reset_index()
del letlist["index"]    
letlist = letlist.dropna()
import datetime as dt    
date = dt.datetime.today().strftime("%d_%m_%Y")

letlist.to_csv("/home/mint/Documents/WP1/Data/Careerjet/careerjet"+date+".csv",encoding="utf-8")
