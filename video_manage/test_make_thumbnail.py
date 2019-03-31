import numpy as np
import cv2

video_path = self.video_dir_path + "/" + self.video_file_name
thumbnail_path = self.video_dir_path + "/" + self.video_file_name[:self.video_file_name.rfind(".")] + ".jpg"
VERTICAL = 3
HORIZONTAL=4
video = cv2.VideoCapture(video_path)
video_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
video_fps = video.get(cv2.CAP_PROP_FPS)

thumbnail_interval = int(video_frame / (VERTICAL * HORIZONTAL - 1)) - 1
image_list = []
temp_image_list = []

flame_num = 0
hor_img_count = 0
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    if flame_num % thumbnail_interval == 0:
        # 動画の長さ計算
        video_len_sec = flame_num / video_fps
        put_text = '{0}:{1:0=2}'.format(int(video_len_sec / 60), int(video_len_sec % 60))
        retval, baseLine = cv2.getTextSize(put_text, cv2.FONT_HERSHEY_COMPLEX, 1.0, 1)
        left = 5
        right = left + retval[0] + 10
        bottom = frame.shape[0] - 5
        top = bottom - retval[1] - 10
        pts = np.array(((left, top), (right, top), (right, bottom), (left, bottom)))
        cv2.fillPoly(frame, [pts], (200,200,200))
        cv2.putText(frame, put_text, (10, 260), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
        temp_image_list.append(frame)
        hor_img_count += 1
        if hor_img_count == HORIZONTAL:
            image_list.append(cv2.hconcat(temp_image_list))
            temp_image_list = []
            hor_img_count = 0

    flame_num += 1

# メモリ開放
video.release()
cv2.destroyAllWindows()

thumbnail = cv2.vconcat(image_list)
cv2.imwrite(thumbnail_path, thumbnail)
