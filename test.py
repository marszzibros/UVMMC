import cv2
import matplotlib.pyplot as plt
import keras_ocr
import os
import numpy as np
import math

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

vidcap = cv2.VideoCapture('sample.mp4')
success,image = vidcap.read()
count = 0

while success:
  cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

pipeline = keras_ocr.pipeline.Pipeline()
#read image from the an image path (a jpg/png file or an image url)

lst = os.listdir("frames") # your directory path
number_files = len(lst)

predictions_in_frames = np.empty(number_files ,dtype = object)

for i in range (0, number_files):
  img = keras_ocr.tools.read("frames/frame"+str(i)+".jpg")

  # Prediction_groups is a list of (word, box) tuples
  prediction_groups = pipeline.recognize([img])

  #print image with annotation and boxes
  keras_ocr.tools.drawAnnotations(image=img, predictions=prediction_groups[0])
  predictions_in_frames[i] = prediction_groups



  
box = prediction_groups[0][10]
x0, y0 = box[1][0]
x1, y1 = box[1][1] 
x2, y2 = box[1][2]
x3, y3 = box[1][3] 
        
x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))