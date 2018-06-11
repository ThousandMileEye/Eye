# CLI for BACnet Protocol
## BACnet サービスの管理
### サービスを起動する
　BACnet サービスを利用するためには、まず BACnet サービスへの設定を実行する必要があります。
BACnet サービスは以下のコマンドを使用することで利用することが可能となります。

```bash
$ eye start bacnetd [INTERFACE] [DEVICE_ID]
```

  実際に使用する際には以下のように、インタフェース名を指定する必要があります。
BACnet の デバイス ID は省略することが可能です。（同じネットワークに同じBACnet Device ID
のBACnet デバイスが存在する際には変更を行う必要があります。）

```bash
$ eye start bacnetd eth0 1234
```

### サービスを停止する
  BACnet サービスを停止する際には、以下のコマンドを実行します。
停止する場合には、BACnet を 使用した通信を行うことが出来なくなることに注意してください。

```bash
$ eye stop bacnetd
```

## BACnet による値の取得
### 同一ネットワーク内の BACnet デバイスを検索する
  BACnet では、IP アドレスの代わりに デバイスID と呼ばれる識別子を利用することで、
BACnet デバイス同士の通信が行われます。そのためBACnet の 通信を行うためには、
まず BACnet デバイスを検索する必要があります。以下のコマンドを実行することで、
BACnet デバイスの検索を実行することが可能です。

```bash
$ eye show bacnet scan
```

### BACnet デバイスを確認する
  BACnet デバイスのスキャンに成功すると、BACnet を使用したデバイスを確認することが、
出来るようになります。デバイスリストは以下のように確認することができます。

```bash
$ eye show bacnet devices
{'ip': '192.168.218.8', 'device_id': 23200}
{'ip': '192.168.218.6', 'device_id': 200}
{'ip': '192.168.218.5', 'device_id': 5}
```

### BACnet デバイス の プロパティ一覧を確認する
  BACnet デバイスが保持しているプロパティ一覧や、オブジェクトリストといった基本情報を取得するためには、
以下のコマンドを実行することで、基本的なパラメータを確認することが可能となります。

```bash
$ eye run bacepics 200
{
	'databaseRevision': 7L,
	'maxMaster': 32L,
	'numberOfApduRetries': 3L,
	'intervalOffset': None,
	'protocolServicesSupported': [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1],
	'timeOfDeviceRestart': <bacpypes.basetypes.TimeStamp object at 0x7f40001747d0>,
	'slaveAddressBinding': None,
	'slaveProxyEnable': None,
	'maxSegmentsAccepted': 8L,
	'restoreCompletionTime': None,
	'protocolVersion': 1L,
	'systemStatus': 'operational',
	'deviceAddressBinding': [
		<bacpypes.basetypes.AddressBinding object at 0x7f40000cc750>,
		<bacpypes.basetypes.AddressBinding object at 0x7f3ff078bf90>,
		<bacpypes.basetypes.AddressBinding object at 0x7f40000d4390>,
		<bacpypes.basetypes.AddressBinding object at 0x7f3ff07b9a10>
	],
	'modelName': '### unknown encoding: 1 ###',
	'configurationFiles': [],
	'timeSynchronizationInterval': None,
	'utcTimeSynchronizationRecipients': None,
	'manualSlaveAddressBinding': None,
	'apduTimeout': 6000L,
	'backupFailureTimeout': 0L,
	'apduSegmentTimeout': 6000L,
	'segmentationSupported': 'segmentedBoth',
	'protocolObjectTypesSupported': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1],
	'vendorIdentifier': 279L,
	'firmwareRevision': '### unknown encoding: 1 ###',
	'objectList': None,
	'localDate': (118, 4, 3, 2),
	'vendorName': '### unknown encoding: 1 ###',
	'lastRestoreTime': <bacpypes.basetypes.TimeStamp object at 0x7f4000087290>,
	'location': '',
	'protocolRevision': 0L,
	'activeCovSubscriptions': [],
	'maxInfoFrames': 1L,
	'vtClassesSupported': [],
	'timeSynchronizationRecipients': [],
	'backupPreparationTime': None,
	'lastRestartReason': 'unknown',
	'backupAndRestoreState': None,
	'localTime': (17, 28, 29, 30),
	'structuredObjectList': None,
	'applicationSoftwareVersion': '### unknown encoding: 1 ###',
	'serialNumber': None,
	'maxApduLengthAccepted': 1024L,
	'activeVtSessions': [],
	'restartNotificationRecipients': [],
	'utcOffset': -540,
	'restorePreparationTime': None,
	'daylightSavingsStatus': False,
	'autoSlaveDiscovery': None,
	'alignIntervals': None
}
```

### BACnet デバイス から プロパティの読み込みを実行する
  BACnet デバイスからプロパティの値を取得するためには、bacrpコマンドを使用します。

```bash
$ eye run bacrp 200 4 99 85
{'value': 'active'}
```

## BACnet シミュレータの利用
### 新規オブジェクトの登録
  BACnet Object を シミュレータに登録するには以下のコマンドを実行します。

```bash
$ eye add simulation bacnet object [NAME] [OBJECT_ID] [INSTANCE_ID]
```

  BACnet オブジェクトが登録されているかを確認するためには、bacepics 等のコマンドを
使用してください。

### 新規プロパティを登録
  作成したオブジェクトにプロパティを設定し、外部のデバイスから値を取得することが可能な
状態にします。

```bash
$ eye add simulation bacnet property [NAME] [PROPERTY_ID]
```

### プロパティへの値の設定
  作成したプロパティへの値を設定を行うためには、以下のコマンドを実行します。

```bash
$ eye set simulation bacnet property [NAME] [PROPERTY_ID] [VALUE]
```

### シミュレータが応答したプロパティのログを確認する
  シミュレータ機能を利用して、他の BACnet デバイスからデータを取得した際の、
ログを確認します。

```bash
$ eye show simulation bacnet log [NAME] [PROPERTY_ID]
```

## BACnet 計測機能の利用
  BACnet 計測機能は定期的に設定を行った値のポーリング処理を行い、
データを内部のデータベースに保存します。

### タスクグループの作成　
　計測機能を利用するためには、まずタスクグループの作成を行います。
タスクグループの中に、データの取得頻度が等しいタスクを追加して行くことで計測を行います。

```bash
$ eye add measurement taskgroup [TASK NAME] [INTERVAL]
```

### タスクグループにタスクを追加する
  作成したタスクグループにタスクを追加することで、計測処理を開始することが可能です。
```bash
eye add measurement task bacnet [NAME] [DEVICE_ID] [OBJECT_ID] [INSTANCE_ID] [PROPERTY_ID]
```

## BACnet プロキシ の 利用
  BACnet プロキシ機能は、計測機能とシミュレータ機能を使用します。
計測機能で収集したデータをシミュレータの監視ポイントとして振る舞わせることが可能です。

```bash
eye set simulation bacnet property [BACnetオブジェクト名] [プロパティ番号] MEASUREMENT [TASK_ID]
```

