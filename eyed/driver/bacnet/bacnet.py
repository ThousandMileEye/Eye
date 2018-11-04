#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.apdu import WhoIsRequest, ReadPropertyRequest, ReadPropertyACK
from bacpypes.object import get_object_class, get_datatype
from bacpypes.object import ObjectType, registered_object_types
from bacpypes.basetypes import PropertyIdentifier
from eyed.driver.bacnet import definition

#
# BACnet Client
#
class BACnetClient:
	#
	# BACnetClient 初期化処理
	#
	def __init__(self, application, auto_device_discovery = True):
		#
		# アプリケーションの取得
		#
		self.application = application

		#
		# デバイス の 探索を自動で実行するか？
		#
		self.auto_device_discovery = auto_device_discovery

	#
	# getAddressByDeviceID
	#
	def getAddressByDeviceID(self, device_id):
		#
		# デバイスマップの返却
		#
		device_map = self.application.getDeviceMap()
		if device_id in device_map:
			return device_map[device_id]
		return None

	#
	# WhoIsRequest
	#
	def WhoIsRequest(self, low_limit = 1, high_limit = 65535):
		#
		# WhoIsRequest の レスポンス(IAmRequest) を保存するキューをクリア
		#
		#self.application.clear()

		#
		# WhoIsRequest の 送信
		#
		self.application.who_is(low_limit, high_limit, GlobalBroadcast())
		return True

	#
	# IamRequest の 受信待ち
	# - 例外: Empty (タイムアウト時)
	#
	def receiveIamRequest(self, timeout):
		#
		# タイムアウト秒の間受信待ち
		#
		device_queue = self.application.getDeviceQueue()
		device_id = device_queue.get(timeout = timeout)
		return { 'device_id' : device_id }

	#
	# ReadProperty
	#
	def _ReadPropertyRequest(self, device_id, objectIdentifier, propertyIdentifier):
		#
		# デバイスID から IPの取得
		#
		address = self.getAddressByDeviceID(device_id)
		if not address:
			#
			# デバイスの探索オプションの確認
			#
			if self.auto_device_discovery == False:
				return None

			#
			# デバイスの探索
			#
			self.WhoIsRequest()

		#
		# リクエスト作成
		#
		request = ReadPropertyRequest(
			destination		= address,
			objectIdentifier	= objectIdentifier,
			propertyIdentifier	= propertyIdentifier,
		)

		#
		# リクエストを送信 & 結果取得待ち
		#
		iocb = IOCB(request)
		self.application.request_io(iocb)
		iocb.wait()

		#
		# エラーがあるかを確認
		#
		if iocb.ioError:
			return None

		#
		# レスポンスの確認
		#
		elif iocb.ioResponse:
			#
			# レスポンスデータの取得
			#
			apdu = iocb.ioResponse

			#
			# ACKであるかの確認
			#
			if not isinstance(apdu, ReadPropertyACK):
				print 'ACK is not contain...'
				return None

			#
			# データタイプの取得
			#
			datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
			if not datatype:
				print 'Unknown datatype...'
				return None

			#
			# データ種別と値の取得
			#
			return apdu, datatype

		#
		# 例外
		#
		else:
			print 'Response seems something wrong...'
			return None

	#
	# ReadProperty
	#
	def ReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		#
		# リクエストの作成
		#
		result = BACnetClient._ReadPropertyRequest(
			self,
			device_id		= device_id,
			objectIdentifier	= (object_id, instance_id),
			propertyIdentifier	= property_id
		)

		#
		# レスポンスの確認
		#
		if result == None:
			return None

		#
		# キャスト
		#
		apdu, datatype = result
		return apdu.propertyValue.cast_out(datatype)

	#
	# ReadDeviceProperty (デバイス関連の情報読み出し)
	#
	def _ReadDevicePropertyRequest(self, device_id, propertyIdentifier):
		#
		# リクエストの作成
		#
		result = BACnetClient._ReadPropertyRequest(
			self,
			device_id		= device_id,
			objectIdentifier	= ('device', device_id),
			propertyIdentifier	= propertyIdentifier
		)

		#
		# レスポンスの確認
		#
		if result == None:
			return None

		#
		# キャスト
		#
		apdu, datatype = result
		return apdu.propertyValue.cast_out(datatype)

	#
	# addObject (オブジェクト の 登録)
	#
	def addObject(self, name, object_id, instance_id):
		#
		# BACnetd の 動作確認
		#
		if self.application == None:
			raise Exception('BACnetd is not running...')

		#
		# オブジェクト識別子の取得
		#
		objectIdentifier = self.getObjectIdentifier(object_id, instance_id)
		if objectIdentifier == None:
			return False

		#
		# オブジェクトクラス の 取得
		#
		Object = definition.findObjectClassByType(objectIdentifier[0])

		#
		# オブジェクト の 定義
		#
		new_object = Object(
			objectName              = name,
			objectIdentifier        = objectIdentifier,
		)

		#
		# オブジェクト の 登録
		#
		self.application.add_object(new_object)
		return True

	#
	# addProperty (プロパティ の 登録)
	#
	def addProperty(self, name, property_instance):
		#
		# BACnetd の 動作確認
		#
		if self.application == None:
			raise Exception('BACnetd is not running...')

		#
		# オブジェクトを名前から検索
		#
		obj = self.application.get_object_name(name)
		if obj == None: return False

		#
		# プロパティの登録
		#
		obj.add_property(property_instance)
		return True

	#
	# getProperty (プロパティ の 登録)
	#
	def getProperty(self, name, property_name):
		obj = self.getObjectByName(name)
		return obj._properties.get(property_name)

	#
	# getObjectByID (オブジェクト の 取得)
	#
	def getObjectIdentifier(self, object_id, instance_id):
		#
		# オブジェクト識別子の作成
		#
		obj_type = definition.findObjectByID(object_id)
		if obj_type == None:
			return None
		objectType = obj_type['name']

		#
		# オブジェクト識別子の作成
		#
		return (objectType, instance_id)

	#
	# getObjectByID (オブジェクト の 取得 [ID 検索])
	#
	def getObjectByID(self, objectIdentifier, instance_id):
		#
		# BACnetd の 動作確認
		#
		if self.application == None:
			raise Exception('BACnetd is not running...')

		#
		# 登録されているオブジェクトの検索
		#
		return self.application.get_object_id((objectIdentifier, instance_id))

	#
	# getObjectByName (オブジェクト の 取得 [名前で検索])
	#
	def getObjectByName(self, name):
		#
		# BACnetd の 動作確認
		#
		if self.application == None:
			raise Exception('BACnetd is not running...')

		#
		# オブジェクトを名前から検索
		#
		return self.application.get_object_name(name)

