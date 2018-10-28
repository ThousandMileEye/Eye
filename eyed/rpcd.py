#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

#
# Remote Procedure Call
#
import rpyc
from rpyc.utils.server import ThreadedServer

#
# Services
#
from eyed.rpc.system import SystemService
from eyed.rpc.bacnet import BACnetService
from eyed.rpc.bacnetd import BACnetdService
from eyed.rpc.scheduler import SchedulerService
from eyed.boot import boot

#
# RPCService
#
class RPCService(rpyc.Service):
	exposed_SystemService		= SystemService
	exposed_BACnetdService		= BACnetdService
	exposed_BACnetService		= BACnetService
	exposed_SchedulerService	= SchedulerService

#
# デーモンの起動
#
def start(port = 1413):
	#
	# RPCサーバ の 起動
	#
	server = ThreadedServer(RPCService, port = port)
	server.start()

#
# Entry Point
#
if __name__ == "__main__":
	import logging
	from eyed import logger
	logger.addHandler(logging.StreamHandler())
	logging.basicConfig(level=logging.DEBUG)

	boot.doAlembicUpgradeHead()
	boot.start()
	start()

