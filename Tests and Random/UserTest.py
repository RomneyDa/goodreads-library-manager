# import subprocess
# import sys

# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# install('oauth2')

import oauth2 as oauth
import urllib
import webbrowser

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token/' % url
authorize_url = '%s/oauth/authorize/' % url
access_token_url = '%s/oauth/access_token/' % url

consumer = oauth.Consumer(key='TNY6fDFILUDCTXZ739z56w',
                          secret='k1CksvrhI3xOcTSDcQU9jCL2yw1HYYzft4fx9SRuB4')

client = oauth.Client(consumer)

response, content = client.request(request_token_url, 'GET')
content = content.decode()

# If the response is not successful, raise an exception
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

request_token = dict(urllib.parse.parse_qsl(content))

# Create a link for the user to go to to authorize access
authorize_link = '%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'])
webbrowser.open_new(authorize_link)
#
# accepted = 'n'
# while accepted.lower() == 'n':
#     # you need to access the authorize_link via a browser,
#     # and proceed to manually authorize the consumer
#     accepted = input('Have you authorized me? (y/n) ')

token = oauth.Token(request_token['oauth_token'],
                    request_token['oauth_token_secret'])

client = oauth.Client(consumer, token)

response, content = client.request(access_token_url, 'POST')
content = content.decode()
if response['status'] != '200':
    print(response['status'],'User has not yet been authorized')
    #raise Exception('Invalid response: %s' % response['status'])

access_token = dict(urllib.parse.parse_qsl(content))
print(access_token)

#this is the token you should save for future uses
token = oauth.Token(access_token['oauth_token'],
                   access_token['oauth_token_secret'])

#http://www.goodreads.com/oauth/authorize/?oauth_token=hDMllJFVCu0VcBml6BOTAw
token = oauth.Token('5DKMLmTsV3vjPpUYW0rVkw', '')
#
# As an example, let's add a book to one of the user's shelves


client = oauth.Client(consumer, token)
# the book is: "Generation A" by Douglas Coupland
body = urllib.parse.urlencode({'name': 'to-read', 'book_id': 6801825})
headers = {'content-type': 'application/x-www-form-urlencoded'}
response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
                                   'POST', body, headers)
# check that the new resource has been created
if response['status'] != '201':
    raise Exception('Cannot create resource: %s' % response['status'])
else:
    print('Book added!')
