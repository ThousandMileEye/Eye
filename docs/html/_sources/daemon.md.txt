# Daemon Manager
## 自動起動の設定
  ここでは、EYED を 自動起動サービスとして登録する方法について説明します。
デーモンの管理は、supervisor を使用します。

### supervisor の インストール
```bash
sudo apt-get install supervisor
```

### supervisor 用 の 設定ファイルを作成
```bash
sudo vi /etc/supervisor/conf.d/eye.conf
```

```bash
[program:eyed]
command=eyed
numprocs=1
autostart=true
autorestart=true
user=root
redirect_stderr=true
stdout_logfile=/var/log/supervisor/eyed.log
```

### 設定ファイルの再読み込み
```bash
supervisorctl reread
```

### サービスの登録
```bash
supervisorctl add eyed
```

### サービスの起動
```bash
supervisorctl start eyed
```

### サービスの停止
```bash
supervisorctl stop eyed
```

### サービスの確認
```bash
supervisorctl status eyed
```

