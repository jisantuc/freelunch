import requests
import pprint as p
#from sunlight import capitolwords #this might be totally unnecessary
from ggplot import *
import pandas as pd
import numpy as np

api_key = '887de3e17a5f445b879c20372af0a6a1'

#need to get:
#   method for counting anti-free-lunch-ist speeches given in congress by senator/rep
#   database of congressional gifts received OR
#   database of money spent dining lobbyists (free DINNER also counts, eh? ha)
#   or both.
#   plan for how to visualize (maybe d3py instead, if you feel like learning that; something like a McDouble that grows or shrinks based on how much money was spent or received on free lunches)

endpoint = 'http://capitolwords.org/api/1/text.json'

#gets phrases between start and end dates. Going to be using this a lot, so there's a DRY
#attempt here and not much else interesting going on
def get_phrase_standard(phrase, start, end):
    """Gets phrases between start and end dates.
Dates must be formatted for use in CapitolWords API, which is 'YYYY-MM-DD'
Returns a pandas dataframe full of all pages in results"""
    
    keys = ['speaker_state',
            'speaker_first',
            'congress',
            'title',
            'origin_url',
            'number',
            'pages',
            'volume',
            'chamber',
            'session',
            'speaking',
            'capitolwords_url',
            'speaker_party',
            'date',
            'bills',
            'bioguide_id',
            'order',
            'speaker_last',
            'speaker_raw']

    out_df = pd.DataFrame(columns = keys)

    i = 0

    while True:
        print i
        
        query_params = {'apikey': '887de3e17a5f445b879c20372af0a6a1',
                        'phrase': phrase,
                        'per_page': 1000, #this appears to be the maximum
                        'page': i,
                        'start_date': start,
                        'end_date': end}

        response = requests.get(endpoint, params = query_params)
        
        if len(response.json()['results']) > 0:
            i += 1
            out_df = pd.concat([out_df, pd.DataFrame.from_dict(response.json()['results'])])
        else:
            return out_df


#def merge_requests(requests):
#    """Takes a list of requests and concatenates them into a single dict"""
    

#We can use this to show that things are working, but I did that already, so it's unnecessary now.
#test = get_phrase_standard(phrase = 'America',
#                           start = '2013-01-05',
#                           end = '2013-09-06')
#print len(test.index)

#this is the list of phrases I'm associating with "free-lunch-ism," or
#the belief that people can get something for free. In this sense, a caricatured
#Bernie Sanders is an absolute free-lunch-ist, while a caricatured Rand Paul is
#an absolute anti-free-lunch-ist.
#Plan will be: get count of each of these by legislator for the length of the
#Obama administration and analyze total sentiment (polarity) using NLTK to get each
#Congressperson's free-lunch-ism score
#Note: this list is entirely improvisational. Scores may be sensitive to inclusion/
#exclusion of certain words or phrases
phrases = ['entitlement', 'entitlement programs', 'food stamps',
           'social security', 'tighten our belts', 'budget deficit']

#makes a dictionary of the dataframes returned by get_phrase_standard() for each phrase
#in phrases
data = {ph: get_phrase_standard(ph, start = '2008-01-01', end = '2014-06-01') for ph in phrases}

#hooray, look what we have!
print {ph: len(data[ph]) for ph in data.keys()}
