#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyramid.view import view_config, view_defaults

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPNetwork

#
# API 共通化用
#
from eyed.api.common.response import OK

#
# NIC情報の取得用API
#
@view_config(route_name='api::v1:system:network_interfaces', renderer='json')
def network_interfaces(request):
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
		# NIC の 情報をリストに追加
		#
		nics.append({
			'interface'	: iface_name,
			'ipv4'		: ipv4,
			'ipv6'		: ipv6
		})

	#
	# システムのNICの情報をJSON化
	#
	return OK(nics)

