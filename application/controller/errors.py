from flask import Blueprint, render_template, make_response

blueprint = Blueprint('errors', __name__)

@blueprint.route('/error')
def error_app():

	content = {
		'title': '無効なIDです',
		'msg'  : 'データが削除されたか、無効なIDが指定されました',
		'center': True
	}

	return make_response(render_template('message.html', content=content)), 404

@blueprint.app_errorhandler(400)
def error_400(error):

	content = {
		'title': '400 Bad Request',
		'msg'  : '不正なリクエストです',
		'center': True
	}

	return make_response(render_template('message.html', content=content)), 400

@blueprint.app_errorhandler(404)
def error_404(error):

	content = {
		'title': '404 Not Found',
		'msg'  : 'ページが見つかりませんでした',
		'center': True
	}

	return make_response(render_template('message.html', content=content)), 404

@blueprint.app_errorhandler(413)
def error_413(error):

	content = {
		'title': '413 Request Entity Too Large',
		'msg'  : 'アップロードファイルのサイズが大きすぎます',
		'center': True
	}

	return make_response(render_template('message.html', content=content)), 404