#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPRequestTimeout

#
# BACnet Driver
#
from driver.bacnet import BACnetSimpleClient
from driver.bacnet import definition

#
# Validation Tool
#
import jsonschema

#
# BACnet
#
@view_config(route_name='api::bacnet:index', renderer='json')
def index(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)
	return None

#
# BACnet デバイスのスキャン
#
@view_config(route_name='api::bacnet:WhoIsRequest', request_method = 'GET', renderer='json')
def WhoIsRequest(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)

	#
	# Timeout の 取得
	#
	timeout = 10
	if 'timeout' in request.GET and request.GET['timeout'].isdigit():
		timeout = int(request.GET['timeout'])

	#
	# WhoIsRequest の 送信
	#
	bacnet.WhoIsRequest()

	#
	# WhoIsRequest を 投げてから最初の IAmRequestを受け取るまで待つ
	#
	try:
		device_id = app.responseQueue.get(timeout = timeout)
		return HTTPOk(json_body = { 'device_id' : device_id })
	except Exception:
		#
		# タイムアウトを通知
		#
		return HTTPRequestTimeout()

#
# BACnet プロパティの読み込み
#
@view_config(route_name='api::bacnet:ReadPropertyRequest', request_method = 'GET', renderer='json')
def ReadPropertyRequest(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)

	#
	# BACnet Protocol Schema
	#
	BACnet_Schema = {
		'type' : 'object',
		'properties'    : {
			'device_id'	: {
				'type' : 'integer',
			},
			'object_id'	: {
				'type' : 'integer',
			},
			'instance_id'	: {
				'type' : 'integer',
			},
			'property_id'	: {
				'type' : 'integer',
			},
		},
		'required'      : ['device_id', 'object_id', 'instance_id', 'property_id'],
	}

	#
	# JSONの書式確認
	#
	try:
		jsonschema.validate(request.json_body, BACnet_Schema)
	#
	# JSON内のデータ書式に問題がある場合
	#
	except jsonschema.ValidationError as e:
		return HTTPBadRequest(e.message)
	#
	# JSONの書式に問題がある場合
	#
	except ValueError:
		return HTTPBadRequest()

	#
	# ReadPropertyRequest の 送信
	#
	device_id	= request.json_body['device_id']
	object_id	= request.json_body['object_id']
	instance_id	= request.json_body['instance_id']
	property_id	= request.json_body['property_id']

	#device_id	= 123
	#object_id	= 'analogValue'
	#object_id	= 2
	#instance_id	= 6
	#property_id	= 85
	#property_id	= 'presentValue'

	#
	# リクエストの実行
	#
	value = bacnet.ReadPropertyRequest(device_id, object_id, instance_id, property_id)

	#
	# リクエスト結果をJSONで返す
	#
	return { 'value' : value }

#
# BACnet デバイスリストの取得
#
@view_config(route_name='api::bacnet:devices', renderer='json')
def devices(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application

	#
	# デバイスリストの作成
	#
	devices = []
	for key, value in app.device_map.items():
		devices.append({ 'device_id' : key, 'ip' : str(value) })

	#
	# デバイスリストを返却
	#
	return HTTPOk(json_body = devices)

#
# BACnet デバイスリストの取得
#
@view_config(route_name='api::bacnet:device', renderer='json')
def device(request):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = request.registry.bacnetd.application
	bacnet = BACnetSimpleClient(app)

	#
	# デバイスID の 取得
	#
	device_id = request.matchdict['device_id']

	#
	# 型の確認とキャスト
	#
	if str(device_id).isdigit() == False:
		return HTTPBadRequest()
	device_id = int(device_id)

	#
	# デバイスID が あるかを確認
	#
	if not device_id in app.device_map:
		return HTTPNotFound()

	#
	# オブジェクトリスト
	#
	object_list = [
		'vendor-name',
		'vendor-identifier',
		'model-name',
		'firmware-revision',
		'application-software-version',
		'protocol-version',
		'protocol-revision',
		'protocol-services-supported',
		'protocol-object-types-supported',
		'object_list'
	]

	#
	# 各プロパティの取得
	#
	r = {}
	for object_name in object_list:
		r[object_name] = bacnet.getDeviceProperty(object_name, 123)

	#
	# プロパティを返却
	#
	return HTTPOk(json_body = r)

#
# BACnet オブジェクトリストの取得
#
@view_config(route_name='api::bacnet:objects', renderer='json')
def objects(request):
	#
	# オブジェクトリスト の 取得
	#
	object_list = definition.getObjects()
	return object_list

#
# BACnet オブジェクト内 プロパティの取得
#
@view_config(route_name='api::bacnet:object_properties', renderer='json')
def object_properties(request):
	#
	# オブジェクトID の 取得
	#
	object_id = request.matchdict['object_id']
	if str(object_id).isdigit() == False:
		return HTTPBadRequest()
	object_id = int(object_id)

	#
	# オブジェクトID から オブジェクトを検索
	#
	return getPropertiesByObject(findObjectByID(object_id))

#
# BACnet オブジェクトリストの取得
#
@view_config(route_name='api::bacnet:properties', renderer='json')
def properties(request):
	#
	# プロパティリスト の 取得
	#
	property_list = definition.getProperties()
	return property_list

