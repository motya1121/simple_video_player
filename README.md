# simple_video_server

PCに保存した動画を簡単にLAN内の端末で視聴できるようにするツール。

## 環境

- OS: Ubuntu16.04
- 使用したアプリケーション:
  - Python 3.5.2
  - pip 8.1.1
  - PHP 7.0.33
  - Apache 2.4.18

## 環境構築

### プログラムの配置

- web_page/
  - apacheの配下に配置
- video_manage/
  - どこでも可

### 設定ファイル

#### video_manage/video_manage.conf

- root_web_dir: Webページのルートディレクトリ(web_pageディレクトリを配置した場所)
- root_video_dir: 動画ファイルが配置されているディレクトリ(カンマ区切りで複数指定可能)

#### web_page/web_page_conf.php

- $is_open: Trueならばサイトを公開,Falseならばサイトを公開しない

### 動画登録

`video_manage/video_manage.py`を実行するだけ
なお、シンボリックリンクなどを張ったり、ファイルを作成する必要があるため、権限には注意が必要。
動画を更新したい場合も同じコマンドを実行するだけで更新される．
