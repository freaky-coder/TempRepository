# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 12:37:45 2020
@author: Ayush Kapoor

"""
#%% -------RESTful API Implementation-------- 

#%% Importing Necessary Libraries
import requests
import json
import time

#%% Parameter & variable Declarations
urls = []
resp_data = []
movie_id = ['tt7131622','tt7131322', 'tt6565702' ,'tt4154796'] # Can be changed later on
api_id = '68fd98ab'
omdb_url  = 'http://www.omdbapi.com/?i={0}&apikey={1}&plot=full'
# The RAW urls are being used here so as to to parse them.
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/11043689.json')
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/11528860.json')
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/3532674.json')
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/5979300.json')

#%% Function Declarations
# This method takes key and value as two lists and return a 
# dictionary after making required operations
def ApplyRules (k,v):
    for i in range (len(k)):
        if (k[i] == 'title'):
            k[i] = 'Title'
        if ((k[i] == 'description') or (k[i] == 'Description')):
            k[i] = 'Plot'
        if (k[i] == 'duration'):
            k[i] = 'Runtime'
        if (k[i] == 'userrating'):
            k[i] = 'Ratings'   
            v[i] = convertRatings (v[i])
        if ((k[i] == 'Actors') or (k[i] == 'Writer') or (k[i] == 'Director')):
            v[i] = Str2StrArray (v[i])
    return json.dumps(dict(zip(k,v)))

# The input to this fucntion is value of 'userrating' key
# and will convert to the format of 'Rating' of OMDB format
def convertRatings (value_):
    c = 0
    f_value = ''
    for key,value in value_.items():
        c+=1
        temp = '{'
        temp = temp +"'Source':"+"'%s'," %key +"'Value':"+"'%s'" %value
        temp = temp + '}'
        if (c < len(value_)):
            temp = temp + ','
        f_value = f_value+temp
    return f_value

# This method will take string (',' separated)
# and will return a string array    
def Str2StrArray (str_):
    return str_.split(',') # Will return a list
 
#%% Task 1: Fetching data from static urls and omdb API
for i in range (len(urls)):
    resp=requests.get(urls[i])
    if (resp.status_code == 200): # Check for Successfull connection
        resp_data.append (resp)
        print ('DEBUG: '+str(resp.json()['id']))
    else:
        print ('ERROR: Error Connecting URL. Movie ID:'+urls[i].split('/')[-1].split('.')[0]+'. Try Again\n')   
    
for i in range (len(movie_id)):
    resp=requests.get(omdb_url.format(movie_id[i], api_id))
    if (resp.status_code == 200): # Check for Successfull connection
        resp_data.append (resp)
        print ('DEBUG:'+resp.json()['imdbID'])
    else:
        print ('ERROR: Conenction to OMDB Failed. Movie ID:'+movie_id[i]+'.Try Again\n')

#%% Task 2: Applying Merging Rules
# These rules stand only for the static json files we have stored
key = []
value = []
for i in range (len(resp_data)):
    for k,v in resp_data[i].json().items():
        key.append (k)
        value.append (v)
    # Replace the old data with the new processed data    
    resp_data[i] = ApplyRules (key,value)
    # Emptying the key-value list 
    del key[:]
    del value[:]
    
#%% Task 3: Merging both the Data 














