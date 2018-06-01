#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from driver.icmp import ICMP
import jsonschema

#
# ICMP監視
#
@view_config(route_name='api::icmp:index', request_method = 'POST', renderer='json')
def index(request):
	#
	# ICMP Protocol Schema
	#
	ICMP_Schema = {
		'type'		: 'object',
		'properties'	: {
			'ip'	: {
				'type'	: 'string',
				'oneOf'	: [{ 'format' : 'ipv4' }],
			},
		},
		'required'	: ['ip'],
	}

	#
	# JSONの書式確認
	#
	try:
		jsonschema.validate(request.json_body, ICMP_Schema)

	#
	# JSON内のデータ書式に問題がある場合
	#
	except jsonschema.ValidationError as e:
		return { 'error' : e.message }

	#
	# JSONの書式に問題がある場合
	#
	except ValueError:
		return { 'error' : 'Syntax error...' }

	#
	# 書式確認後のデータを取得
	#
	data = request.json_body

	#
	# ICMP リクエストの送信
	#
	icmp = ICMP(data['ip'])
	return icmp.ping()

