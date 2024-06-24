from flask import Blueprint, request, jsonify, abort
from flask_restful import Resource, Api

blueprint = Blueprint('api_test', __name__, url_prefix='/api')
api = Api(blueprint)

class ApiTest(Resource):

	def get(self):
		return jsonify({"msg": "api active"})

	def post(self):

		if not request.is_json:
			abort(400)

		post_data = request.get_json()
		return jsonify({"request": post_data})


api.add_resource(ApiTest, '/test')