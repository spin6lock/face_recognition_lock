import cv2
import numpy as np
import time
import sys
from ctypes import *

# 下载链接：https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
prototxt_path = "weights/deploy.prototxt.txt"
# 下载链接：https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel 
model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
# 加载Caffe model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)


class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

while True:
    idle_time_seconds = get_idle_duration()
    if idle_time_seconds > 10:
        cap = cv2.VideoCapture(0)
        _, image = cap.read()
        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        model.setInput(blob)
        output = np.squeeze(model.forward())
        font_scale = 1.0
        found = False
        for i in range(0, output.shape[0]):
            confidence = output[i, 2]
            if confidence > 0.5:
                box = output[i, 3:7] * np.array([w, h, w, h])
                start_x, start_y, end_x, end_y = box.astype(int)
                cv2.rectangle(image, (start_x, start_y), (end_x, end_y), color=(255, 0, 0), thickness=2)
                cv2.putText(image, f"{confidence*100:.2f}%", (start_x, start_y-5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)
                found = True
        # debug show image
        #cv2.imshow("image", image)
        if not found:
            # lock screen
            user32 = windll.LoadLibrary('user32.dll')
            user32.LockWorkStation()
            cv2.destroyAllWindows()
            cap.release()
            sys.exit(0)
        else:
            cap.release()
        time.sleep(5)
    
cv2.destroyAllWindows()
cap.release()