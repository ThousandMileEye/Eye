#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

#
# get logger
#
from eyed import logger

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
from property import EyedPresentValue

#
# オブジェクト の 登録
#
def addBACnetObject(name, object_id, instance_id):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = SingleBACnetdService.getApplication()

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
def addBACnetProperty(name, object_id, instance_id, property_id, type, value):
	#
	# プロパティオブジェクトの定義
	#
	propertyObjects = dict()
	propertyObjects[85] = EyedPresentValue

	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = SingleBACnetdService.getApplication()

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
	print prop, type, value
	#prop.setType(type, value)

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
			if addBACnetObject(obj.name, obj.object_id, obj.instance_id) == False:
				logger.debug('Failed to add BACnet object(name=%s, object_id=%d, instance_id=%d)' %(obj.name, obj.object_id, obj.instance_id))
			for prop in obj.properties:
				#
				# プロパティの登録
				#
				if addBACnetProperty(obj.name, obj.object_id, obj.instance_id, prop.property_id, prop.type, prop.value) == False:
					logger.debug('Failed to add BACnet property(name=%s, property_id=%d)' %(obj.name, prop.property_id))

		#
		# 正常終了
		#
		return True

	#
	# 例外確認要
	#
	assert sys.exc_info()[0] == None, sys.exc_info()
	return False

#
# Entry Point
#
if __name__ == '__main__':
	start_bacnet_emulation()

