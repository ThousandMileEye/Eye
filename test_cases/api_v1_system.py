#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import requests

#
# アクセス用ベースURL
#
url = 'http://127.0.0.1:2018'

class System(unittest.TestCase):
	def test_getVersion(self):
		response = requests.get('%s/api/v1/system/version' %(url))
		self.assertEqual(response.status_code, 200)

	def test_getNetworkInterfaces(self):
		response = requests.get('%s/api/v1/system/network_interfaces/' %(url))
		self.assertEqual(response.status_code, 200)

