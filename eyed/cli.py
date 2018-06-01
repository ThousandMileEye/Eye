#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from eyed.client.rpc import RPCClient
from eyed.client.rpc import BACnetRPCClient
from eyed.client.rpc import BACnetdRPCClient
from eyed.client.rpc import SchedulerRPCClient

#########################################################################
# 引数処理
#########################################################################
@click.group()
@click.option('--host', '-h', default = '127.0.0.1')
@click.option('--port', '-p', default = 1413)
@click.pass_context
def cmd(ctx, host, port):
	ctx.obj['host'] = host
	ctx.obj['port'] = port

#########################################################################
# パラメータ の 追加
#########################################################################
@cmd.group()
@click.pass_context
def add(ctx):
	pass

#########################################################################
# 測定グループ の 定義
#########################################################################
@add.group(name = 'measurement')
@click.pass_context
def add_measurement(ctx):
	pass

#########################################################################
# 測定グループ の 定義
#########################################################################
@add_measurement.command(name = 'taskgroup')
@click.pass_context
@click.argument('name')
@click.argument('interval')
def add_measurement_taskgroup(ctx, name, interval):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = SchedulerRPCClient(host, port)
	click.echo(client.addTaskGroup(name, int(interval)))

#########################################################################
# 測定タスクの追加
#########################################################################
@add_measurement.group(name = 'task')
@click.pass_context
def add_measurement_task(ctx):
	pass

#########################################################################
# BACnet測定タスクの追加
#########################################################################
@add_measurement_task.command(name = 'bacnet')
@click.pass_context
@click.argument('name')
@click.argument('device_id')
@click.argument('object_id')
@click.argument('instance_id')
@click.argument('property_id')
def add_measurement_task_bacnet(ctx, name, device_id, object_id, instance_id, property_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = SchedulerRPCClient(host, port)
	click.echo(client.addBACnetTask(
		name,
		int(device_id),
		int(object_id),
		int(instance_id),
		int(property_id)
	))

#########################################################################
# シミュレーションパラメータ の 定義
#########################################################################
@add.group(name = 'simulation')
@click.pass_context
def add_simulation(ctx):
	pass

#########################################################################
# プロトコル の 定義
#########################################################################
@add_simulation.group(name = 'bacnet')
@click.pass_context
def add_simulation_bacnet(ctx):
	pass

#########################################################################
# BACnet オブジェクト の 定義
#########################################################################
@add_simulation_bacnet.command(name = 'object')
@click.pass_context
@click.argument('name')
@click.argument('object_id')
@click.argument('instance_id')
def add_simulation_bacnet_object(ctx, name, object_id, instance_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.addObject(
		name,
		int(object_id),
		int(instance_id),
	))

#########################################################################
# パラメータ の 定義
#########################################################################
@add_simulation_bacnet.command(name = 'property')
@click.pass_context
@click.argument('name')
@click.argument('property_id')
def add_simulation_bacnet_property(ctx, name, property_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.addProperty(
		name,
		int(property_id)
	))

#########################################################################
# パラメータ の 設定
#########################################################################
@cmd.group()
@click.pass_context
def set(ctx):
	pass

#########################################################################
# シミュレーションパラメータ の 設定
#########################################################################
@set.group(name = 'simulation')
@click.pass_context
def set_simulation(ctx):
	pass

#########################################################################
# プロトコル の 設定
#########################################################################
@set_simulation.group(name = 'bacnet')
@click.pass_context
def set_simulation_bacnet(ctx):
	pass

#########################################################################
# プロペティ種別 の 設定
#########################################################################
@set_simulation_bacnet.command(name = 'property')
@click.pass_context
@click.argument('name')
@click.argument('property_id')
@click.argument('type', type = click.Choice(['STATIC', 'MEASUREMENT']))
@click.argument('value')
def set_simulation_bacnet_property(ctx, name, property_id, type, value):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.setPropertyType(
		name,
		int(property_id),
		type,
		value
	))

#########################################################################
# 静的パラメータ の 設定
#########################################################################
@set_simulation_bacnet.group(name = 'static')
@click.pass_context
def set_simulation_bacnet_static(ctx):
	pass

@set_simulation_bacnet_static.command(name = 'property')
@click.pass_context
@click.argument('name')
@click.argument('property_id')
@click.argument('value')
def set_simulation_bacnet_static_property(ctx, name, property_id, value):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)

	#
	# オブジェクトの登録
	#
	click.echo(client.setProperty(
		name,
		int(property_id),
		float(value)
	))

#########################################################################
# 情報確認用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def show(ctx):
	pass

