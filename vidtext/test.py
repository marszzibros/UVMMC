from vidtofrm import vidtofrm 
import cv2

batch_size = 5
every = 10

vid = vidtofrm("sample.avi", batch_size, every)
vid.extframes()
vid.make_vid("result.mp4")