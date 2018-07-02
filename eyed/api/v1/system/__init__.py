#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.add_route('api::v1:system:version', '/version')
	config.add_route('api::v1:system:network_interfaces', '/network_interfaces/')
	config.scan('.controller')

#
# Make bootstrap attribute
#
__all__ = [bootstrap]

