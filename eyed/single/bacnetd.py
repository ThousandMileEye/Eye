#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Datastore for BACnetd
#
class Datastore:
	#
	# コンストラクタ
	#
	def __init__(self):
		self.hashmap = dict()

	#
	# 識別子の作成
	#
	def __generateKey(self, cls, key):
		#
		# 鍵の作成
		#
		return '%s:%s' %(cls, key)

	#
	# BACnet プロトコル用の識別子作成
	#
	def getBACnetKey(self, cls, object_id, instance_id, property_id):
		#
		# 鍵の作成
		#
		return self.__generateKey(cls, '%d:%d:%d' %(object_id, instance_id, property_id))

	#
	# BACnet プロトコル値の設定
	#
	def setBACnetValue(self, cls, object_id, instance_id, property_id, value):
		#
		# 鍵を生成しハッシュマップに登録
		#
		key = self.getBACnetKey(
			cls,
			object_id,
			instance_id,
			property_id
		)

		#
		# 価の登録
		#
		self.hashmap[key] = value

	#
	# 値の検索
	#
	def getBACnetValue(self, cls, object_id, instance_id, property_id):
		#
		# ハッシュマップ内から鍵を検索
		#
		key = self.getBACnetKey(
			cls,
			object_id,
			instance_id,
			property_id
		)

		#
		# 識別子の存在確認
		#
		if not key in self.hashmap:
			return None
		return self.hashmap[key]

#
# Datastore 種別
#
class DatastoreType:
	STATIC		= 'STATIC'
	MEASUREMENT	= 'MEASUREMENT'

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
	# get Application
	#
	@classmethod
	def getApplication(cls):
		#
		# BACnetd が 起動しているかを確認
		#
		self = SingleBACnetd().getInstance()
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
		self = SingleBACnetd().getInstance()
		return self.datastore

#
# Test Case
#
if __name__ == '__main__':
	datastore = SingleBACnetd().getDatastore()
	print datastore.set(0, 1, 2, 3, 'Hello')
	print datastore.get(0, 1, 2, 3)

