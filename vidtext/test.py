from vidtofrm import vidtofrm 
import cv2
import time

start = time.time()

batch_size = 2
every = 5

vid = vidtofrm("test.avi", batch_size, every)
vid.extframes()
vid.make_vid("result.mp4")

end = time.time()
print(end - start)