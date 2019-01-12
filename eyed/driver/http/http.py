#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

class HTTP:
	#
	# 初期化処理
	#
	def __init__(self, url):
		self.url = url

	#
	# execute request
	#
	def do(self):
		try:
			response = requests.get(self.url)
			status_code = response.status_code
			return {
				'result'	: True,
				'status_code'	: status_code
			}
		except:
			return {
				'result'	: False,
			}

if __name__ == '__main__':
	http = HTTP('https://www.google.com/')
	print http.do()

