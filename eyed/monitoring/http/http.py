#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

#
# Database 接続用
#
from eyed.model import HTTPMonitoringConfiguration, HTTPMeasurementValue
from eyed.db import SessionFactory

#
# BACnet Daemon Instance
#
from eyed.single import SingleScheduler

#
# HTTP Driver
#
from eyed.driver.http import HTTP

#
# 定期実行関数
#
def job_http(id, url):
	#
	# HTTP通信の実施
	#
	http = HTTP(url)

	#
	# リクエストの実行
	#
	r = http.do()
	result = r['result']
	jsonstr = json.dumps(r)

	#
	# DB への 接続
	#
	with SessionFactory() as session:
		value = HTTPMeasurementValue(id, result, jsonstr)
		session.add(value)
		session.commit()

#
# HTTPMonitoringScheduler
#
class HTTPMonitoringScheduler:
	@classmethod
	def addHTTPMonitoringConfiguration(cls, name, url, interval):
		#
		# スケジューラ の 取得
		#
		single_scheduler = SingleScheduler.getInstance()

		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# 監視設定を登録
			#
			config = HTTPMonitoringConfiguration(name, url, interval)
			session.add(config)
			session.commit()

			#
			# タスクが起動しているかを確認
			#
			single_scheduler.addIntervalTask(config.id, config.interval, job_http, [config.id, config.url])
			return config.to_dict()

		#
		# 例外の検知
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

	@classmethod
	def getHTTPMonitoringConfigurations(cls):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# 監視設定の取得
			#
			configs = session.query(HTTPMonitoringConfiguration).all()
			return [config.to_dict() for config in configs]

	@classmethod
	def getHTTPMonitoringConfiguration(cls, id):
		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# 監視設定の取得
			#
			config = session.query(HTTPMonitoringConfiguration).filter_by(id = id).first()
			if config == None:
				return None
			return config.to_dict()

	@classmethod
	def deleteHTTPMonitoringConfiguration(cls, id):
		#
		# スケジューラ の 取得
		#
		single_scheduler = SingleScheduler.getInstance()

		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# 監視設定の取得
			#
			config = session.query(HTTPMonitoringConfiguration).filter_by(id = id).first()
			if config == None:
				return False

			#
			# ジョブの停止とDBからの削除
			#
			single_scheduler.deleteIntervalTaskByID(config.id)
			session.delete(config)
			session.commit()
			return True

		#
		# 例外の検知
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

	@classmethod
	def reload(cls):
		#
		# スケジューラに登録
		#
		single_scheduler = SingleScheduler.getInstance()

		#
		# DB への 接続
		#
		with SessionFactory() as session:
			#
			# 監視設定の取得
			#
			configs = session.query(HTTPMonitoringConfiguration).all()
			for config in configs:
				#
				# タスクが起動しているかを確認
				#
				if single_scheduler.getIntervalTaskByID(config.id) == None:
					single_scheduler.addIntervalTask(config.id, config.interval, job_http, [config.id, config.url])

			#
			# 成功時
			#
			return True

		#
		# 失敗した場合の処理
		#
		assert sys.exc_info()[0] == None, sys.exc_info()
		return False

#
# Entry Point
#
if __name__ == '__main__':
	scheduler = SingleScheduler.getInstance()
	help(scheduler.scheduler)
	pass

