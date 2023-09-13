from vidtofrm import vidtofrm 
import time
import cv2
import os

batch_size = 5
every = 10

vid = vidtofrm("test.avi", batch_size, every)

start_time = time.time()

vid.extframes()

img_array = []


for i in range(0,len(os.listdir("frames"))-1):
    img = cv2.imread('frames/frame'+str(i)+'.jpeg')
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


cap = cv2.VideoCapture("test.avi") 
original_fps = int(cap.get(cv2.CAP_PROP_FPS))


out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), original_fps // every, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

end_time = time.time()
print(end_time - start_time)