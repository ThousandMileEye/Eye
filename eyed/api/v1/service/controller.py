#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults

#
# API 共通化用
#
from eyed.api.common.response import OK

#
# BACnet デーモン管理用
#
from eyed.single import SingleBACnetd

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
			'alive' : SingleBACnetd.isAlive()
		})

	#
	# BACnetd の 操作
	#
	@view_config(request_method = 'START')
	def start(self):
		return OK({
			'alive' : SingleBACnetd.isAlive()
		})

