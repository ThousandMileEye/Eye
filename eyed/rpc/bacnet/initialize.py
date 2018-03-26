#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from eyed.single import SingleBACnetd
from property import EyedPresentValue

#
# オブジェクト の 登録
#
def addBACnetObject(name, object_id, instance_id):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = SingleBACnetd.getApplication()

	#
	# BACnet クライアント の 取得
	#
	bacnet = BACnetClient(app)

	#
	# オブジェクトの登録
	#
	if bacnet.addObject(name, object_id, instance_id) == False:
		return False
	return True

#
# プロパティ の 登録
#
def addBACnetProperty(name, object_id, instance_id, property_id):
	#
	# プロパティオブジェクトの定義
	#
	propertyObjects = dict()
	propertyObjects[85] = EyedPresentValue

	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = SingleBACnetd.getApplication()

	#
	# BACnet クライアント の 取得
	#
	bacnet = BACnetClient(app)

	#
	# プロパティオブジェクト の インスタンス化
	#
	if not property_id in propertyObjects:
		return False
	prop = propertyObjects[property_id](object_id, instance_id)

	#
	# プロパティ の 登録
	#
	if bacnet.addProperty(name, prop) == False:
		return False
	return True

#
# データベースに登録されているポイントの登録
#
def start_bacnet_emulation():
	#
	# DB への 接続
	#
	with SessionFactory() as session:
		#
		# ポイント名が既に利用されていないかを確認
		#
		objects = session.query(BACnetSimulationObject).all()
		for obj in objects:
			#
			# オブジェクト の 登録
			#
			addBACnetObject(obj.name, obj.object_id, obj.instance_id)
			for prop in obj.properties:
				#
				# プロパティの登録
				#
				addBACnetProperty(obj.name, obj.object_id, obj.instance_id, prop.property_id)

if __name__ == '__main__':
	start_bacnet_emulation()

