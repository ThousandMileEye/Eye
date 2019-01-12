#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

#
# Database 接続用
#
from eyed.model import TaskGroup, BACnetMeasuredValue
from eyed.db import SessionFactory

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient

#
# Single Instances
#
from eyed.single import SingleBACnetdService, DatastoreType

#
# 定期実行関数
#
def job_bacnet(name):
	#
	# DB への 接続
	#
	with SessionFactory() as session:
		#
		# オブジェクト一覧の取得
		#
		taskGroup = session.query(TaskGroup).filter_by(name = name).first()
		if taskGroup == None: return

		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetdService.getApplication()
		if app == None: return
		bacnet = BACnetClient(app)

		#
		# Data Store の 取得
		#
		datastore = SingleBACnetdService().getDatastore()

		#
		# タスクの取得
		#
		for task in taskGroup.bacnetTasks:
			#
			# リクエストの実行
			#
			value = bacnet.ReadPropertyRequest(
				task.device_id,
				task.object_id,
				task.instance_id,
				task.property_id
			)

			#
			# 計測値のセットアップ
			#
			datastore.setBACnetValue(
				DatastoreType.MEASUREMENT,
				task.object_id,
				task.instance_id,
				task.property_id,
				value
			)

			#
			# 値の保存
			#
			task.measuredValues.append(BACnetMeasuredValue(value))
			session.commit()

	#
	# 例外の検知
	#
	assert sys.exc_info()[0] == None, sys.exc_info()
	return False

#
# Entry Point
#
if __name__ == '__main__':
	pass

