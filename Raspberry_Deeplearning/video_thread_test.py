import tensorflow as tf
import tensornets as nets
import cv2
import numpy as np
import time
import threading
import keyboard
import firebase_admin
import random
from tensorflow.python.compiler.tensorrt import trt_convert as trt
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.framework import convert_to_constants
import picamera
from time import sleep
from firebase_admin import credentials
from firebase_admin import db


def recordVideo():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.start_preview()
        sleep(20)
        camera.start_recording('/home/pi/Graduate/video.h264')
        camera.capture('/home/pi/Graduate/image.JPG')
        camera.wait_recording(1)
        camera.stop_recording()
        camera.stop_preview()

def record(name1, name2):
    while True:
        print(name1)
        recordVideo()
        print(name2)


def deeplearning(name1, name2):
    print(name1)
    inputs = tf.placeholder(tf.float32, [None, 416, 416, 3])
    model = nets.YOLOv3COCO(inputs, nets.Darknet19)
    # model = nets.YOLOv2(inputs, nets.Darknet19)

    # frame=cv2.imread("D://pyworks//yolo//truck.jpg",1)

    # classes={'0':'person','1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
    classes = {'0': 'person'}

    # list_of_classes=[0,1,2,3,5,7]
    list_of_classes = [0]
    with tf.Session() as sess:
        sess.run(model.pretrained())
        # "D://pyworks//yolo//videoplayback.mp4"

        # cap=cv2.imread('test.jpg',cv2.IMREAD_COLOR)
        cap = cv2.imread('image.JPG', cv2.IMREAD_COLOR)

        img = cv2.resize(cap, (416, 416))
        image = np.array(img).reshape(-1, 416, 416, 3)
        start_time = time.time()
        preds = sess.run(model.preds, {inputs: model.preprocess(image)})

        print(time.time() - start_time)
        boxes = model.get_boxes(preds, image.shape[1:3])
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)

        cv2.resizeWindow('image', 700, 700)

        # print("--- %s seconds ---" % (time.time() - start_time))
        boxes1 = np.array(boxes)
        for j in list_of_classes:
            count = 0
            if str(j) in classes:
                lab = classes[str(j)]
            if len(boxes1) != 0:

                for i in range(len(boxes1[j])):
                    box = boxes1[j][i]

                    if boxes1[j][i][4] >= .40:
                        count += 1

                        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 1)
                        cv2.putText(img, lab, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255),
                                    lineType=cv2.LINE_AA)
            print(lab, ": ", count)
            ref3.set({'people_number': count})
            ref1.set({'people_number': random.randint(0, 10)})
            ref2.set({'people_number': random.randint(0, 10)})
            ref4.set({'people_number': random.randint(0, 10)})


        cv2.imshow("IMAGE", img)

    cv2.destroyAllWindows()

    print(name2)


if __name__ == '__main__':
    cred = credentials.Certificate('myKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://graduate-work-462b3.firebaseio.com'
    })

    ref1 = db.reference('Distribution_DB/Edong')
    ref2 = db.reference('Distribution_DB/Sanyung')
    ref3 = db.reference('Distribution_DB/Kpu')
    ref4 = db.reference('Distribution_DB/Olive')

    for i in range(3):
        t1 = threading.Thread(target=record, args=('record run', 'record end'))
        t2 = threading.Thread(target=deeplearning, args=('deeplearning run', 'deeplearning end'))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


    print("===exit===")

