#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPAddress

#
# 値管理用
#
from datastore import Datastore, DatastoreType

#
# BACnet 接続用ドライバ
#
from eyed.driver.bacnet import BACnetd

#
# Database 接続用
#
from eyed.model import Config
from eyed.db import SessionFactory

#
# Singletone BACnetd
#
class SingleBACnetd:
	#
	# インスタンス保持用変数
	#
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		self.bacnetd = None
		self.datastore = Datastore()

	#
	# get Instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# BACnetd の 起動
	#
	@classmethod
	def start(cls, interface, device_id):
	       #
	       # BACnet Daemon が 起動しているか確認
	       #
	       single = SingleBACnetd.getInstance()
	       if not single.bacnetd == None:
	               return False
	
	       #
	       # DB への 接続
	       #
	       with SessionFactory() as session:
	               #
	               # DB から BACNET INTERFACE を取得
	               #
	               bacnet_interface = session.query(Config).filter_by(key = 'BACNET_INTERFACE').first()
	               if interface == None:
	                       if bacnet_interface == None: return False
	                       interface = bacnet_interface.value
	
	               #
	               # DB から BACNET DEVICE ID を取得
	               #
	               bacnet_device_id = session.query(Config).filter_by(key = 'BACNET_DEVICE_ID').first()
	               if device_id == None:
	                       if bacnet_device_id == None: return False
	                       device_id = int(bacnet_device_id.value)
	
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
	                       return False
	
	               #
	               # BACnet アドレスが定義されていない場合
	               #
	               if bacnet_address == None:
	                       return False
	
	               #
	               # BACnet Daemon の 起動
	               #
	               single.bacnetd = BACnetd(bacnet_address, device_id)
	               single.bacnetd.start()
	
	               #
	               # BACnet Interface を DB に書き込み
	               #
	               if bacnet_interface == None:
	                       session.add(Config('BACNET_INTERFACE', interface))
	                       session.add(Config('BACNET_DEVICE_ID', device_id))
	               else:
	                       bacnet_interface.value = interface
	                       bacnet_device_id.value = str(device_id)
	
	               #
	               # コミット
	               #
	               session.commit()
	               return True

	#
	# BACnetd の 生存確認
	#
	@classmethod
	def isAlive(cls):
		#
		# BACnetd が 起動しているかを確認
		#
		self = SingleBACnetd.getInstance()
		if not self.bacnetd == None:
			return True
		return False

	#
	# BACnetd の 停止
	#
	@classmethod
	def stop(cls):
		#
		# サービスが起動していることを確認
		#
		if SingleBACnetd.isAlive() == False:
		        return False

		#
		# BACnetd の 停止
		#
		single = SingleBACnetd.getInstance()
		single.bacnetd.stop()
		single.bacnetd = None
		return True

	#
	# get Application
	#
	@classmethod
	def getApplication(cls):
		#
		# BACnetd が 起動しているかを確認
		#
		self = SingleBACnetd.getInstance()
		if self.bacnetd == None:
			return None

		#
		# application の インスタンスを返す
		#
		return self.bacnetd.application

	#
	# get Datastore
	#
	@classmethod
	def getDatastore(cls):
		#
		# Datastore の 返却
		#
		self = SingleBACnetd.getInstance()
		return self.datastore

#
# Test Case
#
if __name__ == '__main__':
	pass

