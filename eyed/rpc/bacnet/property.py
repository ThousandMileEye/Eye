#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.primitivedata import Real
from bacpypes.object import Property
from bacpypes.errors import ExecutionError

from eyed.single import SingleBACnetdService, DatastoreType

#
# Database 接続用
#
from eyed.model import BACnetSimulationLog, BACnetMeasuredValue, BACnetTask
from eyed.db import SessionFactory

#
# Eyed Present Value
#
class EyedPresentValue(Property):
	#
	# コンストラクタ
	#
	def __init__(self, object_id, instance_id, default_value = 0, type = DatastoreType.STATIC):
		#
		# 各識別子の定義
		#
		self.key		= None
		self.type		= type
		self.object_id		= object_id
		self.instance_id	= instance_id
		self.property_id	= 85
		self.identifier		= 'presentValue'

		#
		# スーパクラスのコンストラクタ呼び出し
		#
		Property.__init__(
			self,
			self.identifier,
			Real,
			default=0.0,
			optional=True,
			mutable=False
		)

		#
		# 初期値のセットアップ
		#
		self.setType(type, default_value)

	#
	# 読み込み
	#
	def ReadProperty(self, obj, arrayIndex=None):
		#
		# Access an array
		#
		if arrayIndex is not None:
			raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')

		#
		# キャッシュに値があれば、キャシュの値を返す
		#
		datastore = SingleBACnetdService().getDatastore()
		value = datastore.getValue(self.key)

		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# DBへの登録
			#
			session.add(BACnetSimulationLog(self.object_id, self.instance_id, self.property_id, value))
			session.commit()

		#
		# 値の返却
		#
		if not value == None:
			return value
		raise ExecutionError(errorClass='property', errorCode='abortProprietary')

	#
	# 書き込み
	#
	def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
		raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')

	#
	# プロパティ種別の変更
	#
	def setType(self, type, value):
		#
		# プロパティ種別の設定
		#
		self.type = type
		datastore = SingleBACnetdService().getDatastore()

		#
		# プロパティ種別が「STATIC」の場合
		#
		if type == DatastoreType.STATIC:
			#
			# 鍵の取得
			#
			self.key = datastore.getBACnetKey(
				DatastoreType.STATIC,
				self.object_id,
				self.instance_id,
				self.property_id,
			)

			#
			# 初期値の設定
			#
			datastore.setBACnetValue(
				DatastoreType.STATIC,
				self.object_id,
				self.instance_id,
				self.property_id,
				value
			)
			return True
		#
		# プロパティ種別が「MEASUREMENT」の場合
		#
		else:
			#
			# DB への 接続
			#
			with SessionFactory() as session:
				#
				# タスクの確認
				#
				task = session.query(BACnetTask).filter_by(id = value).first()

				#
				# 鍵の取得
				#
				self.key = datastore.getBACnetKey(
					DatastoreType.MEASUREMENT,
					task.object_id,
					task.instance_id,
					task.property_id,
				)
			return True
		return False

