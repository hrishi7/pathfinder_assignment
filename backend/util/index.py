import os
import requests
from requests.auth import HTTPBasicAuth
from util.token import get_amadeus_token

def get_flight_offers(origin_location_code, destination_location_code, departure_date, number_of_passengers, max_result_count):
    # API endpoint
    url = os.getenv('AMADEUS_FLIGHT_OFFERS_ENDPOINT');

    # Query parameters
    params = {
        "originLocationCode": origin_location_code,
        "destinationLocationCode": destination_location_code,
        "departureDate": departure_date,
        "adults": number_of_passengers,
        "max": max_result_count
    }

    access_token = get_amadeus_token();

    # Set up headers with access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Make the API request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}"}
