#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import requests

#
# アクセス用ベースURL
#
url = 'http://127.0.0.1:2018'

class Service(unittest.TestCase):
	def test_start_bacnetd(self):
		response = requests.request(
			'START',
			'%s/api/v1/service/bacnetd/' %(url),
			json = {
				'interface_name'	: 'eth0',
				'device_id'		: 2018
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_stop_bacnetd(self):
		response = requests.request('STOP', '%s/api/v1/service/bacnetd/' %(url))
		self.assertEqual(response.status_code, 200)

