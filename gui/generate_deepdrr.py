#! python3
"""Minimal projection example with DeepDRR."""

import deepdrr
from deepdrr import geo
from deepdrr.utils import test_utils, image_utils
from deepdrr.projector import Projector
import cv2
import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt

class Generate:
    def __init__(self, file, path = "projector.png"):
        """
        Generate class

        Descriptions
        --------------------------------
        generate simulated x-ray image using Deep DRR

        Args
        --------------------------------
        file: str
            file path
        path: str
            output name
        """

        # set volume
        self.patient = deepdrr.Volume.from_nifti(file, use_thresholding=True)
        self.patient.facedown()
        self.path = path

    def deepdrr_run(self, x, y, z, a, b):
        """
        deepdrr_run
        
        Descriptions
        --------------------------------
        generate simulated x-ray image using Deep DRR

        Args
        --------------------------------
        x: float
            x coordinate value from center of the volume
        y: float
            y coordinate value from center of the volume
        z: float
            z coordinate value from center of the volume
        a: float
            alpha value in radient
        b: float
            beta value in radient

        """

        # define the simulated C-arm
        carm = deepdrr.MobileCArm(self.patient.center_in_world + geo.v(float(x) ,-float(y),-float(z) * 1.5), 
                                alpha=-np.rad2deg(float(a)),
                                beta=-np.rad2deg(float(b)))

        # project in the AP view
        with Projector(self.patient, carm=carm) as projector:

            image = projector()


        equalized_image = exposure.equalize_adapthist(image/np.max(image))

        # Get the center coordinates of the image
        center_x = equalized_image.shape[1] // 2
        center_y = equalized_image.shape[0] // 2

        # Create a copy of the equalized image
        image_with_cross = equalized_image.copy()

        # Define the size of the cross
        cross_size = 20

        # Draw horizontal and vertical lines for the cross
        image_with_cross[center_y - cross_size // 2: center_y + cross_size // 2 + 1, :] = 1
        image_with_cross[:, center_x - cross_size // 2: center_x + cross_size // 2 + 1] = 1

        # Create a mesh grid for the circle
        x, y = np.meshgrid(np.arange(image_with_cross.shape[1]), np.arange(image_with_cross.shape[0]))
        dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

        # Draw a circle in the middle
        image_with_cross[dist <= cross_size // 2] = 1
        plt.imsave('projector.png', image_with_cross, cmap='gray')

    def empty_file(self):
        """
        empty_file
        
        Descriptions
        --------------------------------
        remove previously generated files; create an image with white background
        """
        image_utils.save(self.path, np.ones((1536, 1536))) 



