from flask import Flask, jsonify, request
from datetime import datetime
from util.index import get_flight_offers
from dotenv import load_dotenv
from util.cache import RedisCache
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

load_dotenv();

#
# Provides a simple health check endpoint for the application.
# This endpoint can be used to verify that the application is running and responding to requests.
#
@app.route('/flights/ping')
def ping():
    return jsonify({"data": "pong"})

#
# Retrieves the cheapest flight offer based on the provided origin, destination, travel date, number of passengers, and maximum number of results to return.
# Args:
#     origin (str): The origin airport code.
#     destination (str): The destination airport code.
#     date_str (str): The travel date in the format 'YYYY-MM-DD'.
#     number_of_passengers (int, optional): The number of passengers. Defaults to 1.
#     max_results (int, optional): The maximum number of results to return. Defaults to 1.
# Returns:
#     dict: A JSON response containing the flight offer data.
# Raises:
#     ValueError: If the provided date format is invalid.
#
@app.route('/api/flights/price')
def get_cheapest_flight():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date_str = request.args.get('date')
    number_of_passengers = request.args.get('passengers') if request.args.get('passengers') is not None else 1
    max_results = request.args.get('max_results') if request.args.get('max_results') is not None else 1
    no_cache = request.args.get('no_cache')

    if not all([origin, destination, date_str]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        travel_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    data = get_flight_offers(origin, destination, date_str, number_of_passengers, max_results, no_cache)


    return jsonify(data)

if __name__ == '__main__':
    RedisCache.initialize()
    app.run(debug=True)
