#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

#
# Job Scheduler
#
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

#
# SingleScheduler
#
class SingleScheduler:
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		#
		# スケジューラの設定
		#
		self.scheduler = BackgroundScheduler({
			#
			# スレッドプールの設定
			#
			'apscheduler.executors.default' : {
				'class'		: 'apscheduler.executors.pool:ThreadPoolExecutor',
				'max_workers'	: '256'
			},
			'apscheduler.job_defaults.coalesce'		: 'false',
			'apscheduler.job_defaults.max_instances'	: '1',
			'apscheduler.timezone'				: 'UTC',
		})

	#
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# start
	#
	def start(self):
		#
		# スケジューラの開始
		#
		return self.scheduler.start()

	#
	# addIntervalTask
	#
	def addIntervalTask(self, monitoring_id, interval, callback, args):
		#
		# 定期実行ジョブの追加
		#
		return self.scheduler.add_job(
			callback,
			'interval',
			args,
			id		= monitoring_id,
			seconds		= interval,
			max_instances	= 1
		)

	#
	# getIntervalTaskByID
	#
	def getIntervalTaskByID(self, monitoring_id):
		#
		# ジョブの検索
		#
		return self.scheduler.get_job(monitoring_id)

	#
	# deleteIntervalTaskByID
	#
	def deleteIntervalTaskByID(self, monitoring_id):
		#
		# ジョブの検索
		#
		return self.scheduler.remove_job(monitoring_id)

#
# getAllIntervalTask
#
def getAllIntervalTask(self):
        return self.scheduler.get_jobs()

	#
	# addTaskGroup
	#
	def addTaskGroup(self, name, interval):
		from eyed.monitoring.bacnet import job_bacnet

		#
		# 定期実行ジョブの追加
		#
		self.scheduler.add_job(
			job_bacnet,
			'interval',
			[name],
			name		= name,
			seconds		= interval,
			max_instances	= 1
		)

#
# Entry Point
#
if __name__ == '__main__':
	scheduler = SingleScheduler()
	scheduler.addTaskGroup('ok', 30)
	pass

