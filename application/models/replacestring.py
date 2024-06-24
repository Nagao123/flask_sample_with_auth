from markupsafe import escape
import re
import pykakasi
from unicodedata import normalize


class ReplaceString:

	def remove_all_space(self, text):
		return re.sub('(\s|\t|　)', '', text)

	def remove_newline(self, text):
		return re.sub('(\n|\r|\r\n)', '', text)

	def remove_not_num(self, text):
		return re.sub('[^\d]', '', text)

	def remove_escape_str(self, text):
		return re.sub('(&#39;|\s|\[|\])', '', text)


	## ハイフンと間違いやすい記号を変換、Unicodeで指定
	def convert_adress_hyphen(self, text):
		return re.sub('(\d)(\\u30fc|\\u2010|\\u2011|\\u2013|\\u2014|\\u2015|\\u2212|\\uff70)', '\\1-', text)

	## 建物名を省いて部屋番号を書いてくるケースへの対応処理
	def convert_num_space2hyphen(self, text):
		return re.sub('(\d)(\s|\t|　)+(\d)', '\\1-\\3', text)

	def to_kana(self, text):

		kana = ''
		kakasi = pykakasi.kakasi()

		for kks in kakasi.convert(text):
			kana += kks['kana']
		return kana

	def to_agerange(self, text):

		age = str(text)
		if age == '':
			return ''

		## age: 10 - 99
		if re.match('^\d{2}$', age):
			return '{}0代'.format(age[0:1])

		else:
			return 'その他'

	def filter_text(self, text):
		filtere_text = self.remove_newline(text)
		filtere_text = self.remove_all_space(filtere_text)
		return normalize('NFKC', filtere_text)

	def filter_num(self, text):
		filtere_text = self.remove_newline(text)
		filtere_text = self.remove_all_space(filtere_text)
		filtere_text = normalize('NFKC', filtere_text)
		return self.remove_not_num(filtere_text)

	def join_adress(self, address1, address2):

		input_adress = '{} {}'.format(address1, address2)

		## ex: 巣鴨1-2-3 123号室 -> 巣鴨1-2-3-123号室
		full_adress = self.convert_num_space2hyphen(input_adress)
		return self.remove_all_space(full_adress)
	
	def clean_form_data(self, data, num_filter_keys, raw_data_keys):

		clean_data = {}

		for key in data.keys():

			escaped_strings = str(escape(data[key]))

			if key in num_filter_keys:
				clean_data[key] = self.filter_num(escaped_strings)
			
			elif key in raw_data_keys:
				clean_data[key] = escaped_strings
			
			else:
				clean_data[key] = self.filter_text(escaped_strings)
			
		return clean_data