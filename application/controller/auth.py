from flask import Blueprint, render_template, make_response, redirect, url_for, request, flash, current_app, session
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_jwt_extended import create_access_token

from models.models import User
from models.database import db
from models.validation import ValidationFlash
from models.replacestring import ReplaceString
from models.create_register import CreateRegister
from models.email import SendEmail

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('profile.profile'))

	content = {
		'title': 'login'
	}

	## GET
	if request.method != 'POST':
		
		return make_response(render_template('login.html', content=content))

	## POST
	form_data = request.form

	## Escape
	num_filter_keys = []
	raw_data_keys = []
	clean_data = ReplaceString().clean_form_data(form_data, num_filter_keys, raw_data_keys)

	## remember-me
	remember = True if request.form.get('remember') else False

	validation = ValidationFlash()

	if validation.email(clean_data['user']) == False:
		return redirect(url_for('auth.login'))

	if validation.password(clean_data['password']) == False:
		return redirect(url_for('auth.login'))

	## Check if the user exists in db
	user = User.query.filter_by(user=clean_data['user']).first()

	if not user:
		flash('そのユーザーは存在しません')
		return redirect(url_for('auth.login'))

	## Check the password
	if not check_password_hash(user.password, clean_data['password']):
		flash('パスワードが正しくありません')
		return redirect(url_for('auth.login'))

	## Log the user in
	login_user(user, remember=remember)

	return redirect(url_for('profile.profile'))

@blueprint.route('/pre-signup', methods=['GET', 'POST'])
def pre_signup():

	content = {
		'title': 'pre-signup'
	}

	## GET
	if request.method != 'POST':
		return make_response(render_template('pre_signup.html', content=content))

	## POST
	form_data = request.form

	## Escape
	num_filter_keys = []
	raw_data_keys = []
	clean_data = ReplaceString().clean_form_data(form_data, num_filter_keys, raw_data_keys)

	validation = ValidationFlash()

	user_id = clean_data['user']

	if validation.email(user_id) == False:
		return redirect(url_for('auth.pre_signup'))

	## Check duplication
	if User.query.filter_by(user=user_id).first() is not None:
		flash('このユーザー名は登録済みです')
		return redirect(url_for('auth.login'))
	
	expires = current_app.config['SIGNUP_TOKEN_EXPIRES']
	signup_token = create_access_token(str(user_id), expires_delta=expires)
	signup_url = '{}auth/signup?token={}'.format(request.host_url, signup_token)

	email_data = {
		'user': user_id,
		'subject': 'ユーザー登録',
		'message': '下記のリンクをクリックして、ユーザー登録を完了して下さい。\n{}'.format(signup_url)
	}

	SendEmail().send_email(email_data)
	flash('Eメールを送信しました　１時間以内にユーザー登録して下さい')

	return redirect(url_for('auth.login'))

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():

	content = {
		'title': 'signup',
		'token': request.args.get('token')
	}

	## GET
	if request.method != 'POST':

		return make_response(render_template('signup.html', content=content))

	## POST
	form_data = request.form

	## Get the token from url
	signup_token = request.args.get('token')

	token = CreateRegister().validation_token(signup_token)
	email = token['sub']

	num_filter_keys = []
	raw_data_keys = []
	clean_data = ReplaceString().clean_form_data(form_data, num_filter_keys, raw_data_keys)

	password = clean_data['password']

	validation = ValidationFlash()
	if validation.password(password) == False:
		return make_response(render_template('signup.html', content=content))
	
	if validation.password_confirmation(password, clean_data['password_confirmation']) == False:
		return make_response(render_template('signup.html', content=content))
	
	CreateRegister().user_register(password, email)
	return redirect(url_for('auth.login'))

@blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

	content = {
		'title': 'forgot-password'
	}

	## GET
	if request.method != 'POST':
		return render_template('forgot_password.html', content=content)
	
	## POST
	form_data = request.form

	num_filter_keys = []
	raw_data_keys = []
	clean_data = ReplaceString().clean_form_data(form_data, num_filter_keys, raw_data_keys)

	user_id = clean_data['user']

	if ValidationFlash().email(user_id) == False:
		return redirect(url_for('auth.forgot_password'))
	
	flash('パスワード再設定のリクエストをお受けしました')
	reset_user = User.query.filter_by(user=user_id).first()
	expires = current_app.config['RESET_TOKEN_EXPIRES']
	reset_token = create_access_token(str(reset_user.id), expires_delta=expires)
	reset_password_url = '{}auth/reset-password?token={}'.format(request.host_url, reset_token)

	if reset_user != None:
		email_data = {
			'user': user_id,
			'subject': 'パスワード再設定',
			'message': '下記のリンクをクリックして、パスワード再設定を完了して下さい。\n{}'.format(reset_password_url)
		}
		SendEmail().send_email(email_data)
		flash('Eメールを送信しました　１時間以内に再設定して下さい')

	return redirect(url_for('auth.login'))

@blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

	content = {
		'title': 'reset-password',
		'token': request.args.get('token')
	}

	## GET
	if request.method != 'POST':

		return make_response(render_template('reset_password.html', content=content))

	## POST
	form_data = request.form

	signup_token = request.args.get('token')

	token = CreateRegister().validation_token(signup_token)
	email = token['sub']

	num_filter_keys = []
	raw_data_keys = []
	clean_data = ReplaceString().clean_form_data(form_data, num_filter_keys, raw_data_keys)

	password = clean_data['password']

	validation = ValidationFlash()

	if validation.password(password) == False:
		return make_response(render_template('reset_password.html', content=content))
	
	if validation.password_confirmation(password, clean_data['password_confirmation']) == False:
		return make_response(render_template('reset_password.html', content=content))
	
	CreateRegister().reset_password(password, email)
	return redirect(url_for('auth.login'))

@blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():

	content = {
		'title': 'change-password'
	}

	## GET
	if request.method != 'POST':

		return make_response(render_template('change_password.html', content=content))

	## POST
	form_data = request.form

	num_filter_keys = []
	raw_data_keys = []
	clean_data = ReplaceString().clean_form_data(form_data, num_filter_keys, raw_data_keys)

	password = clean_data['password']

	validation = ValidationFlash()

	if validation.password(password) == False:
		return redirect(url_for('auth.change_password'))
	
	if validation.password_confirmation(password, clean_data['password_confirmation']) == False:
		return redirect(url_for('auth.change_password'))
	
	CreateRegister().reset_password(password, current_user.user)
	return redirect(url_for('auth.login'))

@blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
	session.clear()
	logout_user()
	return redirect(url_for('auth.login'))