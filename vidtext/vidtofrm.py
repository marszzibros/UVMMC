import cv2
import os
import numpy as np
import easyocr
import datetime
import time
from copy import deepcopy

class vidtofrm:

## video_path :
## batchs_size:
## every      :
    def __init__(self, video_path, batch_size, every):
        # objects for keras_ocr and video reader
        self.pipeline = easyocr.Reader(['en'], gpu=True)
        self.vr = cv2.VideoCapture(video_path)
        
        # get the first keras_ocr prediction in each batches
        self.every = every
        self.batch_size = batch_size

        self.img_array = []
        
    # midpoint - get midpoint of text edges
    def midpoint(self, x1, y1, x2, y2):
        x_mid = int((x1 + x2)/2)
        y_mid = int((y1 + y2)/2)
        return (x_mid, y_mid)

    # mse - get mse (mean standard errors) for images; image comparison
    def mse(self, img1, img2):

        # convert the images to grayscale
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse

    def removal(self, prediction, frame):
        processed_img = deepcopy(frame)

        for box in prediction:
            val = box
            for i in range(int(val[0][0][0]//1), int(val[0][2][0])//1):
                for j in range(int(val[0][0][1]//1), int(val[0][2][1]//1)):
                    processed_img[j][i] = (255,255,255)

        return processed_img

    def extframes(self):
        count = 0
        preFrame = None
        prediction_groups = None
        prePrediction = None
        for i in range(0, int(self.vr.get(cv2.CAP_PROP_FRAME_COUNT))):
            success, frame = self.vr.read()
            
            if i % self.every == 0:
                preFrame = deepcopy(frame)
                result = self.mse(preFrame,frame)
                if count == 0 or result > 30 or count % self.batch_size == 0 :
                    prediction_groups = self.pipeline.readtext(frame)
                    prePrediction = deepcopy(prediction_groups)
                    if result < 30 and count != 0:
                        prediction_groups = prediction_groups + prePrediction 
                    prePrediction = deepcopy(prediction_groups)
                    print(i)
                
                img = self.removal(prediction_groups, frame)
                self.img_array.append(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

                count += 1
                
    def make_vid(self, file_path):
        height, width, layers = self.img_array[0].shape
        size = (width, height)

        original_fps = int(self.vr.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter(file_path,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), original_fps // self.every, size)
        for i in range(len(self.img_array)):
            out.write(self.img_array[i])
        out.release()