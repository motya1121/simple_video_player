#!/usr/bin/python
# coding: utf-8

'''
動画管理を行うプログラム
CONFIGファイルに書かれているディレクトリ内に存在する動画に関する情報をまとめて、JSON形式で出力する。
'''


import io
import sys
import codecs
import configparser
import subprocess
import os.path
import hashlib
import json
import stat
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time


#############################################
#                  classes                  #
#############################################


class VIDEO:
    def __init__(self, video_dir_path, video_file_name, video_web_dir_path="", sha1=None, video_length=0, tags=[], exists_video_file=False, exists_thumbnail=False, view_count=0, is_favorite=False):
        self.video_dir_path = video_dir_path
        self.video_file_name = video_file_name
        self.video_web_dir_path = video_web_dir_path
        self.sha1 = sha1
        self.video_length = video_length
        self.tags = tags
        self.exists_thumbnail = exists_thumbnail
        self.view_count = view_count
        self.exists_video_file = exists_video_file
        self.is_favorite = is_favorite

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
        video_path = self.video_dir_path + "/" + self.video_file_name
        with open(video_path, "rb") as video_file:
            video_binary_data = video_file.read(10000)
            sha1 = hashlib.sha1(video_binary_data).hexdigest()
        if DEBUG in ["2"]:
            print("*INFO: {0}'s sha1sum->{1}".format(self.video_file_name, sha1), flush=True)
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
                print("*INFO: thumbnail exists", flush=True)
            self.exists_thumbnail = True
        else:
            if DEBUG in ["2"]:
                print("*INFO: thumbnail not exists", flush=True)
            self.exists_thumbnail = False
        return self.exists_thumbnail

    def make_thumbnail(self, VERTICAL=3, HORIZONTAL=3):
        '''
        サムネイルを作成し、self.exists_thumbnailをTrueにする

        Parameters
        ----------
        無し

        Returns
        -------
        無し
        '''

        import numpy as np
        import cv2

        if DEBUG in ["1", "2"]:
            print("*INFO: make {0}'s thumbnail".format(self.video_file_name), flush=True)

        video_path = self.video_dir_path + "/" + self.video_file_name
        thumbnail_path = self.video_dir_path + "/" + self.video_file_name[:self.video_file_name.rfind(".")] + ".jpg"
        video = cv2.VideoCapture(video_path)
        video_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
        video_fps = video.get(cv2.CAP_PROP_FPS)

        thumbnail_interval = int(video_frame / (VERTICAL * HORIZONTAL - 1)) - 1
        image_list = []
        temp_image_list = []

        flame_num = 0
        hor_img_count = 0
        for flame_num in range(0, int(video_frame), int(thumbnail_interval)):
            while True:
                video.set(cv2.CAP_PROP_POS_FRAMES, flame_num)
                ret, frame = video.read()

                if frame is None:
                    if flame_num <= thumbnail_interval*2:
                        flame_num += 1
                    else:
                        flame_num -= 1
                else:
                    break
            video.set(cv2.CAP_PROP_POS_FRAMES, flame_num)
            ret, frame = video.read()

            video_len_sec = flame_num / video_fps
            put_text = '{0}:{1:0=2}'.format(int(video_len_sec / 60), int(video_len_sec % 60))
            retval, baseLine = cv2.getTextSize(put_text, cv2.FONT_HERSHEY_COMPLEX, 1.0, 1)
            left = 5
            right = left + retval[0] + 10
            bottom = frame.shape[0] - 5
            top = bottom - retval[1] - 10
            pts = np.array(((left, top), (right, top), (right, bottom), (left, bottom)))
            cv2.fillPoly(frame, [pts], (200,200,200))
            cv2.putText(frame, put_text, (left + 5, bottom-5), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
            temp_image_list.append(frame)
            hor_img_count += 1
            if hor_img_count == HORIZONTAL:
                image_list.append(cv2.hconcat(temp_image_list))
                temp_image_list = []
                hor_img_count = 0

        # メモリ開放
        video.release()
        cv2.destroyAllWindows()

        thumbnail = cv2.vconcat(image_list)
        cv2.imwrite(thumbnail_path, thumbnail)

        self.exists_thumbnail = True

    def calc_video_length(self):
        '''
        動画の長さを計算し、self.video_lengthに格納する

        Parameters
        ----------
        無し

        Returns
        -------
        video_len_sec
            type: int
            内容: 動画の長さ
        '''

        # 動画の長さ計算
        import numpy as np
        import cv2

        video_path = self.video_dir_path+"/"+self.video_file_name
        video = cv2.VideoCapture(video_path)

        video_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
        video_fps = video.get(cv2.CAP_PROP_FPS)
        if video_frame == 0.0 or video_fps == 0.0:
            video_len_sec = 0
        else:
            video_len_sec = video_frame / video_fps

        self.video_length = video_len_sec

        return video_len_sec

    def generate_dict(self):
        '''
        クラス内のデータをJSONとして出力するために辞書化する

        Parameters
        ----------
        無し

        Returns
        -------
        video_file_dict:
            type: Dict
            内容: 出力する辞書ファイル
        '''
        video_file_dict = {
            "video_dir_path": self.video_dir_path,
            "video_file_name": self.video_file_name,
            "sha1": self.sha1,
            "video_length": int(self.video_length),
            "tags": self.tags,
            "exists_thumbnail": self.exists_thumbnail,
            "view_count": self.view_count,
            "exists_video_file": self.exists_video_file,
            "is_favorite": self.is_favorite
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
    video_file_list = []

    if DEBUG in ["1", "2"]:
        print("*INFO: in dir:{0}".format(search_path), flush=True)
    # シンボリックリンクの作成
    search_path_sha1 = hashlib.sha1(search_path.encode("utf8")).hexdigest()
    os.symlink(search_path, ROOT_WEB_DIR+"/video_contents/"+search_path_sha1)

    proc = subprocess.run(["ls", "-1"], cwd=search_path,
                          stdout=subprocess.PIPE)
    ls_results = proc.stdout.decode("utf8").splitlines()

    for ls_result in ls_results:
        file_path = search_path + "/" + ls_result
        if os.path.isdir(file_path):
            video_file_list.extend(search_video_file(file_path))
        elif ls_result.split(".")[-1] not in ["mp4"]:
            pass
        else:
            video_file_list.append(get_video_data(search_path, ls_result))
    if DEBUG in ["1", "2"]:
        print("*INFO: out dir: {0}".format(search_path), flush=True)

    return video_file_list


def get_video_data(video_dir_path, video_file_name):
    '''
    受け取った動画ファイルに関する情報をVIDEOクラスにまとめる

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
    if DEBUG in ["2"]:
        print("*INFO: get {0} data for directory".format(video_file_name), flush=True)

    video = VIDEO(video_dir_path=video_dir_path,
                  video_file_name=video_file_name, exists_video_file=True)
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

    exists_video_data = False
    for json_video_data in json_video_data_list:
        if (json_video_data.sha1 == sha1):
            exists_video_data = True
            break

    return exists_video_data


def set_video_data_for_json(json_video_data_dict):
    '''
    JSONのデータをVIDEOクラスのデータに変換する

    Parameters
    ----------
    json_video_data_dict:
        type:Dict
        内容:JSONのデータが入った辞書変数

    Returns
    -------
    video_data:
        type:VIDEOクラス
        内容:動画のデータ
    '''
    if DEBUG in ["2"]:
        print("*INFO: get {0} data for JSON".format(json_video_data_dict["video_file_name"]), flush=True)
    video_data = VIDEO(video_dir_path=json_video_data_dict["video_dir_path"],
                       video_file_name=json_video_data_dict["video_file_name"],
                       sha1=json_video_data_dict["sha1"])

    if "video_length" in json_video_data_dict:
        video_data.video_length = json_video_data_dict["video_length"]
    if "tags" in json_video_data_dict:
        video_data.tags = json_video_data_dict["tags"]
    if "exists_video_file" in json_video_data_dict:
        #video_data.exists_video_file = json_video_data_dict["exists_video_file"]
        video_data.exists_video_file = False
    if "exists_thumbnail" in json_video_data_dict:
        video_data.exists_thumbnail = json_video_data_dict["exists_thumbnail"]
    if "view_count" in json_video_data_dict:
        video_data.view_count = json_video_data_dict["view_count"]
    if "is_favorite" in json_video_data_dict:
        video_data.is_favorite = json_video_data_dict["is_favorite"]

    return video_data


def check_json_format(json_file_path):
    '''
    JSONファイルが不正かどうかを確認

    Parameters
    ----------
    json_file_path :
        type: str
        内容: JSONファイルへのパス(絶対パス)

    Returns
    -------
        type: boolean
        内容: 正しい->True, 不正->False
    '''
    with open(json_file_path, "r") as json_file:
        try:
            json.load(json_file)
            return True
        except json.JSONDecodeError:
            return False


def update_video_data(json_video_data_list, dir_video_data):
    '''
    JSONファイル内の情報をアップデート

    Parameters
    ----------
    json_video_data_list:
        type: VIDEOのlist
        内容: JSON内に書かれている動画データ
    dir_video_data:
        type: VIDEOクラス
        内容: ディレクトリにある動画データ

    Returns
    -------
    json_video_data_list
        type: VIDEOのlist
        内容: 新しい情報にしたあとのjson_video_data_list
    '''
    for json_video_data in json_video_data_list:
        if (json_video_data.sha1 == dir_video_data.sha1):
            json_video_data.video_dir_path = dir_video_data.video_dir_path
            json_video_data.video_file_name = dir_video_data.video_file_name
            json_video_data.exists_thumbnail = dir_video_data.exists_thumbnail
            json_video_data.exists_video_file = dir_video_data.exists_video_file

            if json_video_data.video_length == 0:
                json_video_data.calc_video_length()
            if json_video_data.exists_thumbnail == False:
                json_video_data.make_thumbnail()
    return json_video_data_list

#############################################
#                   main                    #
#############################################


# initialize
config_file = configparser.ConfigParser()
config_file.read('video_manage.conf', 'UTF-8')
ROOT_VIDEO_DIR_LIST = config_file.get("SETTINGS", "root_video_dir").split(",")
ROOT_WEB_DIR = config_file.get("SETTINGS", "root_web_dir")
DEBUG = config_file.get("DEBUG", "DEBUG_LEVEL")

# シンボリックリンク
# INFO
print ("*INFO: シンボリックリンクの作成", flush=True)
if os.path.isdir(ROOT_WEB_DIR+"/video_contents/") == True:
    # ディレクトリ内のシンボリックリンクを削除
    proc = subprocess.run(["ls", "-1"], cwd=ROOT_WEB_DIR +
                          "/video_contents/", stdout=subprocess.PIPE)
    ls_results = proc.stdout.decode("utf8").split()
    for ls_result in ls_results:
        os.unlink(ROOT_WEB_DIR+"/video_contents/"+ls_result)
else:
    # ディレクトリの作成
    os.mkdir(ROOT_WEB_DIR+"/video_contents/")


# ディレクトリ内の動画ファイルをリスト化
# INFO
print ("*INFO: ディレクトリ内の動画ファイルをリスト化", flush=True)
dir_video_data_list = []
for ROOT_VIDEO_DIR in ROOT_VIDEO_DIR_LIST:
    dir_video_data_list.extend(search_video_file(ROOT_VIDEO_DIR))


# videos.json内の動画データをリスト化
# INFO
print ("*INFO: JSONファイル内の動画データをリスト化", flush=True)
json_video_data_list = []
if os.path.isfile(ROOT_WEB_DIR + "/videos.json") == True and check_json_format(ROOT_WEB_DIR + "/videos.json") == True:
    with open(ROOT_WEB_DIR + "/videos.json", "r") as video_json_file:
        json_video_data = json.load(video_json_file)
        # json_video_data(辞書型)のデータをVIDEOクラスのリスト(json_video_data_list)に変換
        for json_video_data_dict in json_video_data:
            json_video_data_list.append(
                set_video_data_for_json(json_video_data_dict))


# dir_video_data_listとjson_video_data_listを比較
# INFO
print ("*INFO: ディレクトリとJSONの内容を比較", flush=True)
for dir_video_data in dir_video_data_list:
    if len(json_video_data_list) == 0:
        # 新規追加
        dir_video_data.calc_video_length()
        json_video_data_list.append(dir_video_data)
        if dir_video_data.exists_thumbnail == False:
            dir_video_data.make_thumbnail()
    elif exists_video_data(json_video_data_list, dir_video_data.sha1) == True:
        # ファイルパスなどをアップデート
        json_video_data_list = update_video_data(
            json_video_data_list, dir_video_data)
    else:
        # 新規追加
        dir_video_data.calc_video_length()
        json_video_data_list.append(dir_video_data)
        if dir_video_data.exists_thumbnail == False:
            dir_video_data.make_thumbnail()


# 書き出すデータの準備
# INFO
print ("*INFO: JSONの書き出し準備", flush=True)
output_video_data_list = []
for json_video_data in json_video_data_list:
    output_video_data_list.append(json_video_data.generate_dict())


# video.jsonに書き出し
# INFO
print ("*INFO: JSONの書き出し", flush=True)
with open(ROOT_WEB_DIR + "/videos.json", "w") as video_json_file:
    json.dump(output_video_data_list, video_json_file, indent=4)
os.chmod(ROOT_WEB_DIR + "/videos.json",
         stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
