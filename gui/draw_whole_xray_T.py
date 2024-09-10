import deepdrr
from deepdrr import geo
from deepdrr.projector import Projector
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
import pandas as pd
import os
import requests
import shutil
import cv2

# Function to extract case number
def extract_case_number(path):
    parts = path.split('/')
    for part in parts:
        if part.startswith('case'):
            return part

# Function to generate projection images
def get_projection_image(offset_x, offset_y, patient):

    # define the simulated C-arm
    carm = deepdrr.MobileCArm(patient.center_in_world + geo.v(offset_x, offset_y, 0))

    # project in the AP view
    with Projector(patient, 
                    carm=carm, 
                    spectrum="60KV_AL35", 
                    attenuate_outside_volume=True, 
                    photon_count=50000,
                    ) as projector:

        image = projector()
    

    equalized_image = exposure.equalize_adapthist(image/np.max(image))
    plt.imsave("temp.png", equalized_image, cmap='gray')
    image = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
    
    # Apply Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))

    image = clahe.apply(image)
    return image

mysql_url = 'https://jjung2.w3.uvm.edu/uvmmc/api/read.php'

# Make a get request to insert data into the MySQL table
response = requests.get(mysql_url)

table = pd.DataFrame(response.json()['data'])
table['case_number'] = table['target'].apply(extract_case_number)


for case_num in set(table['case_number']):
    try:
        # Load the patient volume
        patient = deepdrr.Volume.from_nifti(f"sample_datasets/{case_num}_BONE_TORSO_3_X_3.nii.gz", use_thresholding=True)
        patient.facedown()
        lower, top = patient.get_bounding_box_in_world()

        half_center = (top[1] - lower[1]) / 3
        positions_hor = [half_center, 0, -half_center]

        multiply = 0
        center_x = patient.center_in_world[0]
        for i in range(0, 10):
            center_x = center_x - half_center
            multiply += 1
            if center_x < lower[0]:
                break
        
        positions_ver = [i * half_center for i in range(-multiply, multiply + 1)]

        # Generate the images
        images = [[get_projection_image(pos_x, pos_y, patient) for pos_y in positions_hor] for pos_x in positions_ver]

        # Calculate the total width and the maximum height for the combined image
        heights, widths = (images[0][0].shape[0] * len(positions_ver), images[0][0].shape[1] * len(positions_hor))

        # Create a new blank array with the calculated width and height
        combined_image = np.zeros((heights, widths), dtype=images[0][0].dtype)

        # Paste the images into the new array
        y_offset = 0
        for img_line in images:
            x_offset = 0
            for img in img_line:
                combined_image[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
                x_offset += img.shape[1]
            y_offset += img.shape[0]

        filtered_table = table[table.apply(lambda row: 'BONE_TORSO_3_X_3' in row.values, axis=1) & (table['case_number'] == case_num)]
        cv2.imwrite(f"whole_body/T/{case_num}.png", combined_image)

    except Exception as e:
        print(e)

