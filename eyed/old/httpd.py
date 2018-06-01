#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from waitress import serve

#
# デーモンの起動
#
def start():
	#
	# WEB アプリケーションの設定
	#
	config = Configurator()

	#
	# API
	#
	import api.bacnet
	config.include(api.bacnet.bootstrap, route_prefix='api/bacnet/')
	import api.bacnetd
	config.include(api.bacnetd.bootstrap, route_prefix='api/bacnetd/')
	import api.icmp
	config.include(api.icmp.bootstrap, route_prefix='api/icmp/')
	import api.system
	config.include(api.system.bootstrap, route_prefix='api/system/')

	#
	# HTTPDサーバの設定
	#
	app = config.make_wsgi_app()
	serve(app, host='0.0.0.0', port=8888)

#
# Main
#
if __name__ == '__main__':
	start()

