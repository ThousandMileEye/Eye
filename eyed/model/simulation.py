#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, DATETIME, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject
from datetime import datetime

#
# BACnet Simulation Object の 設定
#
class BACnetSimulationObject(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_BACNET_SIMULATION_OBJECT'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	name		= Column('NAME', String)
	object_id	= Column('OBJECT_ID', Integer)
	instance_id	= Column('INSTACNE_ID', Integer)

	#
	# リレーション
	#
	properties = relationship('BACnetSimulationProperty', lazy='dynamic', backref = 'object', cascade = 'save-update')

	#
	# コンストラクタ
	#
	def __init__(self, name, object_id, instance_id):
		self.name		= name
		self.object_id		= object_id
		self.instance_id	= instance_id

	#
	# 文字列化
	#
	def __str__(self):
		return '<SimulationObject name=%s, object_id=%d, instance_id=%d>' %(self.name, self.object_id, self.instance_id)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'name'		: self.name,
			'object_id'	: self.object_id,
			'instance_id'	: self.instance_id,
			'properties'	: [prop.to_dict() for prop in self.properties]
		}

#
# BACnet Simulation Property の 設定
#
class BACnetSimulationProperty(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_BACNET_SIMULATION_PROPERTY'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	type		= Column('TYPE', String)
	property_id	= Column('PROPERTY_ID', Integer)
	value		= Column('VALUE', String)

	#
	# 外部キー
	#
	emulation_object_id = Column('SIMULATION_POINT_ID', Integer, ForeignKey('M_BACNET_SIMULATION_OBJECT.ID'))

	#
	# コンストラクタ
	#
	def __init__(self, type, property_id, value):
		self.type = type
		self.property_id = property_id
		self.value = value

	#
	# 文字列化
	#
	def __str__(self):
		return '<BACnetProperty type=%s property_id=%d>' %(self.type, self.property_id)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'type'		: self.type,
			'property_id'	: self.property_id,
			'value'		: self.value
		}

