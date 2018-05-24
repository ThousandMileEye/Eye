#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, DATETIME, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject
from datetime import datetime

#
# BACnet Simulation Log の 設定
#
class BACnetSimulationLog(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_BACNET_SIMULATION_LOG'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	object_id	= Column('OBJECT_ID', Integer)
	instance_id	= Column('INSTACNE_ID', Integer)
	property_id	= Column('PROPERTY_ID', Integer)
	value		= Column('VALUE', String)
	datetime	= Column('DATETIME', DATETIME, default=datetime.now, nullable=False)

	#
	# コンストラクタ
	#
	def __init__(self, object_id, instance_id, property_id, value):
		self.object_id		= object_id
		self.instance_id	= instance_id
		self.property_id	= property_id
		self.value		= value

	#
	# 文字列化
	#
	def __str__(self):
		return '<BACnetSimulationLog value=%s>' %(self.value)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'object_id'	: self.object_id,
			'instance_id'	: self.instance_id,
			'property_id'	: self.property_id,
			'value'		: self.value,
			'datetime'	: self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
		}

