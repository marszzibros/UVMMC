from paddleocr import PaddleOCRVL
import cv2
import numpy as np
from copy import deepcopy
import json
import os
os.environ["FLAGS_allocator_strategy"] = "naive_best_fit"
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "1"
"""
vidtofrm (class)
Take a video to detect and remove all texts using ocr

video_path  : (string) specifying video path
batch_size  : (int) every batch_size, the OCR will detect the text; 
    (high batch_size will cause the lower accuracy, and vice versa)

every       : (int) specify how many frames you want to skip 
    (may lower the fps (frame rate) but increase the speed of the process)

gpu         : (bool) using GPU will increase the speed dramatically
"""
class vidtofrm:
    def __init__(self, video_path, batch_size):

        # objects for paddleocr and video reader 
        self.pipeline = PaddleOCRVL()
        self.vr = cv2.VideoCapture(video_path)
        

        self.batch_size = batch_size

        self.img_array = []

    """
    removal (method)
    remove texts based on the text predictions by easyocr

    prediction  : (narray) results of ocr; consists of texts, and coordinates
    frame       : (narray) cv2 processed frame
    """
    def removal(self, prediction, frame):

        processed_img = deepcopy(frame)

        for box in prediction:

            x1, y1, x2, y2 = box['coordinate']
            

            # get coordinate from the predictions and draw a white box
            for i in range(int(x1//1), int(x2//1)):
                for j in range(int(y1//1), int(y2//1)):
                    processed_img[j][i] = (255,255,255)

        return processed_img
    
    """
    mse (method)
    calculate the difference between two images (optional)

    img1 : (narray) the previous frame
    img2 : (narray) the current frame
    """
    def mse(self, img1, img2):

        # convert the images to grayscale
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse

    """
    extframes (method)
    extract frames from video and conduct predictions on the frame
    """
    def extframes(self):
        count = 0
        prediction_groups = None
        pre_image = None
        frm_num = self.vr.get(cv2.CAP_PROP_FRAME_COUNT)

        # get the number of frames
        for i in range(0, int(self.vr.get(cv2.CAP_PROP_FRAME_COUNT))):
            success, frame = self.vr.read()


            # every batch_size, it will redo the text predictions
            if count % self.batch_size == 0: # (optional - increase the accuracy but speed) or self.mse(pre_frame,frame) > 15:
                print("count: ", count)
                prediction_groups = self.pipeline.predict(frame)
                # pre_frame = deepcopy (frame) # need this line to activate the mse

            # remove text based on the predictions
            img = self.removal(prediction_groups[0]["layout_det_res"]["boxes"], frame)

            # save it into numpy array
            self.img_array.append(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

            count += 1            

            progress = open("log.txt", "w")
            progress.write(f"{count}/{(frm_num)}")
            progress.close()

    """
    make_vid (method)
    make video using the array created from the previous process
    
    file_path : file path(string)
    """
    def make_vid(self, file_path):
        height, width, layers = self.img_array[0].shape
        size = (width, height)

        original_fps = int(self.vr.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter(file_path,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), original_fps, size)
        for i in range(len(self.img_array)):
            out.write(self.img_array[i])
        out.release()