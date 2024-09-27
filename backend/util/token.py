import os
import time
import requests
import redis
from dotenv import load_dotenv

load_dotenv()

class TokenManager:
    def __init__(self):
        self.client_id = os.getenv('AMADEUS_CLIENT_ID')
        self.client_secret = os.getenv('AMADEUS_CLIENT_SECRET')
        self.token_url = os.getenv('AMADEUS_TOKEN_ENDPOINT');
        self.redis = redis.Redis(host='redis', port=6379, db=0)
        self.token_key = 'amadeus_token'
        self.expiration_key = 'amadeus_token_expiration'

    def get_token(self):
        token = self.redis.get(self.token_key)
        expiration = self.redis.get(self.expiration_key)
        
        if token is None or expiration is None or float(expiration) <= time.time():
            self._fetch_new_token()
            token = self.redis.get(self.token_key)
        
        return token.decode('utf-8')

    def _fetch_new_token(self):
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
            
            self.redis.set(self.token_key, token)
            self.redis.set(self.expiration_key, expiration)
        else:
            raise Exception("Failed to obtain Amadeus API token")

# Create a singleton instance of TokenManager
token_manager = TokenManager()

def get_amadeus_token():
    return token_manager.get_token()
