#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# BACnet デーモン管理用
#
from eyed.single import SingleBACnetd

#
# BACnetdService
#
class BACnetdService(object):
	#
	# BACnetd サービスの起動
	#
	def exposed_start(self, interface, device_id):
		return SingleBACnetd.start(interface, device_id)

	#
	# BACnetd の 状態確認
	#
	def exposed_getStatus(self):
		return SingleBACnetd.isAlive()

	#
	# BACnetd サービスの停止
	#
	def exposed_stop(self):
		return SingleBACnetd.stop()

