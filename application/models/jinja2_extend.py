from flask import current_app
import os
import re
 
class Jinja2Extend(object):
 
	def staticfile_add_version(self):
 
		def add_version(file_name):
 
			file_name = re.sub('^/', '', file_name)
			file_path = os.path.join(current_app.root_path, file_name)
 
			if os.path.isfile(file_path) == True:
				mtime = str(int(os.stat(file_path).st_mtime))
				return '/{}?ver={}'.format(file_name, str(mtime))
 
		return dict(staticfile_add_version=add_version)