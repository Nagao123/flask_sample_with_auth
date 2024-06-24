
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, init_db, User
from models.jinja2_extend import Jinja2Extend

from controller.profile import blueprint as profile_bp
from controller.auth import blueprint as auth_bp
from controller.errors import blueprint as errors_bp
from api.api_test import blueprint as api_test_bp
from api.auth import blueprint as api_auth_bp

def create_app():

	csrf = CSRFProtect()
	jinja2_ext = Jinja2Extend()

	app = Flask(__name__)
	app.config.from_object('config.Config')

	init_db(app)
	csrf.init_app(app)

	jwt = JWTManager(app)
	
	CORS(app, origins=app.config['ORIGINS'])

	## Initialize flask_login
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	## callback func to load user
	@login_manager.user_loader
	def load_user(user):
		return User.query.get(str(user))
	
	## For css and javascript files
	@app.context_processor
	def add_staticfile():
		return jinja2_ext.staticfile_add_version()

	## app
	app.register_blueprint(profile_bp)
	app.register_blueprint(auth_bp)
	app.register_blueprint(errors_bp)
	app.register_blueprint(api_test_bp)
	app.register_blueprint(api_auth_bp)

	csrf.exempt(profile_bp)
	csrf.exempt(auth_bp)
	csrf.exempt(errors_bp)
	csrf.exempt(api_test_bp)
	csrf.exempt(api_auth_bp)

	return app

app = create_app()
