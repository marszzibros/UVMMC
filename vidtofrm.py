import cv2
import os
import numpy as np
import keras_ocr
import datetime
import time
from copy import deepcopy
from decord import VideoReader
from decord import cpu, gpu
import keras_ocr

class vidtofrm:
    def __init__(self, video_path, batch_size, every):
        # objects for keras_ocr and video reader
        self.pipeline = keras_ocr.pipeline.Pipeline()
        self.vr = VideoReader(video_path, ctx = cpu(0))
        print(len(self.vr))
        
        # get the first keras_ocr prediction in each batches
        self.batch_size = batch_size
        self.every = every
   
    def get_predictions(self, size):
        for i in range(0, size):
            frame = self.vr[i * self.every * self.batch_size].asnumpy()
            self.frames[i] = self.pipeline.recognize([frame])
        
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
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        processed_img = deepcopy(frame)

        for box in prediction[0]:
            
            x0, y0 = box[1][0]
            x1, y1 = box[1][1] 
            x2, y2 = box[1][2]
            x3, y3 = box[1][3] 
            

            x_mid0, y_mid0 = self.midpoint(x1, y1, x2, y2)
            x_mid1, y_mi1 = self.midpoint(x0, y0, x3, y3)
            
            thickness = int(np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
            
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255, thickness)
            processed_img = cv2.inpaint(processed_img, mask, 0, cv2.INPAINT_TELEA)
        
        return processed_img

    def extframes(self):
        count = 0
        prediction_groups = None
        for i in range(0, len(self.vr), self.every):
            frame = self.vr[i].asnumpy()
            
            if count == 0 or count % self.batch_size == 0:
                prediction_groups = self.pipeline.recognize([frame])
                
            img = self.removal(prediction_groups, frame)
            save_path = os.path.join("frames/frame" + str(i // self.every) + ".jpeg")

            cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            count += 1
