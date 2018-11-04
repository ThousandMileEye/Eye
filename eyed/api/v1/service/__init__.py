#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bacnetd
import bacnet

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.add_route('api::v1:service:bacnetd', '/bacnetd/')
        config.include(bacnetd.bootstrap)
	config.add_route('api::v1:service:bacnet:devices', '/bacnet/devices/')
        config.include(bacnet.bootstrap)

#
# Make bootstrap attribute
#
__all__ = [bootstrap]