#########################################################################
# VERSION の 確認
#########################################################################
@show.command(name = 'version')
@click.pass_context
def show_version(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = RPCClient(host, port)

	#
	# バージョンの確認
	#
	version = client.getVersion()
	click.echo(version)

#########################################################################
# NIC の 情報取得
#########################################################################
@show.command(name = 'interfaces')
@click.pass_context
def show_interfaces(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = RPCClient(host, port)

	#
	# 接続した Eyed の NIC 情報取得
	#
	interfaces = client.getNetworkInterfaces()
	for interface in interfaces:
		name = interface['name']
		ipv4 = interface['ipv4']
		click.echo('%s %s' %(name, ipv4))

#########################################################################
# 測定グループ の 確認
#########################################################################
@show.group(name = 'measurement')
@click.pass_context
def show_measurement(ctx):
	pass

#########################################################################
# 測定グループ の 確認
#########################################################################
@show_measurement.command(name = 'taskgroups')
@click.pass_context
def show_measurement_taskgroups(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = SchedulerRPCClient(host, port)
	for taskGroup in client.getTaskGroups():
		click.echo(taskGroup)

#########################################################################
# 測定タスク (BACnet) の表示機能
#########################################################################
@show_measurement.group(name = 'bacnet')
@click.pass_context
def show_measurement_bacnet(ctx):
	pass

#########################################################################
# 測定タスクの表示機能
#########################################################################
@show_measurement_bacnet.command(name = 'tasks')
@click.argument('name')
@click.pass_context
def show_measurement_bacnet_tasks(ctx, name):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = SchedulerRPCClient(host, port)
	for task in client.getBACnetTasks(name):
		click.echo(task)

#########################################################################
# 測定値の表示機能
#########################################################################
@show_measurement_bacnet.command(name = 'values')
@click.argument('task_id')
@click.pass_context
def show_measurement_bacnet_values(ctx, task_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = SchedulerRPCClient(host, port)
	for value in client.getBACnetMeasuredValues(task_id):
		click.echo(value)

#########################################################################
# シミュレーションパラメータ の 確認
#########################################################################
@show.group(name = 'simulation')
@click.pass_context
def show_simulation(ctx):
	pass

#########################################################################
# プロトコルパラメータ の 確認
#########################################################################
@show_simulation.group(name = 'bacnet')
@click.pass_context
def show_simulation_bacnet(ctx):
	pass

#########################################################################
# 測定グループ の 定義
#########################################################################
@show_simulation_bacnet.command(name = 'objects')
@click.pass_context
def show_simulation_bacnet_objects(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	for obj in client.getObjects():
		click.echo('OBJECT(name=%10s, object_id=%4d, instance_id=%4d)' %(obj['name'], obj['object_id'], obj['instance_id']))
		for prop in obj['properties']:
			click.echo('-PROPERTY(property_id=%4d)' %(prop['property_id']))

#########################################################################
# DB ログ取得用 の コマンド
#########################################################################
@show_simulation_bacnet.command(name = 'log')
@click.pass_context
@click.argument('name')
@click.argument('property_id')
def show_simulation_bacnet_log(ctx, name, property_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	results = client.getPropertyLog(name, int(property_id))
	if results == None: return None

	#
	# ログの表示
	#
	for r in results:
		click.echo(r)

#########################################################################
# BACnet 関連の情報取得
#########################################################################
@show.group(name = 'bacnet')
@click.pass_context
def show_bacnet(ctx):
	pass

#
# BACnet Device の スキャン
#
@show_bacnet.command(name = 'scan')
@click.pass_context
def show_bacnet_scan(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.scan())

#
# BACnet Device の 情報取得
#
@show_bacnet.command(name = 'devices')
@click.pass_context
def show_bacnet_devices(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	for device in client.getDevices():
		click.echo(device)

#########################################################################
# データ取得用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def run(ctx):
	pass

#
# BACEPICS の起動
#
@run.command(name = 'bacepics')
@click.pass_context
@click.argument('device_id')
def run_bacepics(ctx, device_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.getEpics(int(device_id)))

#
# BACRP の起動
#
@run.command(name = 'bacrp')
@click.pass_context
@click.argument('device_id')
@click.argument('object_id')
@click.argument('instance_id')
@click.argument('property_id')
def run_bacrp(ctx, device_id, object_id, instance_id, property_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	if client.getStatus() == False:
		click.echo('BACnetd is not running...')
		return

	#
	# Eyed に RPC接続
	#
	client = BACnetRPCClient(host, port)
	click.echo(client.doReadPropertyRequest(
		int(device_id),
		int(object_id),
		int(instance_id),
		int(property_id)
	))

#########################################################################
# デーモン起動用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def start(ctx):
	pass

#
# BACNETD の起動
#
@start.command(name = 'bacnetd')
@click.pass_context
@click.argument('interface')
@click.argument('device_id', default = 2018)
def start_bacnetd(ctx, interface, device_id):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# EYED に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	click.echo(client.start(interface, device_id))

#########################################################################
# デーモン状態取得用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def status(ctx):
	pass

#
# BACNETD の 状態確認
#
@status.command(name = 'bacnetd')
@click.pass_context
def status_bacnetd(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# Eyed に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	click.echo(client.getStatus())

#########################################################################
# デーモン停止用 の コマンド
#########################################################################
@cmd.group()
@click.pass_context
def stop(ctx):
	pass

#
# BACNETD の 停止
#
@stop.command(name = 'bacnetd')
@click.pass_context
def stop_bacnetd(ctx):
	#
	# 引数の取得
	#
	host = ctx.obj['host']
	port = ctx.obj['port']

	#
	# EYED に RPC接続
	#
	client = BACnetdRPCClient(host, port)
	click.echo(client.stop())

#
# START
#
def start_cli():
	cmd(obj = {})

#
# Entry Point
#
if __name__ == '__main__':
	start_cli()

