#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from bacpypes.apdu import WhoIsRequest, IAmRequest
from bacpypes.app import BIPSimpleApplication
from bacpypes.service.object import ReadWritePropertyMultipleServices
from Queue import Queue
import sys

#
# App
#
class App(BIPSimpleApplication, ReadWritePropertyMultipleServices):
	def __init__(self, *args):
		#
		# スーパーコンストラクタ呼び出し
		#
		BIPSimpleApplication.__init__(self, *args)

		#
		# BACnet デバイスキャッシュ用
		#
		self.device_map = {}

		#
		# IAmRequest を 受けたデバイスIDを管理するキュー
		#
		self.responseQueue = Queue()

	#
	# デバイスマップ、レスポンスキューのクリア
	#
	def clear(self):
		#self.device_map = {}
		self.responseQueue = Queue()

	#
	# リクエスト の 送信
	#
	def request(self, apdu):
		BIPSimpleApplication.request(self, apdu)

	#
	# レスポンスの確認
	#
	def confirmation(self, apdu):
		BIPSimpleApplication.confirmation(self, apdu)

	#
	# レスポンスの受け取り
	#
	def indication(self, apdu):
		#
		# IAmRequest の 解析
		#
		if isinstance(apdu, IAmRequest):
			#
			# デバイスID, IPアドレスの取得
			#
			ipaddr = apdu.pduSource
			device_type, device_instance = apdu.iAmDeviceIdentifier

			#
			# デバイスID と IPアドレスのマッピング管理
			#
			self.device_map[device_instance] = ipaddr

			#
			# IAmRequest を 取得したことを通知する
			#
			self.responseQueue.put(device_instance)

		#
		# forward it along
		#
		BIPSimpleApplication.indication(self, apdu)

