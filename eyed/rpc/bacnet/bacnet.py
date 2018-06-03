#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from bacpypes.object import AnalogValueObject
from bacpypes.object import AnalogInputObject

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient
from eyed.driver.bacnet import definition

#
# Database 接続用
#
from eyed.model import BACnetSimulationObject, BACnetSimulationProperty, BACnetSimulationLog
from eyed.db import SessionFactory

#
# BACnet Daemon Instance
#
from eyed.single import SingleBACnetd, DatastoreType

#
# 初期化処理
#
from initialize import addBACnetObject, addBACnetProperty

#
# BACnetService
#
class BACnetService(object):
	#
	# WhoIsRequest の 実行
	#
	def exposed_doWhoIsRequest(self, timeout = 10):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not running...')
		bacnet = BACnetClient(app)

		#
		# WhoIsRequest の 送信
		#
		bacnet.WhoIsRequest()

		#
		# WhoIsRequest を 投げてから最初の IAmRequestを受け取るまで待つ
		#
		try:
			device_id = app.responseQueue.get(timeout = timeout)
			return { 'device_id' : device_id }
		except Exception:
			#
			# タイムアウトを通知
			#
			return None

	#
	# デバイスマップの取得
	#
	def exposed_getDevices(self):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not running...')
		bacnet = BACnetClient(app)

		#
		# デバイスリストの作成
		#
		devices = []
		for key, value in app.device_map.items():
			devices.append({ 'device_id' : key, 'ip' : str(value) })

		#
		# デバイスリストを返却
		#
		return devices

	#
	# ReadPropertyRequest の 実行
	#
	def exposed_doReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')
		bacnet = BACnetClient(app)

		#
		# リクエストの実行
		#
		value = bacnet.ReadPropertyRequest(device_id, object_id, instance_id, property_id)

		#
		# リクエスト結果をJSONで返す
		#
		return { 'value' : value }

	#
	# パラメータの複数読み込みに対応
	#

	#
	# 登録済みオブジェクトの取得
	#
	def exposed_getObjects(self):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# オブジェクト一覧の取得
			#
			objs = session.query(BACnetSimulationObject).all()
			return [obj.to_dict() for obj in objs]

	#
	# オブジェクト の 登録
	#
	def exposed_addObject(self, name, object_id, instance_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')

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
			# オブジェクトの登録
			#
			if addBACnetObject(name, object_id, instance_id) == False:
				return False

			#
			# オブジェクトの登録(DB)
			#
			session.add(BACnetSimulationObject(name, object_id, instance_id))
			session.commit()
			return True

	#
	# オブジェクト の 取得
	#
	def exposed_getObjectByName(self, name):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')
		bacnet = BACnetClient(app)

		#
		# BACnet オブジェクトの検索
		#
		return bacnet.getObjectByName(name)

	#
	# プロパティの追加
	#
	def exposed_addProperty(self, name, property_id, value, type = DatastoreType.STATIC):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')

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
			if addBACnetProperty(obj.name, obj.object_id, obj.instance_id, property_id) == False:
				return False

			#
			# プロパティの登録(DB)
			#
			obj.properties.append(BACnetSimulationProperty(type, property_id, value))
			session.commit()
			return True
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

	#
	# プロパティの取得
	#
	def exposed_getProperty(self, name, property_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')
		bacnet = BACnetClient(app)

		#
		# BACnet オブジェクトの検索
		#
		property = definition.findPropertyByID(property_id)
		if property == None:
			return None
		return bacnet.getProperty(name, property['name'])

	#
	# プロパティの設定
	#
	def exposed_setProperty(self, name, property_id, value):
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
			# プロパティ名が登録されているかを確認
			#
			prop = obj.properties.filter_by(property_id = property_id).first()
			if prop == None: return False

			#
			# Datastore の 取得
			#
			datastore = SingleBACnetd().getDatastore()

			#
			# 値の設定
			#
			datastore.setBACnetValue(
				DatastoreType.STATIC,
				obj.object_id,
				obj.instance_id,
				prop.property_id,
				value
			)
			return True

		#
		# 例外の確認
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

	#
	# プロパティ種別 の 設定
	#
	def exposed_setPropertyType(self, name, property_id, type, value):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')
		bacnet = BACnetClient(app)

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
			# プロパティ名が登録されているかを確認
			#
			prop = obj.properties.filter_by(property_id = property_id).first()
			if prop == None: return False

			#
			# BACnet オブジェクトの検索
			#
			property = definition.findPropertyByID(property_id)
			if property == None:
				return None
			property = bacnet.getProperty(name, property['name'])
			if property == None:
				return None

			#
			# プロパティ種別の設定
			#
			if property.setType(type, value) == False:
				return False

			#
			# プロパティの取得
			#
			return True

		#
		# 例外の確認
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

	#
	# プロパティログの取得
	#
	def exposed_getPropertyLog(self, name, property_id):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# オブジェクト名が既に利用されていないかを確認
			#
			obj = session.query(BACnetSimulationObject).filter_by(name = name).first()
			if obj == None: return None

			#
			# プロパティの取得
			#
			prop = obj.properties.filter_by(property_id = property_id).first()
			if prop == None: return None

			#
			# ログ の 取得
			#
			logs = session.query(BACnetSimulationLog).filter_by(
				object_id = obj.object_id,
				instance_id = obj.instance_id,
				property_id = prop.property_id,
			).all()

			#
			# JSON 出力用の辞書化
			#
			return [log.to_dict() for log in  logs]

#
# Entry Point
#
if __name__ == '__main__':
	obj = definition.findObjectByName('device')
	prs = definition.getPropertiesByObject(obj)

	print obj
	print prs
	pass

