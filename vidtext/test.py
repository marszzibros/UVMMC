from vidtofrm import vidtofrm 
import cv2
import time

start = time.time()

batch_size = 10
every = 10

vid = vidtofrm("test.avi", batch_size, every)
vid.extframes()
vid.make_vid("result.mp4")

end = time.time()
print(end - start)