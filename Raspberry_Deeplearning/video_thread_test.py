import tensorflow as tf
import tensornets as nets
import cv2
import numpy as np
import time
import threading
import firebase_admin
import random
from tensorflow.python.compiler.tensorrt import trt_convert as trt
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.framework import convert_to_constants
import picamera
from time import sleep
from uuid import uuid4
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate('myKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://graduate-work-462b3.firebaseio.com',
    'storageBucket': "graduate-work-462b3.appspot.com"
})


bucket = storage.bucket()

def fileUpload(file):
    blob = bucket.blob(file)
    #new token and metadata 설정
    print("save start")
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata

    #upload file
    blob.upload_from_filename(filename=file, content_type='image/png')
    print(blob.public_url)



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

def record(cond,turn):
    while True:
        cond.acquire()  ### mutex_lock
        while turn.myTurn != 0: cond.wait()
        print('record run')
        recordVideo()
        turn.myTurn = 1

        cond.notifyAll()  # notify to all consumers
        cond.release() ### mutex_unlock
        print('record end')


def deeplearning(cond,turn):
    print('deeplearning start')
    inputs = tf.placeholder(tf.float32, [None, 416, 416, 3])
    model = nets.YOLOv3COCO(inputs, nets.Darknet19)
    # model = nets.YOLOv2(inputs, nets.Darknet19)

    # frame=cv2.imread("D://pyworks//yolo//truck.jpg",1)

    # classes={'0':'person','1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
    classes = {'0': 'person'}

    # list_of_classes=[0,1,2,3,5,7]
    list_of_classes = [0]

    try:
        with tf.Session() as sess:
            cond.acquire()  ### mutex_lock
            sess.run(model.pretrained())
            # "D://pyworks//yolo//videoplayback.mp4"
            while turn.myTurn != 1: cond.wait() #추가해준거임 내 번호가 아닐경우 대기

            # cap=cv2.imread('test.jpg',cv2.IMREAD_COLOR)
            cap = cv2.imread('image.JPG', cv2.IMREAD_COLOR)

            img = cv2.resize(cap, (647, 647), cv2.INTER_AREA)

            image = np.array(img).reshape(-1, 647, 647, 3)
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


            cv2.imwrite("result_image.png", img)

            fileUpload("result_image.png")
            print("save end")

        cv2.destroyAllWindows()
        turn.myTurn = 0
        cond.notifyAll()  # notify to all consumers
        cond.release()  ### mutex_unlock

        print('deeplearning end')

    except Exception as e:
        print(str(e))


class CondVar :
    myTurn = 0
    def __init__ (self):
        pass

if __name__ == '__main__':
    cond = threading.Condition()
    turn = CondVar()
    ref1 = db.reference('Distribution_DB/JongHap')
    ref2 = db.reference('Distribution_DB/Sanyung')
    ref3 = db.reference('Distribution_DB/TIP')
    ref4 = db.reference('Distribution_DB/Olive')

    for i in range(1):
        t1 = threading.Thread(target=record, args=(cond,turn))
        t2 = threading.Thread(target=deeplearning, args=(cond,turn))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


    print("===exit===")


