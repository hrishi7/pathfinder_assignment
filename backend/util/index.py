import os
import requests
import json
from redis import Redis
from datetime import timedelta
from util.token import get_amadeus_token
from util.cache import get_redis_client



# '''
# Gets flight offers from the Amadeus API.

# This function retrieves flight offers based on the provided origin, destination, departure date, number of passengers, and maximum result count. 
# It checks the cache for existing data unless nocache is set to True. If the data is not cached, it makes a request to the Amadeus API to fetch the flight offers. 
# The retrieved data is cached for future use. Returns the flight data or an error message if the API request fails.
# '''
def get_flight_offers(origin_location_code, destination_location_code, departure_date, number_of_passengers, max_result_count, nocache=False):
    # Initialize Redis client
    redis_client = get_redis_client()
    CACHE_EXPIRATION_FOR_API_DATA = 600  # 10 minutes in seconds
    cache_key = f"flight_offers:{origin_location_code}:{destination_location_code}:{departure_date}:{number_of_passengers}:{max_result_count}"

    # Check cache if nocache is False
    if not nocache:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            print("Data: Cache hit!")
            return json.loads(cached_data)

    # API endpoint
    url = os.getenv('AMADEUS_FLIGHT_OFFERS_ENDPOINT')

    # Query parameters
    params = {
        "originLocationCode": origin_location_code,
        "destinationLocationCode": destination_location_code,
        "departureDate": departure_date,
        "adults": number_of_passengers,
        "max": max_result_count
    }

    #
    # Gets the Amadeus API access token.
    # This function retrieves the Amadeus API access token, which is required for making authenticated requests to the Amadeus API. 
    # The token is obtained by calling the `get_amadeus_token()` function
    #
    access_token = get_amadeus_token()

    # Set up headers with access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Make the API request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        flight_data = response.json()
        # Cache the data
        redis_client.setex(cache_key, CACHE_EXPIRATION_FOR_API_DATA, json.dumps(flight_data))
        return flight_data
    else:
        error_data = response.json()
        if 'errors' in error_data and len(error_data['errors']) > 0:
            error = error_data['errors'][0]
            return {
                "error": f"API request failed: {error.get('title', 'Unknown error')}",
                "detail": error.get('detail', ''),
                "code": error.get('code', ''),
                "status": error.get('status', response.status_code)
            }
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
