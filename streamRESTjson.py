## Imports
import urllib2, urllib, json, requests, time, os.path, psycopg2
import pandas as pd
from urllib2 import HTTPError
from datetime import datetime

def JSONtoPostgres(x):
    
    '''
    Save JSON to Postgres
    '''
    
    #import username and password for postgres
    with open('/Users/theresa/postgres.json') as f:
        data = json.load(f)
        user = data['user'] 
        password = data['password']
    try:
        conn = psycopg2.connect("dbname='finalproject' user='{}' host='localhost' password='{}'".format(user,password))
        x0 = json.dumps(x)
        cur = conn.cursor()
        cur.execute("INSERT INTO delaytable (data) VALUES(%s);",(x0,))
    except:
        print "JSONtoPostgres didn't work!"
        pass


df = pd.read_csv('airportData/us_airports.csv')
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
    
    #Save to Postgres
    JSONtoPostgres(l)
    
    end = time.time()
    
    #Run again in an hour
    time.sleep(3600 - (end-start))