#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BACnetdIsNotRunningException(Exception):
	pass

#
# BACnet Device が 見つからなかった場合の例外
#
class BACnetDeviceNotFoundException(Exception):
	pass

