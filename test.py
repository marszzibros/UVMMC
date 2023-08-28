# import libraries
import cv2
import matplotlib.pyplot as plt
import keras_ocr
import os
import numpy as np
import math
import time


test_array = [25,20,15]
ran_detect = 1

# midpoint - get midpoint of text edges
def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

# mse - get mse (mean standard errors) for images; image comparison
def mse(or_img1, or_img2):
   
   # load the input images
  img1 = cv2.imread(or_img1)
  img2 = cv2.imread(or_img2)

  # convert the images to grayscale
  img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

  h, w = img1.shape
  diff = cv2.subtract(img1, img2)
  err = np.sum(diff**2)
  mse = err/(float(h*w))
  return mse

# inpaint_text - extract text from images and remove
def inpaint_text(img_path, pipeline, num, predictions):
    if num == 0 or mse("frames/frame" + str(num - 1) + ".png", "frames/frame" + str(num) + ".png") > 50:
       
      # read image
      img = keras_ocr.tools.read(img_path)
      # generate (word, box) tuples 
      prediction_groups = pipeline.recognize([img])
      mask = np.zeros(img.shape[:2], dtype="uint8")
      

      for box in prediction_groups[0]:
          
          x0, y0 = box[1][0]
          x1, y1 = box[1][1] 
          x2, y2 = box[1][2]
          x3, y3 = box[1][3] 
          
          x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
          x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
          
          thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
          
          cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
          thickness)
          img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
      
      return(img, prediction_groups)
    else:
      print(1)
      # read image
      img = keras_ocr.tools.read(img_path)
      mask = np.zeros(img.shape[:2], dtype="uint8")

      for box in predictions[0]:
          
          x0, y0 = box[1][0]
          x1, y1 = box[1][1] 
          x2, y2 = box[1][2]
          x3, y3 = box[1][3] 
          
          x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
          x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
          
          thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
          
          cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
          thickness)
          img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                  
      return(img, predictions)       
       


for i in range(0,1):

  test_value = test_array[i]

  



  start = time.time()

  vidcap = cv2.VideoCapture('sample.avi')
  success,image = vidcap.read()
  count = 0

  # save frame as JPEG file      
  while success:
    cv2.imwrite("frames/frame%d.png" % count, image)     
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1





  pipeline = keras_ocr.pipeline.Pipeline()
  #read image from the an image path (a jpg/png file or an image url)

  lst = os.listdir("frames") # your directory path
  number_files = len(lst)

  predictions_in_frames = np.empty(number_files ,dtype = object)

  for i in range (0, number_files):
    if i != 0:
      (img, predictions_in_frames[i]) = inpaint_text("frames/frame"+str(i)+".png", pipeline, i, predictions_in_frames[i - 1])
    else:
      (img, predictions_in_frames[i]) = inpaint_text("frames/frame"+str(i)+".png", pipeline, i, predictions_in_frames[i])
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite("frames/frame"+str(i)+".png",img_rgb)



  img_array = []
  for i in range(0,len(os.listdir("frames"))):
      img = cv2.imread('frames/frame'+str(i)+'.png')
      height, width, layers = img.shape
      size = (width,height)
      img_array.append(img)
  
  if ran_detect == 0:
    out = cv2.VideoWriter('project_'+'no_rand'+'_'+str(test_value)+'.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, size)
  else:
    out = cv2.VideoWriter('project_'+'_rand'+'_'+str(test_value)+'.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, size)
  
  for i in range(len(img_array)):
    out.write(img_array[i])
  
  out.release()
  end = time.time()

  time_result_file = open("results.txt", "a")

  if ran_detect == 0:
    time_result_file.write(str(test_value) + " " + " no random took :" + str(end - start) + " seconds to operate\n")
  else:
    time_result_file.write(str(test_value) + " " + " random took :" + str(end - start) + " seconds to operate\n")
  

  time_result_file.close()
