#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults

#
# JSON Validation
#
import jsonschema

#
# API 共通化用
#
from eyed.api.common.response import OK, Error

#
# BACnet Daemon Instance
#
from eyed.single import SingleScheduler
from eyed.monitoring.http import HTTPMonitoringScheduler

#
# 実体の操作
#
@view_defaults(route_name = 'api::v1:monitoring:http:rest', renderer = 'json')
class MonitoringsConfigrations:
	#
	# コンストラクタ
	#
	def __init__(self, request):
		self.request = request

	#
	# 監視項目の取得
	#
	@view_config(request_method = 'GET')
	def get(self):
		#
		# 監視設定 の 取得
		#
		configs = HTTPMonitoringScheduler.getHTTPMonitoringConfigurations()
		return OK(configs)

	#
	# 監視項目の追加
	#
	@view_config(request_method = 'POST')
	def post(self):
		#
		# JSON の 書式定義
		#
		schema = {
			'type'          : 'object',
			'properties'    : {
				'name' : {
					'type'		: 'string',
					'minLength'	: 2,
				},
				'url' : {
					'type'		: 'string',
					'minLength'	: 2,
				},
				'interval' : {
					'type'		: 'integer',
				}
			},
			#
			# 追加の引数を許可しない
			#
			'additionalProperties'	: False,
			'required'		: ['url', 'interval'],
		}

		#
		# 書式チェックの実施
		#
		try:
			jsonschema.validate(self.request.json_body, schema)
		#
		# JSON内のデータ書式に問題がある場合
		#
		except jsonschema.ValidationError as e:
			return Error(e.message)
		#
		# JSONの書式に問題がある場合
		#
		except ValueError:
			return Error('JSON Syntax error...')

		#
		# リクエストパラメータ取得
		#
		name = self.request.json_body['name']
		url = self.request.json_body['url']
		interval = self.request.json_body['interval']

		#
		# 監視項目の追加
		#
		config = HTTPMonitoringScheduler.addHTTPMonitoringConfiguration(name, url, interval)

		#
		# HTTPプロトコルによる監視の追加
		#
		return OK(config)

#
# 実体の操作
#
@view_defaults(route_name = 'api::v1:monitoring:http:rest-id', renderer = 'json')
class MonitoringsConfigration:
	#
	# コンストラクタ
	#
	def __init__(self, request):
		self.request = request

	#
	# 監視項目の取得
	#
	@view_config(request_method = 'GET')
	def get(self):
		#
		# 監視項目ID の 取得
		#
		id = self.request.matchdict['id']

		#
		# 監視設定 の 取得
		#
		config = HTTPMonitoringScheduler.getHTTPMonitoringConfiguration(id)
		if config == None:
			return Error('ID is not found...')
		return OK(config)

	#
	# 監視項目の取得
	#
	@view_config(request_method = 'DELETE')
	def delete(self):
		#
		# 監視項目ID の 取得
		#
		id = self.request.matchdict['id']

		#
		# 監視設定 の 取得
		#
		result = HTTPMonitoringScheduler.deleteHTTPMonitoringConfiguration(id)
		if result == None:
			return Error('ID is not found...')
		return OK()

