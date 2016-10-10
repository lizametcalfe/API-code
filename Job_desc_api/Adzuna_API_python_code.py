from urllib2 import Request, urlopen, URLError
import json
from pandas.io.json import json_normalize
import requests
import pandas as pd
import matplotlib
import numpy as np
import time
import sys

#stop truncating of strings
pd.options.display.max_seq_items = 2000
pd.options.display.max_colwidth = 1000

N = 10000
#go up from here

#Courses: https://www.codecademy.com/apis

#URL for Adzuna
#Parameters:
#   First page
#   unique API key, please register on the website and change this to your own: https://developer.adzuna.com/overview
#    category is IT job, this can be removed (collect all) or changed to reflect what you would like to collect.
#    To see other options see: http://api.adzuna.com/static/swagger-ui/index.html#!/adzuna/search_get_0

the = 'http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id="add your appd id here"&app_key="add your app key here"&category=it-jobs&results_per_page=50&content-type=application/text/html'
#start from here

#request API results for the URL of interest and return dataframe, return "That's your lot!" when finished.
#pause for 5 seconds between requests
def adzunalapi(url):
    time.sleep(5)
    request = Request(url)
    try:
        response = urlopen(request)
        resp = response.read()
        data = json.loads(resp)
    except URLError, e:
        print 'No response. Got an error code:', e
    try:
        df = json_normalize(data['results'])
        return df
    except:
        sys.exit("That's your lot!")

#Cycle through the URL's changing the page number from 1 to 2...
df = pd.DataFrame({ 'A' : range(720, N + 1 ,1)})
df["URL"]= df["A"].apply(lambda x: the.replace("1?",str(x)+"?"))

dff=pd.DataFrame()
for i in df["URL"]:
    print(i)
    try:
        dff = dff.append(adzunalapi(i))
    except:
        pass

 #simplify the created variable
dff=dff.reset_index()
dff["created2"]=dff["created"].apply(lambda x: str(x)[8:10])
dff["created2"]=dff["created2"].apply(lambda x: x.replace("-",""))

#take out the regional information from the location field
foo = lambda x: pd.Series([i for i in str(x).split(',')])
dff["region"] = dff['location_area'].apply(foo)[1]
dff["region"] = dff["region"].apply(lambda x: str(x).replace("',","").replace("u","").replace("]",""))

#save data
dff.to_csv("C:\\.....csv", encoding='utf-8')
dff = dff.reset_index()