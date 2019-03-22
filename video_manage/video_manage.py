#!/usr/bin/python
# coding: utf-8

'''
動画管理を行うプログラム
CONFIGファイルに書かれているディレクトリ内に存在する動画に関する情報をまとめて、JSON形式で出力する。
'''


import io,sys,codecs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import configparser
import subprocess
import os.path
import hashlib
import json

#############################################
#                  classes                  #
#############################################
class VIDEO:
    def __init__(self, video_dir_path, video_file_name, sha1=None, video_length=0, tags=[], exists_thumbnail=False, view_count=0):
        self.video_dir_path = video_dir_path
        self.video_file_name = video_file_name
        self.sha1 = sha1
        self.video_length = video_length
        self.tags = tags
        self.exists_thumbnail = exists_thumbnail
        self.view_count = view_count

    def calc_hash(self):
        '''
        ハッシュ値を計算し、self.sha1に格納

        Parameters
        ----------
        無し

        Returns
        -------
        ハッシュ値(str)
        '''
        video_path=self.video_dir_path+"/"+self.video_file_name
        with open(video_path, "rb") as video_file:
            video_binary_data = video_file.read()
            sha1 = hashlib.sha1(video_binary_data).hexdigest()
        if DEBUG in ["1", "2"]:
            print("*INFO: {0}'s sha1sum->{1}".format(self.video_file_name, sha1))
        self.sha1 = sha1
        return self.sha1

    def check_exists_thumbnail(self):
        '''
        サムネイルが存在するかどうかを確認し、結果をself.exists_thumbnailに格納

        Parameters
        ----------
        無し

        Returns
        -------
        Boolean(存在する:True,存在しない:False)
        '''
        tmb_file_name = self.video_file_name[:self.video_file_name.rfind(".")]
        if os.path.isfile(self.video_dir_path + "/" + tmb_file_name + ".jpg"):
            if DEBUG in ["2"]:
                print("*INFO: thumbnail not exists")
            self.exists_thumbnail=True
        else:
            if DEBUG in ["2"]:
                print("*INFO: thumbnail exists")
            self.exists_thumbnail = False
        return self.exists_thumbnail

    def create_thumbnail(self):
        '''
        サムネイルを作成する

        Parameters
        ----------
        無し

        Returns
        -------
        無し
        '''

    def generate_dict(self):
        '''
        サムネイルを作成する

        Parameters
        ----------
        無し

        Returns
        -------
        video_file_dict:
            type:Dict
            内容:クラス内のデータをJSONとして出力するために辞書化する
        '''
        video_file_dict = {
            "video_dir_path": self.video_dir_path,
            "video_file_name": self.video_file_name,
            "sha1": self.sha1,
            "video_length": int(self.video_length),
            "tags": self.tags,
            "exists_thumbnail": self.exists_thumbnail,
            "view_count": self.view_count
        }
        return video_file_dict


#############################################
#                 functions                 #
#############################################

def search_video_file(search_path):
    '''
    ディレクトリ内のビデオファイルを検索する

    Parameters
    ----------
    search_path :
        type: str
        内容: 動画ファイルを検索するディレクトリ(絶対パス)

    Returns
    -------
    video_file_list:
        type: list(〇〇クラス)
        内容: 動画ファイルに関する情報が入ったリスト
    '''
    # initialize
    video_file_list=[]

    if DEBUG in ["1", "2"]:
        print("*INFO: in dir:{0}".format(search_path))
    proc = subprocess.run(["ls", "-1"], cwd=search_path, stdout=subprocess.PIPE)
    ls_results = proc.stdout.decode("utf8").split()

    for ls_result in ls_results:
        file_path = search_path + "/" + ls_result
        if os.path.isdir(file_path):
            video_file_list.extend(search_video_file(file_path))
        elif ls_result.split(".")[-1] not in ["mp4"]:
            pass
        else:
            video_file_list.append(get_video_data(search_path, ls_result))
    if DEBUG in ["1", "2"]:
        print("*INFO: out dir: {0}".format(search_path))

    return video_file_list

def get_video_data(video_dir_path, video_file_name):
    '''
    ディレクトリ内のビデオファイルを検索する

    Parameters
    ----------
    video_dir_path :
        type: str
        内容: 動画ファイルが入っているディレクトリのパス(絶対パス)
    video_file_name :
        type: str
        内容: 動画ファイル名

    Returns
    -------
    video_data:
        type: VIDEOクラス
        内容: 動画ファイルに関する情報
    '''
    if DEBUG in ["1", "2"]:
        print("*INFO: get {0} data".format(video_file_name))

    video=VIDEO(video_dir_path,video_file_name)
    video.calc_hash()
    video.check_exists_thumbnail()

    return video

def exists_video_data(json_video_data_list, sha1):
    '''
    JSONファイル内に同じハッシュ値のデータがあるかどうか

    Parameters
    ----------
    json_video_data_list :
        type: list(VIDEOクラス)
        内容: JSONファイル内の情報
    sha1 :
        type: str
        内容: 比較する動画のハッシュ値(SHA1)

    Returns
    -------
    exists_video_data:
        type: boolean
        内容: 存在する:True, 存在しない:False
    '''
    # TODO: チェックする処理を追加


    return False





#############################################
#                   main                    #
#############################################

# initialize
config_file = configparser.ConfigParser()
config_file.read('video_manage.conf', 'UTF-8')
ROOT_VIDEO_DIR_LIST = config_file.get("SETTINGS", "root_video_dir").split(",")
ROOT_WEB_DIR=config_file.get("SETTINGS", "root_web_dir")
DEBUG = config_file.get("DEBUG", "DEBUG_LEVEL")


# ディレクトリ内の動画ファイルをリスト化
dir_video_data_list=[]
for ROOT_VIDEO_DIR in ROOT_VIDEO_DIR_LIST:
    dir_video_data_list.extend(search_video_file(ROOT_VIDEO_DIR))


# videos.json内の動画データをリスト化
if os.path.isfile(ROOT_WEB_DIR + "/videos.json") ==True:
    with open(ROOT_WEB_DIR + "/videos.json", "r") as video_json_file:
        json_video_data = json.load(video_json_file)
else:
    json_video_data_list=[]

# TODO: json_video_data(辞書型)のデータをVIDEOクラスのリスト(json_video_data_list)に変換




# dir_video_data_listとjson_video_data_listを比較
for dir_video_data in dir_video_data_list:
    if exists_video_data(json_video_data_list, dir_video_data.sha1) == True:
        # ファイルパスなどをアップデート
        pass
    else:
        # 新規追加
        json_video_data_list.append(dir_video_data)

# 書き出すデータの準備
output_video_data_list=[]
for json_video_data in json_video_data_list:
    output_video_data_list.append(json_video_data.generate_dict())

# video.jsonに書き出し
with open(ROOT_WEB_DIR + "/videos.json", "w") as video_json_file:
    json.dump(output_video_data_list,video_json_file)
