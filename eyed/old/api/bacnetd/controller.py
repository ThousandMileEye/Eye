#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPRequestTimeout

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPAddress

#
# BACnet 接続用ドライバ
#
from driver.bacnet import BACnetd
from driver.bacnet import BACnetSimpleClient

#
# Start BACnetd
#
@view_config(route_name='api::bacnetd:start', renderer='json')
def start(request):
	#
	# NIC の 情報を取得
	#
	interface = 'lo0'
        if 'interface' in request.GET:
		interface = request.GET['interface']

	#
	# NIC の 情報取得
	#
	bacnet_address = None
	try:
		#
		# NIC から IPv4 アドレスの取得
		#
		iface_data = netifaces.ifaddresses(interface)
		ipv4 = iface_data.get(netifaces.AF_INET)
		if not ipv4 == None:
			prefix = IPAddress(ipv4[0]['netmask']).netmask_bits()
			bacnet_address = '%s/%d' %(ipv4[0]['addr'], prefix)
	#
	# NIC の情報が見つからなかった場合の処理
	#
	except ValueError:
		return HTTPBadRequest()

	#
	# BACnet アドレスが定義されていない場合
	#
	if bacnet_address == None:
		return HTTPBadRequest()

	#
	# BACnet Daemon が 起動しているか確認
	#
	if request.registry.bacnetd == None:
		#
		# BACnet Daemon の 起動
		#
		request.registry.bacnetd = BACnetd(bacnet_address)
		request.registry.bacnetd.start()

	#
	# BACnet Daemon 起動結果を返す
	#
	return HTTPOk()

