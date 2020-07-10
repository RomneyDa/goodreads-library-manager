# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:14:33 2020

@author: Dalli
"""
from rauth.service import OAuth1Service, OAuth1Session

#### ASKING FOR ACCESS
# Get a real consumer key & secret from: https://www.goodreads.com/api/keys
CONSUMER_KEY = 'TNY6fDFILUDCTXZ739z56w'
CONSUMER_SECRET = 'k1CksvrhI3xOcTSDcQU9jCL2yw1HYYzft4fx9SRuB4'

goodreads = OAuth1Service(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    name='goodreads',
    request_token_url='https://www.goodreads.com/oauth/request_token',
    authorize_url='https://www.goodreads.com/oauth/authorize',
    access_token_url='https://www.goodreads.com/oauth/access_token',
    base_url='https://www.goodreads.com/'
    )

# head_auth=True is important here; this doesn't work with oauth2 for some reason
request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)
print('Visit this URL in your browser: ' + authorize_url)
accepted = 'n'
while accepted.lower() != 'y':
    # you need to access the authorize_link via a browser,
    # and proceed to manually authorize the consumer
    accepted = input('Have you authorized me? (y/n) ')
    
    
#### ADDING A BOOK TO A SHELF
session = goodreads.get_auth_session(request_token, request_token_secret)

# book_id 631932 is "The Greedy Python"
data = {'name': 'to-read', 'book_id': 631932}

# add this to our "to-read" shelf
response = session.post('https://www.goodreads.com/shelf/add_to_shelf.xml', data)

# these values are what you need to save for subsequent access.
ACCESS_TOKEN = session.access_token
ACCESS_TOKEN_SECRET = session.access_token_secret

new_session = OAuth1Session(
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET,
)

# book_id 631932 is "The Greedy Python"
data = {'name': 'to-read', 'book_id': 631932}

# add this to our "to-read" shelf
response = new_session.post('https://www.goodreads.com/shelf/add_to_shelf.xml', data)

if response.status_code != 201:
    print('Cannot create resource: %s' % response.status_code)
else:
    print('Book added!')