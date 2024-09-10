import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import deepdrr
from deepdrr.utils import image_utils
from deepdrr import geo
from deepdrr.projector import Projector
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
import pandas as pd

import cv2
import sys

file = sys.argv[1]

def filter_image():
    image = cv2.imread('temp2.png')
    os.system("rm -r temp2.png")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 45, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(gray_image, contours, -1, (0,255,75), 2)
    plt.imsave("contour.png", img)
    max_area = 400000
    mid_area = 250000
    min_area = 10000

    long_vertical_aspect_ratio_range_max = (0.5, 1)
    long_horizontal_aspect_ratio_range_max = (2, 10)

    long_vertical_aspect_ratio_range_mid = (0.1, 0.5)
    long_horizontal_aspect_ratio_range_mid = (2, 10)

    long_vertical_aspect_ratio_range_min = (0.01, 0.1)
    long_horizontal_aspect_ratio_range_min = (10, 100)

    long_black_chunk_detected = False
 
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > max_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if long_vertical_aspect_ratio_range_max[0] <= aspect_ratio <= long_vertical_aspect_ratio_range_max[1]:
                long_black_chunk_detected = True
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
            elif long_horizontal_aspect_ratio_range_max[0] <= aspect_ratio <= long_horizontal_aspect_ratio_range_max[1]:
                long_black_chunk_detected = True
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                break
        elif area > mid_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if long_vertical_aspect_ratio_range_mid[0] <= aspect_ratio <= long_vertical_aspect_ratio_range_mid[1]:
                long_black_chunk_detected = True
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
            elif long_horizontal_aspect_ratio_range_mid[0] <= aspect_ratio <= long_horizontal_aspect_ratio_range_mid[1]:
                long_black_chunk_detected = True
                
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                break
        elif area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if long_vertical_aspect_ratio_range_min[0] <= aspect_ratio <= long_vertical_aspect_ratio_range_min[1]:
                long_black_chunk_detected = True
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
            elif long_horizontal_aspect_ratio_range_min[0] <= aspect_ratio <= long_horizontal_aspect_ratio_range_min[1]:
                long_black_chunk_detected = True
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break    
        # Display the thresholded image showing black regions
    plt.imsave("thres.png", thresh, cmap='gray')
    plt.title('Thresholded Image (Black Regions)')
    plt.imsave("rec.png", image)
    plt.title('Image with Detected Rectangles')

    if long_black_chunk_detected:
        # Display the original image with rectangles drawn (if any)

        return False
    else:
        return True
    

patient = deepdrr.Volume.from_nifti(f"sample_datasets/{file}.nii.gz", use_thresholding=True)
patient.facedown()
lower, top = patient.get_bounding_box_in_world()


def generate_image(carm, patient):
    # project in the AP view
    # project in the AP view
    with Projector(patient, 
                carm=carm, 
                spectrum="60KV_AL35", 
                attenuate_outside_volume=True, 
                photon_count=50000,
                ) as projector:

        image = projector()
    

    plt.imsave('temp2.png' , image, cmap='gray')


    return image


carm = deepdrr.MobileCArm(geo.Point3D(((top[0] + lower[0]) / 2,
                                       (top[1] + lower[1]) / 2,
                                       (top[2] + lower[2]) / 2, 1)) +  geo.v(-200, 0, 0),alpha=-5.5,beta=20,gamma=20)
coord = geo.Point3D(((top[0] + lower[0]) / 2,
                                       (top[1] + lower[1]) / 2,
                                       (top[2] + lower[2]) / 2, 1)) +  geo.v(-307.5, -252.5, 0) - lower
print(lower)
print(coord)
image = generate_image(carm, patient)
filter_image()
