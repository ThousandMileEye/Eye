#!/usr/bin/env python
# -*- coding: utf-8 -*-
import system

#
# Bootstrap Code
#
def bootstrap(config):
	#
	# Scan controller
	#
	config.include(system.bootstrap, route_prefix='system/')

#
# Make bootstrap attribute
#
__all__ = [bootstrap]

