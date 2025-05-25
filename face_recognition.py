# coding=utf-8
from naoqi import ALProxy
import cv2
import numpy as np
import os
import random
from config import DATA_FOLDER, NAO_IP, NAO_PORT, CONFIDENCE_THRESHOLD

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def prepare_training_data(data_folder):
    faces = []
    labels = []
    for image_name in os.listdir(data_folder):
        if image_name.endswith('.jpg'):
            image_path = os.path.join(data_folder, image_name)
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces_rect:
                faces.append(gray[y:y + h, x:x + w])
                labels.append(0)  # 标签为0
    return faces, labels


def train_face_recognizer(faces, labels):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    return recognizer



faces, labels = prepare_training_data(DATA_FOLDER)
if len(faces) > 0:
    recognizer = train_face_recognizer(faces, labels)
else:
    print("没有足够的训练数据！")


def detect_face(speak_text):
    videoProxy = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
    video_client = videoProxy.subscribeCamera("python_client", 0, 1, 13, 30)

    greetings = ["早上好呀，台下怎么这么多人，你是不是正在答辩哈", "Hello，早上好，台下怎么这么多人，你是不是正在答辩哈"]

    try:
        print("开始人脸识别...")
        while True:
            image_data = videoProxy.getImageRemote(video_client)
            if image_data is None:
                continue

            width, height = image_data[0], image_data[1]
            image_array = np.fromstring(image_data[6], dtype=np.uint8)
            frame = image_array.reshape((height, width, 3))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces_rect:
                face = gray[y:y + h, x:x + w]
                label, confidence = recognizer.predict(face)

                if confidence < CONFIDENCE_THRESHOLD:
                    print("检测到用户, 置信度: {:.2f}".format(confidence))
                    speak_text(random.choice(greetings))
                    videoProxy.unsubscribe(video_client)
                    return True
    finally:
        videoProxy.unsubscribe(video_client)
        cv2.destroyAllWindows()
