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
	# 値の取得
	#
	def getValue(self, key):
		#
		# 識別子の存在確認
		#
		if not key in self.hashmap:
			return None
		return self.hashmap[key]

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
# Test Case
#
if __name__ == '__main__':
	ds = Datastore()

