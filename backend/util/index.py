import requests
from requests.auth import HTTPBasicAuth

def get_flight_offers(origin_location_code, destination_location_code, departure_date, number_of_passengers, max_result_count):
    # API endpoint
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    # Query parameters
    params = {
        "originLocationCode": origin_location_code,
        "destinationLocationCode": destination_location_code,
        "departureDate": departure_date,
        "adults": number_of_passengers,
        "max": max_result_count
    }

    # API credentials
    api_key = "UZO9TntO7jvmdPydE3rC9fpBZDieIQUu"
    api_secret = "OrGSeIzeeDgq36WV"

    # Get access token
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_data = {
        "grant_type": "client_credentials"
    }
    token_response = requests.post(token_url, data=token_data, auth=HTTPBasicAuth(api_key, api_secret))
    access_token = token_response.json()["access_token"]

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
