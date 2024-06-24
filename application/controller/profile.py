from flask import Blueprint, render_template, make_response
from flask_login import login_required, current_user

''' Sample
blueprint = Blueprint('main', __name__, static_folder='../../../frontend/dist/assets', template_folder='../../../frontend/dist')

@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
def index(path):
	return render_template('index.html')
'''

blueprint = Blueprint('profile', __name__, url_prefix='/profile')

@blueprint.route('/', methods=['GET'])
@login_required
def profile():

	content = {
		'title': 'profile',
		'user': current_user.user
	}

	return make_response(render_template('profile.html', content=content))