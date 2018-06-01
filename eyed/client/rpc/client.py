#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rpyc
from eyed.driver.bacnet import definition

#
# RPCClient
#
class RPCClient:
	#
	# コンストラクタ
	#
	def __init__(self, host, port = 1413):
		self.connection = rpyc.connect(host, port)
		self.root = self.connection.root

	#
	# VERSION の 取得
	#
	def getVersion(self):
		systemd = self.root.SystemService()
		return systemd.getVersion()

	#
	# NIC の 取得
	#
	def getNetworkInterfaces(self):
		systemd = self.root.SystemService()
		return systemd.getNetworkInterfaces()

#
# BACnetdRPCClient
#
class BACnetdRPCClient(RPCClient):
	#
	# Start
	#
	def start(self, interface, device_id):
		bacnetd = self.root.BACnetdService()
		return bacnetd.start(interface, device_id)

	#
	# getStatus
	#
	def getStatus(self):
		bacnetd = self.root.BACnetdService()
		return bacnetd.getStatus()

	#
	# Stop
	#
	def stop(self):
		bacnetd = self.root.BACnetdService()
		return bacnetd.stop()

#
# BACnetRPCClient
#
class BACnetRPCClient(RPCClient):
	#
	# doReadPropertyRequest
	#
	def doReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		bacnet = self.root.BACnetService()
		return bacnet.doReadPropertyRequest(device_id, object_id, instance_id, property_id)

	#
	# scan
	#
	def scan(self):
		#
		# WhoIsRequest の 実行
		#
		bacnet = self.root.BACnetService()
		return bacnet.doWhoIsRequest()

	#
	# getDevices
	#
	def getDevices(self):
		#
		# デバイス一覧の取得
		#
		bacnet = self.root.BACnetService()
		return bacnet.getDevices()

	#
	# getObjectList
	#
	def getObjectList(self, device_id):
		#
		# オブジェクトID, プロパティID の 取得
		#
		obj = definition.findObjectByName('device')
		prs = definition.findPropertyByName('objectList')

		#
		# リクエスト の 実行
		#
		return self.doReadPropertyRequest(
			device_id,
			obj['id'],
			device_id,
			prs['id']
		)

	#
	# getEpics
	#
	def getEpics(self, device_id):
		#
		# デバイスオブジェクトの全プロパティ取得
		#
		obj = definition.findObjectByName('device')
		prs = definition.getPropertiesByObject(obj)

		#
		# 各プロパティに対してリクエストの実行
		#
		values = dict()
		for p in prs:
			#
			# リクエスト実行
			#
			result = self.doReadPropertyRequest(
				device_id,
				obj['id'],
				device_id,
				p['id']
			)

			#
			# 実行結果を辞書に登録
			#
			values[p['name']] = result['value']
		return values

	#
	# getObjects
	#
	def getObjects(self):
		#
		# オブジェクトの取得
		#
		bacnet = self.root.BACnetService()
		return bacnet.getObjects()

	#
	# getObjectByName
	#
	def getObjectByName(self, name):
		#
		# オブジェクトの取得
		#
		bacnet = self.root.BACnetService()
		return bacnet.getObjectByName(name)

	#
	# addObject
	#
	def addObject(self, name, object_id, instance_id):
		#
		# オブジェクトの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.addObject(name, object_id, instance_id)

	#
	# setProperty
	#
	def addProperty(self, name, property_id):
		#
		# プロパティの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.addProperty(name, property_id)

	#
	# setProperty
	#
	def setProperty(self, name, property_id, value):
		#
		# ポイントの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.setProperty(name, property_id, value)

	#
	# setPropertyType
	#
	def setPropertyType(self, name, property_id, type, value):
		#
		# ポイントの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.setPropertyType(name, property_id, type, value)

	#
	# getProperty
	#
	def getProperty(self, name, property_id):
		#
		# ポイントの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.getProperty(name, property_id)

	#
	# getPropertyLog
	#
	def getPropertyLog(self, name, property_id):
		#
		# ポイントの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.getPropertyLog(name, property_id)

#
# SchedulerRPCClient
#
class SchedulerRPCClient(RPCClient):
	#
	# addTaskGroup
	#
	def addTaskGroup(self, name, interval):
		service = self.root.SchedulerService()
		return service.addTaskGroup(name, interval)

	#
	# getTaskGroup
	#
	def getTaskGroups(self):
		service = self.root.SchedulerService()
		return service.getTaskGroups()

	#
	# addBACnetTask
	#
	def addBACnetTask(self, name, device_id, object_id, instance_id, property_id):
		service = self.root.SchedulerService()
		return service.addBACnetTask(name, device_id, object_id, instance_id, property_id)

	#
	# getBACnetTasks
	#
	def getBACnetTasks(self, name):
		service = self.root.SchedulerService()
		return service.getBACnetTasks(name)

	#
	# getBACnetMeasuredValues
	#
	def getBACnetMeasuredValues(self, task_id):
		service = self.root.SchedulerService()
		return service.getBACnetMeasuredValues(task_id)

#
# Entry Point
#
if __name__ == '__main__':
	#
	# ポイントの登録
	#
	client = BACnetRPCClient('127.0.0.1', 1413)
	prop = client.getProperty('H0', 85)
	print prop
	help(prop)

	#print client.getPropertyLog('T0', 85)
	#client.getObjectByName('H0')

	#client = SchedulerRPCClient('127.0.0.1', 1413)
	#client.addTaskGroup('TEST1', 60)
	#print client.getBACnetTasks('BACNET')
	#print client.getBACnetMeasuredValues(1)

