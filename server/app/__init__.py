# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
#from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):

	from api.models import User

	app = FlaskAPI(__name__, instance_relative_config=True)
	#app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	@app.route('/user/', methods=['POST', 'GET'])
	def user():
		if request.method == 'POST':
			name = str(request.data.get('name', ''))
			email = str(request.data.get('email', ''))
			if name and email:
				user = User(name=name, email=email)
				user.save()
				response = jsonify({
					'id': user.id,
					'name': user.name,
					'email': user.email,
					'date_created': user.date_created
					})
				response.status_code = 201
				return response
		else: #GET
			users = User.get_all()
			results = []
			for user in users:
				obj = {
					'id': user.id,
					'name': user.name,
					'email': user.email,
					'date_created': user.date_created
				}
				results.append(obj)
			response = jsonify(results)
			response.status_code = 200
			return response

	@app.route('/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
	def user_manipulation(id, **kwargs):
		user = User.query.filter_by(id=id).first()
		if not user:
			abort(404)
		if request.method == 'DELETE':
			user.delete()
			return {'message': 'user {} deleted successfully'.format(user.id)
			}, 200
		elif request.method == 'PUT':
			name = str(request.data.get('name', ''))
			email = str(request.data.get('email', ''))
			user.name = name
			user.save()
			response = jsonify({
					'id': user.id,
					'name': user.name,
					'email': user.email,
					'date_created': user.date_created
			})
			response.status_code = 200
			return response
		else: #GET
			response = jsonify({
					'id': user.id,
					'name': user.name,
					'email': user.email,
					'date_created': user.date_created
			})
			response.status_code = 200
			return response


	return app