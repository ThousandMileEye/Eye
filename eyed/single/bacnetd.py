#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datastore import Datastore, DatastoreType

#
# Singletone BACnetd
#
class SingleBACnetd:
	#
	# インスタンス保持用変数
	#
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		self.bacnetd = None
		self.datastore = Datastore()

	#
	# get Instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# BACnetd の 生存確認
	#
	@classmethod
	def isAlive(cls):
		#
		# BACnetd が 起動しているかを確認
		#
		self = SingleBACnetd.getInstance()
		if not self.bacnetd == None:
			return True
		return False

	#
	# BACnetd の 停止
	#
	@classmethod
	def stop(cls):
		#
		# サービスが起動していることを確認
		#
		if SingleBACnetd.isAlive() == False:
		        return False

		#
		# BACnetd の 停止
		#
		single = SingleBACnetd.getInstance()
		single.bacnetd.stop()
		single.bacnetd = None
		return True

	#
	# get Application
	#
	@classmethod
	def getApplication(cls):
		#
		# BACnetd が 起動しているかを確認
		#
		self = SingleBACnetd.getInstance()
		if self.bacnetd == None:
			return None

		#
		# application の インスタンスを返す
		#
		return self.bacnetd.application

	#
	# get Datastore
	#
	@classmethod
	def getDatastore(cls):
		#
		# Datastore の 返却
		#
		self = SingleBACnetd.getInstance()
		return self.datastore

#
# Test Case
#
if __name__ == '__main__':
	pass

