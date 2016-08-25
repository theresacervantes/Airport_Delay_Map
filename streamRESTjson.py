## Imports
import urllib2, urllib, json, requests, time, os.path
import pandas as pd
from urllib2 import HTTPError
from datetime import datetime


df = pd.read_csv('us_airports.csv')
iata = set(df.iata_code)
now = datetime.now()


'''
Obtain FAA's RESTful API of Airport Delays, which is updated every hour. 
Saving it to S3 and local disk. 
Source: http://services.faa.gov/docs/basics/
'''

save_path = "./delayData/"
while True:
    start = time.time()

    l = []
    for i in iata:
        try:
            results = urllib2.urlopen("http://services.faa.gov/airport/status/{}?format=application/json".format(i)).read()
            data = json.loads(results)
            l.append(data)
            
        except HTTPError:
            pass
        
    now = datetime.now()
    
    #Save locally
    name_of_file = now.strftime("%Y-%m-%d-%H-%M")
    completeName = os.path.join(save_path, name_of_file+".json")   
    with open(completeName, 'w') as file1:
        json.dump(l, file1)
    file1.close()
    
    end = time.time()
    time.sleep(3600 - (end-start))