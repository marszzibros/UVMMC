import cv2
import matplotlib.pyplot as plt
import os
import deepdrr
from deepdrr import geo
from deepdrr.projector import Projector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

file_name = []
x_ct = []
y_ct = []
z_ct = []

x_modified = []
y_modified = []
z_modified = []

case_number = []
parts = []

file = sys.argv[1]
if "TORSO" in file:
    part = "lower"
else:
    part = "upper"

case = file.split("_")[0]
os.system(f"mkdir test_datasets/{case}")

def filter_image():
    # read image and delete after reading
    image = cv2.imread(f'temp_{file}.png')
    os.system(f"rm -r temp_{file}.png")

    # gracy scale, threshold, and contours
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 40, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # define area
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
 
    # filter
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > max_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if long_vertical_aspect_ratio_range_max[0] <= aspect_ratio <= long_vertical_aspect_ratio_range_max[1]:
                long_black_chunk_detected = True
                break
            elif long_horizontal_aspect_ratio_range_max[0] <= aspect_ratio <= long_horizontal_aspect_ratio_range_max[1]:
                long_black_chunk_detected = True
                break
        elif area > mid_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if long_vertical_aspect_ratio_range_mid[0] <= aspect_ratio <= long_vertical_aspect_ratio_range_mid[1]:
                long_black_chunk_detected = True
                break
            elif long_horizontal_aspect_ratio_range_mid[0] <= aspect_ratio <= long_horizontal_aspect_ratio_range_mid[1]:
                long_black_chunk_detected = True
                break
        elif area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h

            if long_vertical_aspect_ratio_range_min[0] <= aspect_ratio <= long_vertical_aspect_ratio_range_min[1]:
                long_black_chunk_detected = True
                break
            elif long_horizontal_aspect_ratio_range_min[0] <= aspect_ratio <= long_horizontal_aspect_ratio_range_min[1]:
                long_black_chunk_detected = True
        
                break    

    if long_black_chunk_detected:
        # Display the original image with rectangles drawn (if any)
        return False
    else:
        return True
    
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
    
    plt.imsave(f'temp_{file}.png' , image, cmap='gray')
    return image

# define Deepdrr parameters
patient = deepdrr.Volume.from_nifti(f"sample_datasets/{file}.nii.gz", use_thresholding=True)
patient.facedown()
lower, top = patient.get_bounding_box_in_world()

proceed_right = True
proceed_left = True
proceed_top = True
proceed_bottom = True

center_y = 0
center_x = 0
continue_false = 0
# top bottom right left

center_point = [(top[0] + lower[0]) / 2,(top[1] + lower[1]) / 2,(top[2] + lower[2]) / 2]

while proceed_top:
    center_y = 0
    while proceed_right:
        carm = deepdrr.MobileCArm(geo.Point3D((center_point[0], center_point[1], center_point[2], 1)) +  geo.v(center_x, center_y, 0))
        coord = geo.Point3D(((top[0] + lower[0]) / 2,
                                            (top[1] + lower[1]) / 2,
                                            (top[2] + lower[2]) / 2, 1)) + geo.v(center_x, center_y, 0) - lower
        image = generate_image(carm, patient)

        if filter_image() and lower[1] < center_y:
            plt.imsave(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png", image,cmap='gray')

            center_y = center_y - 10
            continue_false = 0
            file_name.append(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png")
            x_ct.append(center_x)
            y_ct.append(center_y)
            z_ct.append(0)
            
            x_modified.append(coord[0])
            y_modified.append(coord[1])
            z_modified.append(coord[2])

            case_number.append(case)
            parts.append(part)

        else:

            proceed_right = False
            continue_false += 1  
            

    center_y = 10
    while proceed_left:
        carm = deepdrr.MobileCArm(geo.Point3D((center_point[0], center_point[1], center_point[2], 1)) +  geo.v(center_x, center_y, 0))
        coord = geo.Point3D(((top[0] + lower[0]) / 2,
                                            (top[1] + lower[1]) / 2,
                                            (top[2] + lower[2]) / 2, 1)) + geo.v(center_x, center_y, 0) - lower
        image = generate_image(carm, patient)

        if filter_image() and top[1] > center_y:
            plt.imsave(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png", image,cmap='gray')

            center_y = center_y + 10
            continue_false = 0
            file_name.append(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png")
            x_ct.append(center_x)
            y_ct.append(center_y)
            z_ct.append(0)
            
            x_modified.append(coord[0])
            y_modified.append(coord[1])
            z_modified.append(coord[2])

            case_number.append(case)
            parts.append(part)
        else:

            proceed_left = False
            continue_false += 1
    
    if continue_false >= 2 or lower[1] > center_x:
        proceed_top = False
    else:
        center_x -= 10 
            
        proceed_right = True
        proceed_left = True

center_x = 10
continue_false = 0
proceed_right = True
proceed_left = True
# top bottom left right
while proceed_bottom:
    center_y = 0
    while proceed_right:
        carm = deepdrr.MobileCArm(geo.Point3D((center_point[0], center_point[1], center_point[2], 1)) +  geo.v(center_x, center_y, 0))
        coord = geo.Point3D(((top[0] + lower[0]) / 2,
                                            (top[1] + lower[1]) / 2,
                                            (top[2] + lower[2]) / 2, 1)) + geo.v(center_x, center_y, 0) - lower
        image = generate_image(carm, patient)

        if filter_image() and lower[1] < center_y:
            plt.imsave(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png", image,cmap='gray')
            center_y = center_y - 10
            continue_false = 0
            file_name.append(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png")
            x_ct.append(center_x)
            y_ct.append(center_y)
            z_ct.append(0)
            
            x_modified.append(coord[0])
            y_modified.append(coord[1])
            z_modified.append(coord[2])

            case_number.append(case)
            parts.append(part)
        else:
            proceed_right = False
            continue_false += 1  

    center_y = 10
    while proceed_left:
        carm = deepdrr.MobileCArm(geo.Point3D((center_point[0], center_point[1], center_point[2], 1)) +  geo.v(center_x, center_y, 0))
        coord = geo.Point3D(((top[0] + lower[0]) / 2,
                                            (top[1] + lower[1]) / 2,
                                            (top[2] + lower[2]) / 2, 1)) + geo.v(center_x, center_y, 0) - lower
        image = generate_image(carm, patient)

        if filter_image() and top[1] > center_y:
            plt.imsave(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png", image,cmap='gray')
            center_y = center_y + 10
            continue_false = 0
            file_name.append(f"test_datasets/{case}/{file}_{center_x}_{center_y}.png")
            x_ct.append(center_x)
            y_ct.append(center_y)
            z_ct.append(0)
            
            x_modified.append(coord[0])
            y_modified.append(coord[1])
            z_modified.append(coord[2])

            case_number.append(case)
            parts.append(part)
        else:
            proceed_left = False
            continue_false += 1
    if continue_false >= 2 or top[1] < center_x:
        proceed_bottom = False
    else:
        center_x += 10
        proceed_right = True
        proceed_left = True

data = {"filename":file_name,
        "x_ct":x_ct,
        "y_ct":y_ct,
        "z_ct":z_ct,
        "x_modified":x_modified,
        "y_modified":y_modified,
        "z_modified":z_modified,
        "case_number":case_number,
        "part":parts}

df = pd.DataFrame(data)
df.to_csv(f"test_datasets/{case}_{part}.csv")