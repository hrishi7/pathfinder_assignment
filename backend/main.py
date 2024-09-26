from flask import Flask, jsonify, request
from datetime import datetime
from util.index import get_flight_offers
import random  # For demonstration purposes

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/flights/ping')
def ping():
    return jsonify({"data": "pong"})

@app.route('/flights/price')
def get_cheapest_flight():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date_str = request.args.get('date')
    number_of_passengers = request.args.get('passengers') if request.args.get('passengers') is not None else 1
    max_results = request.args.get('max_results') if request.args.get('max_results') is not None else 1

    if not all([origin, destination, date_str]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        travel_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    data = get_flight_offers(origin, destination, date_str, number_of_passengers, max_results)


    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)
