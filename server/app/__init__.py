# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
#from instance.config import app_config
import datetime

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):

	from api.models import User, Trip

	app = FlaskAPI(__name__, instance_relative_config=True)
	#app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	@app.route('/trip/', methods=['POST', 'GET'])
	def trip():
		if request.method == 'POST':
			name = str(request.data.get('name', ''))
			description = str(request.data.get('description', ''))
			date_starts = str(request.data.get('date_starts', ''))
			date_ends = str(request.data.get('date_ends', ''))
			owner = str(request.data.get('owner', ''))
			date_starts = datetime.datetime.strptime(date_starts, '%d-%m-%Y %H:%M')
			date_ends = datetime.datetime.strptime(date_ends, '%d-%m-%Y %H:%M')
			if name and date_starts and date_ends:
				trip = Trip(name=name, description=description,
					date_starts=date_starts, date_ends=date_ends,
					owner=owner)
				trip.save()
				response = jsonify({
					'id': trip.id,
					'name': trip.name,
					'description': trip.description,
					'date_created': trip.date_created,
					'date_starts': trip.date_starts,
					'date_ends': trip.date_ends,
					'owner': trip.owner
					})
				response.status_code = 201
				return response
		else: #GET
			trips = Trip.get_all()
			results = []
			for trip in trips:
				obj = {
					'id': trip.id,
					'name': trip.name,
					'description': trip.description,
					'date_created': trip.date_created,
					'date_starts': trip.date_starts,
					'date_ends': trip.date_ends,
					'owner': trip.owner
				}
				results.append(obj)
			response = jsonify(results)
			response.status_code = 200
			return response

	@app.route('/trip/<int:id>', methods=['GET', 'PUT', 'DELETE'])
	def trip_manipulation(id, **kwargs):
		trip = Trip.query.filter_by(id=id).first()
		if not trip:
			abort(404)
		if request.method == 'DELETE':
			trip.delete()
			return {'message': 'trip {} deleted successfully'.format(trip.id)
			}, 200
		elif request.method == 'PUT':
			name = str(request.data.get('name', ''))
			description = str(request.data.get('description', ''))
			date_starts = str(request.data.get('date_starts', ''))
			date_ends = str(request.data.get('date_ends', ''))
			owner = str(request.data.get('owner', ''))
			date_starts = datetime.datetime.strptime(date_starts, '%d-%m-%Y %H:%M')
			date_ends = datetime.datetime.strptime(date_ends, '%d-%m-%Y %H:%M')
			
			trip.name = name
			trip.description = description
			trip.date_starts = date_starts
			trip.date_ends = date_ends
			trip.owner = owner
			trip.save()
			response = jsonify({
					'id': trip.id,
					'name': trip.name,
					'description': trip.description,
					'date_created': trip.date_created,
					'date_starts': trip.date_starts,
					'date_ends': trip.date_ends,
					'owner': trip.owner
				})
			response.status_code = 200
			return response
		else: #GET
			response = jsonify({
					'id': trip.id,
					'name': trip.name,
					'description': trip.description,
					'date_created': trip.date_created,
					'date_starts': trip.date_starts,
					'date_ends': trip.date_ends,
					'owner': trip.owner
				})
			response.status_code = 200
			return response
	"""
	from .auth import auth_blueprint
	app.register_blueprint(auth_blueprint)"""


	return app