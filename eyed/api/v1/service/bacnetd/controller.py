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
from eyed.single import SingleBACnetdService

#
# 実体の操作
#
@view_defaults(route_name = 'api::v1:service:bacnetd', renderer = 'json')
class BACnetdController:
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
		return OK({
			'alive' : SingleBACnetdService.isAlive()
		})

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
				'interface_name' : {
					'type'		: 'string',
					'minLength'	: 2,
				},
				'device_id' : {
					'type'		: 'integer',
				}
			},
			#
			# 追加の引数を許可しない
			#
			'additionalProperties'	: False,
			'required'		: ['interface_name', 'device_id'],
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
		# Interface name, device_id の 取得
		#
		interface_name	= self.request.json_body['interface_name']
		device_id	= self.request.json_body['device_id']

		#
		# BACnetd の 起動状態確認
		#
		if SingleBACnetdService.isAlive() == True:
			return Error('BACnetd is already running...')

		#
		# BACnetd の 起動
		#
		if SingleBACnetdService.start(interface_name, device_id) == False:
			return Error('Failed to start Bacnetd...')
		return OK()

	#
	# BACnetd の 停止
	#
	@view_config(request_method = 'DELETE')
	def delete(self):
		#
		# BACnetd の 起動状態確認
		#
		if SingleBACnetdService.isAlive() == False:
			return Error('BACnetd is not running...')

		#
		# BACnetd の 停止
		#
		if SingleBACnetdService.stop() == False:
			return Error('Failed to stop Bacnetd...')
		return OK()

