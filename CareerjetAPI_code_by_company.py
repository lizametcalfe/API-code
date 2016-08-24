#DateL 24/8/2016
#Author: Liz Metcalfe
#Aim: To collect the number of job vacancies for specific companies is careerjet. This becomes more tricky when the names of the company vary in different lists.
#The company name tags from the careerjet website are used (scraped) to match with the list of companies of interest, and then the API is alled by company name.

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
from urllib import urlopen
from bs4 import BeautifulSoup

import fuzzywuzzy
from fuzzywuzzy import fuzz
import operator

#function to scrape the name of the companies and put them in a dataframe
def complist(letter):
    url = "http://www.careerjet.co.uk/jobs/"+letter+".html"    
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    ass = soup.find_all("a")
    abc = pd.DataFrame()
    for i in range(0,len(ass)):
        try:
            abc.loc[i,"tags"] = ass[i].get("title").encode('utf-8').strip()
        except:
            abc.loc[i,"tags"] = ass[i].get("title")
    return abc

#code to run complist function over the neccessary pages and aggregate the data together. Result is a full list of company names
alph = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1']

letlist = pd.DataFrame()
for let in alph:
    time.sleep(2)
    letlist = letlist.append(complist(let))

letlist = letlist.reset_index()
del letlist["index"]    


#load company names
#load a list of companies of interest
comp = pd.read_csv("....\sample_of_company_names.csv")
comp.rename(columns={'RU Name':'Companies'}, inplace=True)
comp2 = comp

# re-format the company names (loaded)
unwanted = ["limited","ltd","plx","(uk)","all", "vat", "(u.k.)", "london", "services", "inc","incl", "group", "uk"]

def removewords(data):
    data = str(data).split()
    resultwords  = [word for word in data if word.lower() not in unwanted]
    return ' '.join(resultwords)

comp["Companies"] = comp["Companies"].apply(lambda x: x.lower())
comp["Companies"] = comp["Companies"].apply(lambda x: removewords(x))
letlist["tags"] = letlist["tags"].apply(lambda x: removewords(x))
letlist["tags"]=letlist["tags"].apply(lambda x: str(x).lower())

#match company names with company names using fuzzy matching
#match comp["Companies"] to abc

def findmatch(name):
    letlist["matchno"] = letlist["tags"].apply(lambda x: fuzz.ratio(name,x))
    index, value = max(enumerate(letlist["matchno"]), key=operator.itemgetter(1))
    if value > 90:
        letlists = letlist.loc[index,"tags"]
    else:
        letlists = name
    del letlist["matchno"]
    return letlists

comp["compmatch"] = comp["Companies"].apply(lambda x: findmatch(x))

#search API's for company tags and return number of vacancies for each company

from careerjet_api_client import CareerjetAPIClient

cj  =  CareerjetAPIClient("en_GB");

#function to request from API, add API id number and IP address, also change browser used if neccessary.

def careerjetAPI(keywords):
    result_json = cj.search({
        'keywords'    : 'company:"'+keywords+'"',
        'affid'       : 'add API id number here',
        'user_ip'     : 'add your IP address here',
        'url'         : 'http://www.careerjet.co.uk/jobsearch?q=company:"'+keywords+'"',
        'user_agent'  : 'Firefox/31.0'
        });
    time.sleep(2)
    return result_json["hits"]

#careerjetAPIall("boots")

#Cycle through the URL's changing the page number from 1 to 2...
df = pd.DataFrame()
dff=pd.DataFrame()
for i in comp["compmatch"]:
    df["index"] = range(0,1)
    df["company"]= i
    df["count"] = careerjetAPI(i)
    try:
        dff = dff.append(df)
    except:
        pass

#add path to save
dff.to_csv("...\_results_careerjet.csv")
