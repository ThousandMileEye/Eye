#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, subprocess
from pyramid.config import Configurator
from waitress import serve

#
# Database の 最新化
#
def init():
        #
        # スクリプトを実行するディレクトリ設定
        #
        base_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_path)

        #
        # DB を 最新のスキーマ へ アップデート
        #
        command = ['alembic upgrade head']
        subprocess.check_call(command, shell=True)

#
# デーモンの起動
#
def start(host = '0.0.0.0', port = 2018):
	#
	# WEB アプリケーションの設定
	#
	config = Configurator()

	#
	# API V1 SYSTEM の 読み込み
	#
	import api.v1.system
	config.include(api.v1.system.bootstrap, route_prefix='api/v1/system/')

	#
	# API V1 SERVICE の 読み込み
	#
	import api.v1.service
	config.include(api.v1.service.bootstrap, route_prefix='api/v1/service/')

	#
	# HTTPDサーバの設定
	#
	app = config.make_wsgi_app()
	serve(app, host=host, port=port)

#
# Main
#
if __name__ == '__main__':
	init()
	start()

