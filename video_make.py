
import cv2
import numpy as np
import os
 
img_array = []
for i in range(0,len(os.listdir("frames"))):
    img = cv2.imread('frames/frame'+str(i)+'.png')
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()