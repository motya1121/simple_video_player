# simple_video_server
PCに保存した動画を簡単にLAN内の端末で視聴できるようにするツール。

# 動作環境
## OS
Ubuntu16.04
4.4.0-131-generic

## 使用したアプリケーションなど
- Python 3.5.2:
Ubuntu16.04のデフォルト
- pip 8.1.1:
`sudo apt-get install python3-pip`でインストール
- PHP 7.0.33:
`sudo apt-get install php`でインストール
- Apache 2.4.18:
`sudo apt-get install apache2`でインストール
今回はhttps通信にしたいので、以下のコマンドを実行
```
# enable mod_rewrite
sudo a2enmod rewrite
sudo systemctl restart apache2

# enable https
sudo a2enmod ssl
sudo a2ensite default-ssl
sudo service apache2 reload
```

その他pip関連で諸々必要


# 環境設定
## 設定ファイル
### video_manage/video_manage.conf
- root_web_dir: Webページのルートディレクトリ(web_pageディレクトリを配置した場所)
- root_video_dir: 動画ファイルが配置されているディレクトリ(カンマ区切りで複数指定可能)


### web_page/web_page_conf.php
- $is_open: Trueならばサイトを公開,Falseならばサイトを公開しない


## 動画登録
`video_manage/video_manage.py`を実行するだけ
なお、シンボリックリンクなどを張ったり、ファイルを作成する必要があるため、権限には注意が必要。
動画を更新したい場合も同じコマンドを実行するだけで更新される．


## Webページ作成
### シンボリックリンク
`/var/www/html/`に`web_page`へのシンボリックリンクを張る．
### ファイルのコピ－
`web_page`ディレクトリをapache配下に移動する


# 使用方法
ブラウザより`top.php`を開けば閲覧できる
