from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from datetime import datetime
from util.index import get_flight_offers
from dotenv import load_dotenv
from util.cache import RedisCache
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Flight Offers API',
    description='A simple API to retrieve flight offers')

load_dotenv()

ns = api.namespace('api', description='Flight operations')

flight_model = api.model('FlightOffer', {
    'data': fields.Raw(description='Flight offer data')
})

@ns.route('/flights/ping')
class Ping(Resource):
    @api.doc(description='Simple health check endpoint')
    @api.response(200, 'Success')
    def get(self):
        return jsonify({"data": "pong"})

@ns.route('/flights/price')
class FlightPrice(Resource):
    @api.doc(params={
        'origin': {'description': 'Origin airport code', 'required': True},
        'destination': {'description': 'Destination airport code', 'required': True},
        'date': {'description': 'Travel date (YYYY-MM-DD)', 'required': True},
        'passengers': {'description': 'Number of passengers', 'default': 1},
        'max_results': {'description': 'Maximum number of results to return', 'default': 1},
        'no_cache': {'description': 'Bypass cache', 'type': 'boolean'}
    })
    @api.response(200, 'Success', flight_model)
    @api.response(400, 'Bad Request')
    def get(self):
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        date_str = request.args.get('date')
        number_of_passengers = request.args.get('passengers', 1, type=int)
        max_results = request.args.get('max_results', 1, type=int)
        no_cache = request.args.get('no_cache', type=bool)

        if not all([origin, destination, date_str]):
            api.abort(400, "Missing required parameters")

        try:
            travel_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            api.abort(400, "Invalid date format. Use YYYY-MM-DD")
        
        data = get_flight_offers(origin, destination, date_str, number_of_passengers, max_results, no_cache)

        return jsonify(data)

if __name__ == '__main__':
    RedisCache.initialize()
    app.run(host="0.0.0.0", port=int("1025"), debug=True)
