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

import numpy as np
import cv2

VERTICAL = 3
HORIZONTAL = 3

video_path = "/mnt/n/save/video/save/息止め/イメージビデオ/5H53TvdJ-00_7s5050dBEjE_youtube.com.mp4"
thumbnail_path = "/mnt/n/save/video/save/息止め/イメージビデオ/5H53TvdJ-00_7s5050dBEjE_youtube.com.jpg"

video = cv2.VideoCapture(video_path)
video_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
video_fps = video.get(cv2.CAP_PROP_FPS)
print("video_frame:{0}".format(video_frame))
thumbnail_interval = int(video_frame / (VERTICAL * HORIZONTAL - 1)) -2
image_list = []
temp_image_list = []

flame_num = 0
hor_img_count = 0
for flame_num in range(0, int(video_frame), int(thumbnail_interval)):
    while True:
        video.set(cv2.CAP_PROP_POS_FRAMES, flame_num)
        ret, frame = video.read()
        #print("type:{0}, 判定:{1}".format(frame, frame is None), flush=True)

        if frame is None:
            flame_num -= 1
        else:
            break

    video_len_sec = flame_num / video_fps
    put_text = '{0}:{1:0=2}'.format(int(video_len_sec / 60),
                                    int(video_len_sec % 60))
    retval, baseLine = cv2.getTextSize(put_text, cv2.FONT_HERSHEY_COMPLEX, 1.0,
                                       1)
    left = 5
    right = left + retval[0] + 10
    bottom = frame.shape[0] - 5
    top = bottom - retval[1] - 10
    pts = np.array(
        ((left, top), (right, top), (right, bottom), (left, bottom)))
    cv2.fillPoly(frame, [pts], (200, 200, 200))
    cv2.putText(frame,
                put_text, (left + 5, bottom - 5),
                cv2.FONT_HERSHEY_COMPLEX,
                1.0, (0, 0, 0),
                lineType=cv2.LINE_AA)
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
