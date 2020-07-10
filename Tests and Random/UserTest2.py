# import subprocess
# import sys
#
# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# install('rauth')

from rauth.service import OAuth1Service, OAuth1Session
import webbrowser

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
#We'll have to exchange our request token for an access token, but doing so requires the user's permission (of course). Open up the authorize_url in your browser in order to allow access to your account.

authorize_url = goodreads.get_authorize_url(request_token)
webbrowser.open_new(authorize_url)

#accepted = 'n'
#while accepted.lower() == 'n':
    # you need to access the authorize_link via a browser,
    # and proceed to manually authorize the consumer
#    accepted = input('Have you authorized me? (y/n) ')

#Adding a Book to a Shelf
#You'll redirect users in your own app to this URL and once they've allowed access they'll be redirected to the Callback URL you provided when registering. Once they're back, you can access the OAuth protected API endpoints:
print(request_token, request_token_secret)
session = goodreads.get_auth_session(request_token, request_token_secret)

id = 631932 # The Greedy Python
#id =
#shelf = 'currently-reading'
shelf = 'to-read'
data = {'name': shelf, 'book_id': 631932}

# add this to our "to-read" shelf
response = session.post('https://www.goodreads.com/shelf/add_to_shelf.xml', data)

# these values are what you need to save for subsequent access.
ACCESS_TOKEN = session.access_token
ACCESS_TOKEN_SECRET = session.access_token_secret

# #Multiple Sessions
# #Goodreads access tokens are valid until they're revoked by the user. One you have your access token, simply store the token and secret to start using it again.
# # create a new session using only our consumer and access keys/secrets
#  # these values are what you need to save for subsequent access.
# ACCESS_TOKEN = session.access_token
# ACCESS_TOKEN_SECRET = session.access_token_secret
#
# new_session = OAuth1Session(
#     consumer_key = CONSUMER_KEY,
#     consumer_secret = CONSUMER_SECRET,
#     access_token = ACCESS_TOKEN,
#     access_token_secret = ACCESS_TOKEN_SECRET,
# )
#
# # book_id 375802 is "Ender's Game"
# data = {'name': 'to-read', 'book_id': 375802}
#
# # add this to our "to-read" shelf
# response = new_session.post('https://www.goodreads.com/shelf/add_to_shelf.xml', data)
#
# if response.status_code != 201:
#     raise Exception('Cannot create resource: %s' % response.status_code)
# else:
#     print('Book added!')
