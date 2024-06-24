from flask import current_app, request, abort, flash
from cerberus import Validator
from pprint import pprint

class FormValidation(object):

	def __init__(self):

		user_minlength = current_app.config['USERNAME_MINLENGTH']
		user_maxlength = current_app.config['USERNAME_MAXLENGTH']
		password_minlength = current_app.config['PASSWORD_MINLENGTH']
		password_maxlength = current_app.config['PASSWORD_MAXLENGTH']

		schema = {
			'is_set': {
				'empty': False,
				'nullable': False
			},
			'num': {
				'type': 'integer',
				'empty': False,
				'nullable': False,
				'regex': '^\d+$',
			},
			'doc_id': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'regex': '^[a-zA-Z0-9-_]+$',
			},
			'user': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'minlength': user_minlength,
				'maxlength': user_maxlength,
				'regex': '\A[a-z]+\Z',
			},
			'password': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'minlength': password_minlength,
				'maxlength': password_maxlength,
				'regex': '\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]+\Z',
			},
			'url': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'regex': 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
			},
			'date': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'regex': '^\d{4}-\d{2}-\d{2}$',
			},
			'time': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'regex': '^([0-1][0-9]|2[0-3]):[0-5][0-9]$',
			},
			'email': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'regex': "^[\w+\-!.#$%&\'*/=?^`{|}~]+@[\w-]+(\.[\w-]+)+$",
			},
			'is_val_int': {
				'type': 'string',
				'empty': False,
				'nullable': False,
				'regex': "^\d{1}$"
			}
		}

		self.validation = Validator(schema)


	def is_set(self, value):
		return self.validation({'is_set': value})

	def num(self, value):
		return self.validation({'num': value})

	def doc_id(self, value):
		return self.validation({'doc_id': value})

	def user(self, value):
		return self.validation({'user': value})

	def password(self, value):
		return self.validation({'password': value})

	def url(self, value):
		return self.validation({'url': value})

	def date(self, value):
		return self.validation({'date': value})

	def time(self, value):
		return self.validation({'time': value})
	
	def email(self, value):
		return self.validation({'email': value})
	
class ValidationFlash(FormValidation):

	def is_set(self, value):
		if self.validation({'is_set': value}) == False:
			flash('エラー')
			return False
		return True

	def num(self, value):
		if self.validation({'num': value}) == False:
			flash('形式が正しくありません')
			return False
		return True

	def doc_id(self, value):
		if self.validation({'doc_id': value}) == False:
			flash('IDが正しくありません')
			return False
		return True

	def password(self, value):
		if self.validation({'password': value}) == False:
			flash('不正なパスワードです')
			return False
		return True
	
	def user(self, value):
		if self.validation({'user': value}) == False:
			flash('ユーザー名が正しくありません')
			return False
		return True
	
	def email(self, value):
		if self.validation({'email': value}) == False:
			flash('不正なEメールアドレスです')
			return False
		return True
	
	def password_confirmation(self, password, password_confirmation):
		if password != password_confirmation:
			flash('確認用のパスワードが一致していません')
			return False
		return True

class ValidationAbort(FormValidation):

	def is_set(self, value):
		if self.validation({'is_set': value}) == False:
			abort(400)

	def num(self, value):
		if self.validation({'num': value}) == False:
			abort(400)

	def doc_id(self, value):
		if self.validation({'doc_id': value}) == False:
			abort(400)

	def password(self, value):
		if self.validation({'password': value}) == False:
			abort(400, '不正なパスワードです')
	
	def user(self, value):
		if self.validation({'user': value}) == False:
			abort(400, '不正な名前です')
	
	def email(self, value):
		if self.validation({'email': value}) == False:
			abort(400, '不正なEメールアドレスです')

	def is_val_int(self, value):
		if self.validation({'is_val_int': value}) == False:
			return False
		return True

	def post_form_check(self, request):

		data = {}

		if self.validation({'date': request.form['date']}):
			data['date'] = request.form.get('date')

		if self.validation({'time': request.form['time']}):
			data['date'] = request.form.get('date')

		return data
	
	def validate_user_password(self, clean_data):
		if self.validation({'email': clean_data['user']}) == False:
			abort(400, '不正なユーザー名です')
		if self.validation({'password': clean_data['password']}) == False:
			abort(400, '不正なパスワードです')
	
	def validate_user(self, clean_data):
		if self.validation({'email': clean_data['user']}) == False:
			abort(400, '不正なユーザー名です')

	def user_form(self, clean_data):
		if self.validation({'email': clean_data['user']}) == False:
			return False

	def validate_password(self, clean_data):
		if self.validation({'password': clean_data['password']}) == False:
			return False
		
	def validate_int(self, clean_data, target_keys):
		
		for key in target_keys:
			if key not in clean_data:
				abort(400)
			if self.is_val_int(clean_data[key]) == False:
				abort(400)