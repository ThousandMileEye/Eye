#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

#
# Services
#
from eyed.rpc.system import SystemService
from eyed.rpc.bacnet import BACnetService, start_bacnet_emulation
from eyed.rpc.bacnetd import BACnetdService, start_bacnetd
from eyed.rpc.scheduler import SchedulerService, start_scheduler

#
# Alembic による DB の 更新を実行
#
def doAlembicUpgradeHead():
	#
	# スクリプトを実行するディレクトリ設定
	#
	base_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(base_path + '/../')

	#
	# DB を 最新のスキーマ へ アップデート
	#
	command = ['alembic upgrade head']
	subprocess.check_call(command, shell=True)

#
# デーモンの起動
#
def start():
	#
	# 初期化処理
	#
	start_bacnetd(None, None)
	start_bacnet_emulation()
	start_scheduler()

