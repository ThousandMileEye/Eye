#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# BACnet デーモン管理用
#
from eyed.single import SingleBACnetdService

#
# BACnetdService
#
class BACnetdService(object):
	#
	# BACnetd サービスの起動
	#
	def exposed_start(self, interface_name, device_id):
		return SingleBACnetdService.start(interface_name, device_id)

	#
	# BACnetd の 状態確認
	#
	def exposed_getStatus(self):
		return SingleBACnetdService.isAlive()

	#
	# BACnetd サービスの停止
	#
	def exposed_stop(self):
		return SingleBACnetdService.stop()

