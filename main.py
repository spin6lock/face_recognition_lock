import cv2
import numpy as np
import time
import sys
import logging
from logging.handlers import RotatingFileHandler
import socket
from ctypes import *

# 下载链接：https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
prototxt_path = "weights/deploy.prototxt.txt"
# 下载链接：https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel 
model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
# 加载Caffe model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
IDLE_TIME = 10
CONFIDENCE = 0.5
INTERVAL = 5
cap = None
log_filename = "debug.log"
DEFINED_PORT = 8888

"""
logging.basicConfig(
                    filename=log_filename,
                    filemode="a",
                    format=
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
"""

rotate_handler = RotatingFileHandler(log_filename,
                    maxBytes=20*1024*1024,
                    backupCount=5)
rotate_handler.setFormatter(logging.Formatter(
                                        '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                        datefmt='%H:%M:%S',
                                        ))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(rotate_handler)

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


def lock_screen():
    user32 = windll.LoadLibrary('user32.dll')
    user32.LockWorkStation()
    logger.debug("lock_screen")


def atexit():
    logger.debug("atexit")
    cv2.destroyAllWindows()
    if cap:
        cap.release()
    sys.exit(0)


def is_away_from_desk():
    global cap
    cap = cv2.VideoCapture(0)
    _, image = cap.read()
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    output = np.squeeze(model.forward())
    away = True
    for i in range(0, output.shape[0]):
        confidence = output[i, 2]
        if confidence > CONFIDENCE:
            away = False
            break
    return away

def main():
    global cap
    cap = cv2.VideoCapture(0)
    cap.release()
    while True:
        try: 
            idle_time_seconds = get_idle_duration()
            if idle_time_seconds < IDLE_TIME:
                time.sleep(INTERVAL)
                logger.debug("not idle check period")
                continue
            if is_away_from_desk():
                lock_screen()
                atexit()
            else:
                cap.release()
            time.sleep(INTERVAL)
            logger.debug("check period")
        except Exception as ex:
            logger.debug("exception:", ex)

    
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', DEFINED_PORT))
    main()
