#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from initialize import addTaskGroup

#
# Database 接続用
#
from eyed.model import TaskGroup, BACnetTask, BACnetMeasuredValue
from eyed.db import SessionFactory

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient

#
# Single Instances
#
from eyed.single import SingleBACnetdService

#
# SchedulerService
#
class SchedulerService(object):
	#
	# 測定周期の追加
	#
	def exposed_addTaskGroup(self, name, interval):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# グループ名が既に登録されていないかを確認
			#
			if not session.query(TaskGroup).filter_by(name = name).first() == None:
				return False

			#
			# タスクグループの追加
			#
			addTaskGroup(name, interval)

			#
			# タスクグループの登録
			#
			session.add(TaskGroup(name, interval))
			session.commit()
			return True

	#
	# タスクグループ の 取得
	#
	def exposed_getTaskGroups(self):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# タスクグループの取得
			#
			taskGroups = [taskGroup.to_dict() for taskGroup in session.query(TaskGroup).all()]
			return taskGroups

	#
	# 測定周期の追加
	#
	def exposed_addBACnetTask(self, name, device_id, object_id, instance_id, property_id):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# グループ名が存在するかの確認
			#
			taskGroup = session.query(TaskGroup).filter_by(name = name).first()
			if taskGroup == None: return False

			#
			# タスクが登録済みであるかを確認
			#
			task = taskGroup.bacnetTasks.filter_by(
				device_id = device_id,
				object_id = object_id,
				instance_id = instance_id,
				property_id = property_id
			).first()
			if not task == None: return False

			#
			# BACnet コマンド操作用インスタンス取得
			#
			app = SingleBACnetdService.getApplication()
			if app == None: return False
			bacnet = BACnetClient(app)

			#
			# 値が取得できるかを確認
			#
			value = bacnet.ReadPropertyRequest(device_id, object_id, instance_id, property_id)
			if value == None: return False

			#
			# タスクの登録
			#
			new_task = BACnetTask(device_id, object_id, instance_id, property_id)
			taskGroup.bacnetTasks.append(new_task)
			session.commit()
			return True

	#
	# 測定タスクの取得
	#
	def exposed_getBACnetTasks(self, name):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# タスクグループの取得
			#
			taskGroup = session.query(TaskGroup).filter_by(name = name).first()
			if taskGroup == None:
				return []

			#
			# タスク情報の辞書化
			#
			tasks = [task.to_dict() for task in taskGroup.bacnetTasks]
			return tasks

		#
		# 例外の確認
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return []

	#
	# 測定データの表示
	#
	def exposed_getBACnetMeasuredValues(self, task_id):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# タスクの取得
			#
			query = session.query(BACnetMeasuredValue).filter_by(task_id = task_id)
			values = [value.to_dict() for value in query.all()]
			return values

		#
		# 例外の確認
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return []

