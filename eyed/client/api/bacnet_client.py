#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from eyed.driver.bacnet import definition
from client import Client
import requests

#
# BACnetdClient
#
class BACnetdClient(Client):
	#
	# BACnet Daemon 起動
	#
	def start(self, interface_name, device_id = 2018):
		#
		# URLの組立
		#
		url = '%s/api/v1/service/bacnetd/' %(self.base_url)

		#
		# BACnet デバイス取得リクエスト送信
		#
		result = requests.post(url, json = {
			'interface_name'	: interface_name,
			'device_id'		: device_id
		}).json()

		#
		# 結果の確認
		#
		if result['ok'] == True: return True
		return False

#
# BACnetClient
#
class BACnetClient(Client):
	#
	# BACnet デバイスのスキャン
	#
	def WhoIsRequest(self, timeout = 3):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/WhoIsRequest?timeout=%d' %(self.base_url, timeout)

		#
		# BACnet デバイス取得リクエスト送信
		#
		result = requests.get(url)

		#
		# 結果の確認
		#
		if result.status_code == 200:
			return True
		return False

	#
	# BACnet プロパティの読み込み
	#
	def ReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/ReadPropertyRequest' %(self.base_url)

		#
		# BACnet デバイス取得リクエスト送信
		#
		result = requests.get(url, json = {
			'device_id'	: device_id,
			'object_id'	: object_id,
			'instance_id'	: instance_id,
			'property_id'	: property_id,
		})

		#
		# 結果の確認
		#
		if result.status_code == 200:
			return result.json()
		return False

	#
	# 別名の登録
	#
	scanDevices = WhoIsRequest

	#
	# BACnet デバイスの取得
	#
	def getDevices(self):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/devices/' %(self.base_url)

		#
		# BACnet デバイス取得リクエスト送信
		#
		result = requests.get(url)

		#
		# 結果の確認
		#
		if result.status_code == 200:
			return result.json()
		return False

	#
	# BACnet デバイスの検索
	#
	def getDevice(self, device_id):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/devices/%s' %(self.base_url, device_id)

		#
		# BACnet デバイス検索リクエストの送信
		#
		result = requests.get(url)
		if result.status_code == 200:
			return result.json()
		return None

	#
	# デバイスの情報取得
	#
	def bacepics(self, device_id):
		obj = definition.findObjectByName('device')
		prs = definition.getPropertiesByObject(definition.findObjectByName('device'))

		values = dict()
		for p in prs:
			result = self.ReadPropertyRequest(device_id, obj['id'], device_id, p['id'])
			values[p['name']] = result['value']
		return values

#
# Entry Point
#
if __name__ == '__main__':
	#client = ICMPClient('localhost', '8888')
	#print client.ping('8.8.8.8')

	#
	# BACnetd の 起動
	#
	client = BACnetdClient('localhost', '2018')
	print client.start(interface_name = 'en1')

	#
	# BACnet 通信の実行
	#
	client = BACnetClient('localhost', '2018')

	print client.scanDevices()

	#print client.bacepics(123)
	#print client.ReadPropertyRequest(123, 2, 6, 85)

