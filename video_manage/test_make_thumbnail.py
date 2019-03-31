import numpy as np
import cv2

video_path = self.video_dir_path + "/" + self.video_file_name
thumbnail_path = self.video_dir_path + "/" + self.video_file_name[:self.video_file_name.rfind(".")] + ".jpg"
video = cv2.VideoCapture(video_path)
video_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)

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

self.exists_thumbnail = True