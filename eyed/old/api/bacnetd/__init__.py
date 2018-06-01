#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# BACnet デーモンの管理用変数
	#
	config.registry.bacnetd = None

	#
	# Scan controller
	#
	config.add_route('api::bacnetd:status', '/status')
	config.add_route('api::bacnetd:start', '/start')
	config.scan('.controller')

#
# Make bootstrap attribute
#
__all__	= [bootstrap]

