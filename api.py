# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 12:37:45 2020
@author: Ayush Kapoor

"""
#============================================
#%% -------RESTful API Implementation--------
#============================================ 
'''
Here requests library is used for implementation instead of Flask/Docker, as we do not 
intend to focus on production ready system.

'''
#---------------------------------------------------
#%% Importing Necessary Libraries
#---------------------------------------------------
import requests
import json

#---------------------------------------------------
#%% Parameter & variable Declarations
#---------------------------------------------------
urls = []
resp_data = []
# These movie-ids are taken at random from the OMDB
movie_id = ['tt7131622','tt7131322', 'tt6565702' ,'tt4154796'] # Can be changed later on
api_id = '68fd98ab' # As provided
omdb_url  = 'http://www.omdbapi.com/?i={0}&apikey={1}&plot=full'
# The RAW urls are being used here so as to to parse them.
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/11043689.json')
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/11528860.json')
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/3532674.json')
urls.append('https://bitbucket.org/babydestination/movie-metadata-service/raw/8108d622f70a432c6c5c77bde22ee60129f6d5bf/movies/5979300.json')

#----------------------------------------------------
#%% Function Declarations
#----------------------------------------------------
# This method takes key and value as two lists and return a dictionary after making required operations
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

# The input to this fucntion is value of 'userrating' key and will convert to the format of 'Rating' of OMDB format by creating a JSON string
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

# This method will take string (',' separated) & will return a string array    
def Str2StrArray (str_):
    return str_.split(',') # Will return a list

#------------------------------------------------ 
#%% Task 1: Fetching data from static urls and omdb API
#------------------------------------------------
for i in range (len(urls)):
    resp=requests.get(urls[i])
    if (resp.status_code == 200): # Check for Successful connection
        resp_data.append (resp)
        print ('DEBUG: Details of '+str(resp.json()['id'])+ ' Fetched.')
    else:
        print ('ERROR: Error Connecting URL. Movie ID:'+urls[i].split('/')[-1].split('.')[0]+'. Try Again\n')   
    
for i in range (len(movie_id)):
    resp=requests.get(omdb_url.format(movie_id[i], api_id))
    if (resp.status_code == 200): # Check for Successful connection
        resp_data.append (resp)
        print ('DEBUG: Details of '+resp.json()['imdbID']+' Fetched.')
    else:
        print ('ERROR: Conenction to OMDB Failed. Movie ID:'+movie_id[i]+'.Try Again\n')

#--------------------------------------------------
#%% Task 2: Applying Merging Rules 
#--------------------------------------------------
# The rules will be applied to the data as per the requirements
key = []
value = []
for i in range (len(resp_data)):
    for k,v in resp_data[i].json().items():
        key.append (k)
        value.append (v)
    # Replace the old data with the new processed data    
    resp_data[i] = eval(ApplyRules(key,value))
    # Emptying the key-value list 
    del key[:]
    del value[:]

#--------------------------------------------------    
#%% Task 3: Merging both the Data
#--------------------------------------------------    
# We will now create a dictionary from the data we just generated above
respDict = {}
for i,resp in enumerate (resp_data):
    respDict[i+1] = resp
    
# Clearing previous data (Release memory from redundant data)
del resp_data   

#-------------------------------------------------- 
#%% Task 4: Implementing the GET functionality
#--------------------------------------------------
# This will take the id as inut and will print the data corresponding to that id.
search_id = input ('Input the ID to be searched->\n')
# Nested Iteration (Complexity: O(n2))
for k,v in respDict.items():
    for in_k,in_v in v.items():
        if ('id' == in_k):
            print (v)
            break
        else:
            print ('RESULT: Result to this ID not found. :(')
        if ('imdbID' == in_k):
            print (v)
            break
        else:
            print ('RESULT: Result to this ID not found. :(') 

