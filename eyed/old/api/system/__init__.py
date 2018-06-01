#!/usr/bin/env python
# -*- coding: utf-8 -*-
import network

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.include(network.bootstrap, route_prefix='/network')

#
# Make bootstrap attribute
#
__all__	= [bootstrap]

