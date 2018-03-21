#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject

#
# TaskGroup の 設定
#
class TaskGroup(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_TASK_GROUP'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	name		= Column('NAME', String)
	interval	= Column('INTERVAL', Integer)

	#
	# リレーション
	#
	bacnetTasks = relationship('BACnetTask', lazy='dynamic', backref = 'taskGroup')

	#
	# コンストラクタ
	#
	def __init__(self, name, interval):
		self.name	= name
		self.interval	= interval

	#
	# 文字列化
	#
	def __str__(self):
		return '<TaskGroup name=%s, interval=%d>' %(self.name, self.interval)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'name'		: self.name,
			'interval'	: self.interval,
		}

#
# BACnetTask の 設定
#
class BACnetTask(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_BACNET_TASK'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True, autoincrement=True)
	device_id	= Column('DEVICE_ID', Integer)
	object_id	= Column('OBJECT_ID', Integer)
	instance_id	= Column('INSTANCE_ID', Integer)
	property_id	= Column('PROPERTY_ID', Integer)

	#
	# 外部キー
	#
	task_group_id = Column('M_TASK_GROUP_ID', Integer, ForeignKey('M_TASK_GROUP.ID'))

	#
	# コンストラクタ
	#
	def __init__(self, device_id, object_id, instance_id, property_id):
		self.device_id = device_id
		self.object_id = object_id
		self.instance_id = instance_id
		self.property_id = property_id

	#
	# 文字列化
	#
	def __str__(self):
		return '<BACnetTask device_id=%d, object_id=%d, instance_id=%d, property_id=%d>' %(
			self.device_id,
			self.object_id,
			self.instance_id,
			self.property_id
		)

