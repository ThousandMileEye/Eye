#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, BOOLEAN, DATETIME, ForeignKey
from sqlalchemy.orm import relationship, backref
from base import BaseObject
from datetime import datetime

#
# 監視設定
#
class HTTPMonitoringConfiguration(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_HTTP_MONITORING_CONFIGRATION'

	#
	# カラム定義
	#
	id		= Column('ID', String, primary_key=True)
	name		= Column('NAME', String)
	url		= Column('URL', String)
	interval	= Column('INTERVAL', Integer)

	#
	# コンストラクタ
	#
	def __init__(self, name, url, interval):
		self.id		= str(uuid.uuid4())
		self.name	= name
		self.url	= url
		self.interval	= interval

	#
	# 文字列化
	#
	def __str__(self):
		return '<HTTPMonitoringConfiguration name=%s, url=%s, interval=%d>' %(self.name, self.url, self.interval)

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'name'		: self.name,
			'url'		: self.url,
			'interval'	: self.interval,
		}

#
# 監視設定
#
class HTTPMeasurementValue(BaseObject):
	#
	# テーブル名
	#
	__tablename__ = 'M_HTTP_MEASUREMENT_VALUE'

	#
	# カラム定義
	#
	id		= Column('ID', Integer, primary_key=True)
	monitoring_id	= Column('MONITORING_ID', String)
	result		= Column('RESULT', BOOLEAN)
	json		= Column('JSON', Integer)
	timestamp	= Column('TIMESTAMP', DATETIME, default=datetime.now)

	#
	# コンストラクタ
	#
	def __init__(self, monitoring_id, result, json):
		self.monitoring_id	= monitoring_id
		self.result		= result
		self.json		= json

	#
	# 辞書化
	#
	def to_dict(self):
		return {
			'id'		: self.id,
			'monitoring_id'	: self.monitoring_id,
			'result'	: self.result,
			'json'		: self.json,
			'timestamp'	: self.timestamp
		}

