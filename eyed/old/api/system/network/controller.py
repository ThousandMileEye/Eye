#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPRequestTimeout

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPNetwork

#
# Start BACnetd
#
@view_config(route_name='api::system:network:interfaces', renderer='json')
def interfaces(request):
	#
	# NIC の 情報の取得
	#
	nics = []
	for iface_name in netifaces.interfaces():
		#
		# IPv4, IPv6 アドレスの取得
		#
		iface_data = netifaces.ifaddresses(iface_name)
		ipv4 = iface_data.get(netifaces.AF_INET)
		ipv6 = iface_data.get(netifaces.AF_INET6)

		#
		# NIC の 登録
		#
		nics.append({
			'interface'	: iface_name,
			'ipv4'		: ipv4,
			'ipv6'		: ipv6
		})

	#
	# BACnet Daemon 起動結果を返す
	#
	return HTTPOk(json_body = nics)

