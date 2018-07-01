#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from waitress import serve

#
# デーモンの起動
#
def start(host = '0.0.0.0', port = 2018):
	#
	# WEB アプリケーションの設定
	#
	config = Configurator()

	#
	# API v1 の 読み込み
	#
	import api.v1
	config.include(api.v1.bootstrap, route_prefix='api/v1/')

	#
	# HTTPDサーバの設定
	#
	app = config.make_wsgi_app()
	serve(app, host=host, port=port)

#
# Main
#
if __name__ == '__main__':
	start()

