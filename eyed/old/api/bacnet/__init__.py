#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.add_route('api::bacnet:index', '/')
	config.add_route('api::bacnet:WhoIsRequest', '/WhoIsRequest')
	config.add_route('api::bacnet:ReadPropertyRequest', '/ReadPropertyRequest')
	config.add_route('api::bacnet:devices', '/devices/')
	config.add_route('api::bacnet:device', '/devices/{device_id}')
	config.add_route('api::bacnet:objects', '/objects/')
	config.add_route('api::bacnet:object_properties', '/objects/{object_id}/properties/')
	config.add_route('api::bacnet:properties', '/properties/')
	config.scan('.controller')

#
# Make bootstrap attribute
#
__all__	= [bootstrap]

