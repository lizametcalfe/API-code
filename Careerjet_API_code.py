import pandas as pd
import time
import sys

#stop truncating of strings
pd.options.display.max_seq_items = 2000
pd.options.display.max_colwidth = 1000

N = 10000
#go up from here

#Courses: https://www.codecademy.com/apis

#Read in list of company names or any other keywords to search for jobs by. Just a simple csv file with a list on will do.
comp = pd.read_csv(".....csv")


#remove any unwanted words from the keywords search.
unwanted = ["limited","ltd","plx","(uk)","all", "vat", "(u.k.)", "london"]

def removewords(data):
    data = str(data).split()
    resultwords  = [word for word in data if word.lower() not in unwanted]
    return ' '.join(resultwords)

comp["Companies"] = comp["Companies"].apply(lambda x: x.lower())
comp["Companies"] = comp["Companies"].apply(lambda x: removewords(x))
comp["Companies"] = comp["Companies"].apply(lambda x: x.replace(" ","+"))


#function to request data from Careerjets API. You will need to sign up for an account to use this: http://www.careerjet.co.uk/partners
#Add in you affid (top right of screen), IP address (open terminal, type ipconfig if you don't know this)
# and put in your user_agent (web browser in)
#More informatino can be found here: https://github.com/careerjet/careerjet-api-client-python

#this will return the count of jobs for each keyword search however, if you remove the ["hits"] there is a lot more information available
from careerjet_api_client import CareerjetAPIClient

cj  =  CareerjetAPIClient("en_GB");

def careerjetAPI(keywords):
    result_json = cj.search({
        'keywords'    : keywords,
        'affid'       : '1fda10a87c250ec936a0082f7244ec97',
        'user_ip'     : '172.28.3.16',
        'url'         : 'http://www.careerjet.co.uk/jobsearch?q='+keywords,
        'user_agent'  : 'Firefox/31.0'
        });
    time.sleep(2)
    return result_json["hits"]


#Cycle through the URL's changing the keywords
df = pd.DataFrame()
dff=pd.DataFrame()
for i in comp["Companies"]:
    df["index"] = range(0,1)
    df["company"]= i
    df["count"] = careerjetAPI('"'+i+'"')
    print(i)
    try:
        dff = dff.append(df)
    except:
        pass

#This will return a dataframe with the keyword used and the count of jobs found

dff.to_csv("add path to save space here")