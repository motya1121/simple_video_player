# easy play video
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



# 使用方法
## 動画の追加


## 動画の削除

