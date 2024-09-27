import os
import time
import requests
from dotenv import load_dotenv
from util.cache import get_redis_client

load_dotenv()

"""
TokenManager class to manage Amadeus API tokens.
Handles token retrieval and refresh based on expiration time.
"""
class TokenManager:
    def __init__(self):
        self.client_id = os.getenv('AMADEUS_CLIENT_ID')
        self.client_secret = os.getenv('AMADEUS_CLIENT_SECRET')
        self.token_url = os.getenv('AMADEUS_TOKEN_ENDPOINT')
        self.token_key = 'amadeus_token'
        self.expiration_key = 'amadeus_token_expiration'

    '''
    Retrieve the current token from the cache.
    If the token is expired or not available, fetch a new token.
    Returns the token as a UTF-8 decoded string.
    '''
    def get_token(self):
        redis_client = get_redis_client()
        token = redis_client.get(self.token_key)
        expiration = redis_client.get(self.expiration_key)
        
        if token is None or expiration is None or float(expiration) <= time.time():
            self._fetch_new_token()
            token = redis_client.get(self.token_key)
        
        return token.decode('utf-8')

    '''
    Fetches a new Amadeus API token using client credentials.
    Posts a request to the token URL with the client ID and client secret.
    If successful, sets the retrieved token and its expiration time in the Redis cache.
    Raises an exception if unable to obtain the token.
    '''
    def _fetch_new_token(self):
        redis_client = get_redis_client()
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            # Set expiration time to 29 minutes from now (1 minute buffer)
            expiration = time.time() + (29 * 60)
            
            redis_client.set(self.token_key, token)
            redis_client.set(self.expiration_key, expiration)
        else:
            raise Exception("Failed to obtain Amadeus API token")

# Create a singleton instance of TokenManager
token_manager = TokenManager()

def get_amadeus_token():
    return token_manager.get_token()
