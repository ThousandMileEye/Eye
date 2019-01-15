#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import Queue

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient

#
# Database 接続用
#
from eyed.model import BACnetSimulationObject, BACnetSimulationProperty
from eyed.db import SessionFactory

#
# BACnet Daemon Instance
#
from eyed.single import SingleBACnetdService
from datastore import DatastoreType
from eyed.single.exception import BACnetdIsNotRunningException
from eyed.single.exception import BACnetDeviceNotFoundException
from property import EyedPresentValue

#
# BACnet Service
#
class SingleBACnetService:
	#
	# get Application
	#
	@classmethod
	def getApplication(cls):
		#
		# BACnetd の 起動状態確認
		#
		if SingleBACnetdService.isAlive() == False:
			raise BACnetdIsNotRunningException()

		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetdService.getApplication()
		if app == None:
			raise BACnetdIsNotRunningException()

		#
		# BACnet 操作クラスを返却
		#
		return BACnetClient(app)

	@classmethod
	def doWhoIsRequest(cls, timeout):
		#
		# BACnet Daemon の インスタンス取得
		#
		bacnet_app = SingleBACnetService.getApplication()

		#
		# WhoIsRequest の 送信
		#
		bacnet_app.WhoIsRequest()

		#
		# IamRequest の 受信待ち
		#
		try:
			return bacnet_app.receiveIamRequest(timeout)
		except Queue.Empty:
			raise BACnetDeviceNotFoundException()

	@classmethod
	def getDevices(cls):
		#
		# BACnet Daemon の インスタンス取得
		#
		bacnet_app = SingleBACnetService.getApplication()

		#
		# デバイスの取得
		#
		devices = []
		for key, value in bacnet_app.application.getDeviceMap().items():
                        devices.append({ 'device_id' : key, 'ip' : str(value) })
		return devices

	@classmethod
	def _addObject(cls, name, object_id, instance_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		bacnet_app = SingleBACnetService.getApplication()

		#
		# オブジェクトの登録
		#
		if bacnet_app.addObject(name, object_id, instance_id) == False:
			return False
		return True

	@classmethod
	def addObject(cls, name, object_id, instance_id):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# オブジェクト名が既に利用されていないかを確認
			#
			obj = session.query(BACnetSimulationObject).filter_by(
				name = name
			).first()
			if not obj == None: return False

			#
			# BACNet Object の 登録
			#
			if cls._addObject(name, object_id, instance_id) == False:
				return False

			#
			# オブジェクトの登録(DB)
			#
			session.add(BACnetSimulationObject(name, object_id, instance_id))
			session.commit()
			return True

	@classmethod
	def _addProperty(cls, name, object_id, instance_id, property_id, type, value):
		#
		# プロパティオブジェクトの定義
		#
		propertyObjects = dict()
		propertyObjects[85] = EyedPresentValue

		#
		# BACnet コマンド操作用インスタンス取得
		#
		bacnet_app = SingleBACnetService.getApplication()

		#
		# プロパティオブジェクト の インスタンス化
		#
		if not property_id in propertyObjects:
			return False
		prop = propertyObjects[property_id](object_id, instance_id)
		#prop.setType(type, value)

		#
		# プロパティ の 登録
		#
		if bacnet_app.addProperty(name, prop) == False:
			return False
		return True

	@classmethod
	def addProperty(cls, name, property_id, value, type = DatastoreType.STATIC):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# オブジェクト名が登録されているかを確認
			#
			obj = session.query(BACnetSimulationObject).filter_by(name = name).first()
			if obj == None: return False

			#
			# プロパティ名が既に存在していないかを確認
			#
			prop = obj.properties.filter_by(property_id = property_id).first()
			if not prop == None: return False

			#
			# プロパティの登録
			#
			if cls._addProperty(obj.name, obj.object_id, obj.instance_id, property_id, type, value) == False:
				return False

			#
			# プロパティの登録(DB)
			#
			obj.properties.append(BACnetSimulationProperty(type, property_id, value))
			session.commit()
			return True

	@classmethod
	def reload(cls):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# BACNet Object の 取得
			#
			objects = session.query(BACnetSimulationObject).all()
			for obj in objects:
				#
				# BACnet Object の 登録
				#
				result = cls._addObject(obj.name, obj.object_id, obj.instance_id)
				if result == False:
					logger.debug(
						'Failed to add BACnet object(name=%s, object_id=%d, instance_id=%d)'
						%(obj.name, obj.object_id, obj.instance_id)
					)

				#
				# BACnet プロパティの取得
				#
				for prop in obj.properties:
					#
					# プロパティの登録
					#
					result = cls._addProperty(
						obj.name,
						obj.object_id,
						obj.instance_id,
						prop.property_id,
						prop.type,
						prop.value
					)
					if result == False:
						logger.debug(
							'Failed to add BACnet property(name=%s, property_id=%d)'
							%(obj.name, prop.property_id)
						)

			#
			# 正常終了
			#
			return True
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

#
# Test Case
#
if __name__ == '__main__':
	pass

