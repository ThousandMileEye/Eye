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
# BACnet デーモン管理用
#
from eyed.single import SingleBACnetService
from eyed.single import SingleBACnetdService
from eyed.single.exception import BACnetdIsNotRunningException
from eyed.single.exception import BACnetDeviceNotFoundException

#
# 実体の操作
#
@view_defaults(route_name = 'api::v1:service:bacnet:devices', renderer = 'json')
class BACnetDeviceController:
	#
	# コンストラクタ
	#
	def __init__(self, request):
		self.request = request

	#
	# BACnetd の 状態確認
	#
	@view_config(request_method = 'GET')
	def get(self):
		#
		# BACnet デバイスの取得
		#
		try:
			devices = SingleBACnetService.getDevices()
			return OK(devices)
		except BACnetdIsNotRunningException:
			return Error('BACnetdIsNotRunningException')

	#
	# BACnetd の 操作
	#
	@view_config(request_method = 'POST')
	def post(self):
		#
		# JSON の 書式定義
		#
		schema = {
			'type'		: 'object',
			'properties'	: {
				'timeout'	: {
					'type'		: 'integer',
					'default'	: 10
				}
			},
			#
			# 追加の引数を許可しない
			#
			'additionalProperties'  : False
		}

		#
		# 書式チェックの実施
		#
		#try:
		#	jsonschema.validate(self.request.json_body, schema)
		#
		# JSON内のデータ書式に問題がある場合
		#
		#except jsonschema.ValidationError as e:
		#	return Error(e.message)
		#
		# JSONの書式に問題がある場合
		#
		#except ValueError:
		#	return Error('JSON Syntax error...')

		#
		# タイムアウトの取得
		#
		timeout = self.request.json_body['timeout']
		print timeout

		#
		# WhoIsRequest の 送信
		#
		try:
			device = SingleBACnetService.doWhoIsRequest(timeout = 10)
			return OK(device)
		except BACnetdIsNotRunningException:
			return Error('BACnetdIsNotRunningException')
		except BACnetDeviceNotFoundException:
			return Error('BACnetDeviceNotFoundException')

