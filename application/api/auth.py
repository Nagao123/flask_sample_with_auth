from flask import Blueprint, request, abort
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import check_password_hash

from models.models import User
from models.database import db
from models.validation import ValidationAbort
from models.replacestring import ReplaceString

blueprint = Blueprint('api_auth', __name__, url_prefix='/api/auth')
api = Api(blueprint)


class Login(Resource):

	def post(self):
		if not request.is_json:
			abort(400, 'Bad Request')
			
		json_data = request.get_json()
		
		num_filter_keys = []
		raw_data_keys = []
		clean_data = ReplaceString().clean_form_data(json_data, num_filter_keys, raw_data_keys)
		
		user_id = clean_data['user']
		user_password = clean_data['password']
		
		validation = ValidationAbort()
		validation.email(user_id)
		validation.password(user_password)

		user = User.query.filter_by(user=user_id).first()

		if not user:
			abort(404, 'User not found')

		if not check_password_hash(user.password, user_password):
			abort(400, 'Invalid Password')

        ## access_token: default = 15 mins
		## refresh_token: default = 30 days
		return {
			'access_token' : create_access_token(identity=user_id),
			'refresh_token': create_refresh_token(identity=user_id)
		}

api.add_resource(Login, '/login')

class RefreshToken(Resource):

	@jwt_required(refresh=True)
	def post(self):
		identity = get_jwt_identity()
		return { 'access_token': create_access_token(identity=identity) }

api.add_resource(RefreshToken, '/refresh')

'''
One of the problems with JWT authentication is that JWTs expire,
and then the user has to re-authenticate by providing their username & password.

We can provide our users two tokens:
1. access token: they can use to access endpoints
2. refresh token: they can use to get a new access token without having to provide their username and password

For a client, the authentication flow is a three-step process:
1. Send the access token they've got stored (may or may not be fresh).
2. If API responds with a 401 Unauthorized, use the refresh token to get a new access token and try again.
   Now you've got a new, non-fresh access token.
3. If the API responds with another 401 Unauthorized, ask the user to log in again.
   Now you've got a fresh access token.

Freshness:
・A fresh access token is given to users immediately after logging in.
・A non-fresh access token is given to users when they use their refresh token.
・e.g. If the user goes to their 'delete my account' page, we might want a fresh token to access that endpoint.
       However, if they're simply going to their profile page, we may accept a non-fresh token.
	   
@jwt_required() => e.g. profile
@jwt_required(fresh=True) => e.g. change-password, delete-account
'''