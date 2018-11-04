#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, subprocess
from pyramid.config import Configurator
from waitress import serve
from eyed.boot import boot

#
# デーモンの起動
#
def start_httpd(host = '0.0.0.0', port = 2018):
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
        #
        # ログレベルの設定
        #
        import logging
        from eyed import logger
        logger.addHandler(logging.StreamHandler())
        logging.basicConfig(level=logging.DEBUG)

	boot.doAlembicUpgradeHead()
	boot.start()
	start_httpd()

