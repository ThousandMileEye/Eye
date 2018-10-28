#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPAddress

#
# BACnet デーモン管理用
#
from eyed.single import SingleBACnetd

#
# BACnet 接続用ドライバ
#
#from eyed.driver.bacnet import BACnetd

#
# Database 接続用
#
#from eyed.model import Config
#from eyed.db import SessionFactory


#
# Start BACnetd
#
#def start_bacnetd(interface, device_id):
#	#
#	# BACnet Daemon が 起動しているか確認
#	#
#	single = SingleBACnetd.getInstance()
#	if not single.bacnetd == None:
#		return False
#
#	#
#	# DB への 接続
#	#
#	with SessionFactory() as session:
#		#
#		# DB から BACNET INTERFACE を取得
#		#
#		bacnet_interface = session.query(Config).filter_by(key = 'BACNET_INTERFACE').first()
#		if interface == None:
#			if bacnet_interface == None: return False
#			interface = bacnet_interface.value
#
#		#
#		# DB から BACNET DEVICE ID を取得
#		#
#		bacnet_device_id = session.query(Config).filter_by(key = 'BACNET_DEVICE_ID').first()
#		if device_id == None:
#			if bacnet_device_id == None: return False
#			device_id = int(bacnet_device_id.value)
#
#		#
#		# NIC の 情報取得
#		#
#		bacnet_address = None
#		try:
#			#
#			# NIC から IPv4 アドレスの取得
#			#
#			iface_data = netifaces.ifaddresses(interface)
#			ipv4 = iface_data.get(netifaces.AF_INET)
#			if not ipv4 == None:
#				prefix = IPAddress(ipv4[0]['netmask']).netmask_bits()
#				bacnet_address = '%s/%d' %(ipv4[0]['addr'], prefix)
#
#		#
#		# NIC の情報が見つからなかった場合の処理
#		#
#		except ValueError:
#			return False
#
#		#
#		# BACnet アドレスが定義されていない場合
#		#
#		if bacnet_address == None:
#			return False
#
#		#
#		# BACnet Daemon の 起動
#		#
#		single.bacnetd = BACnetd(bacnet_address, device_id)
#		single.bacnetd.start()
#
#		#
#		# BACnet Interface を DB に書き込み
#		#
#		if bacnet_interface == None:
#			session.add(Config('BACNET_INTERFACE', interface))
#			session.add(Config('BACNET_DEVICE_ID', device_id))
#		else:
#			bacnet_interface.value = interface
#			bacnet_device_id.value = str(device_id)
#
#		#
#		# コミット
#		#
#		session.commit()
#		return True

#
# BACnetdService
#
class BACnetdService(object):
	#
	# BACnetd サービスの起動
	#
	def exposed_start(self, interface, device_id):
		return start_bacnetd(interface, device_id)

	#
	# BACnetd の 状態確認
	#
	def exposed_getStatus(self):
		#
		# BACnet Daemon が 起動しているか確認
		#
		return SingleBACnetd.isAlive()

	#
	# BACnetd サービスの停止
	#
	def exposed_stop(self):
		#
		# BACnetd の 停止
		#
		return SingleBACnetd.stop()

