#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.add_route('api::system:network:interfaces', '/interfaces')
	config.scan('.controller')

#
# Make bootstrap attribute
#
__all__	= [bootstrap]

