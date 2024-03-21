#! python3
"""Minimal projection example with DeepDRR."""

import deepdrr
from deepdrr import geo
from deepdrr.utils import test_utils, image_utils
from deepdrr.projector import Projector
import numpy as np

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
        carm = deepdrr.MobileCArm(self.patient.center_in_world + geo.v(float(x) ,-float(y),-float(z) * 1.2), 
                                alpha=-np.rad2deg(float(a)),
                                beta=-np.rad2deg(float(b)))

        # project in the AP view
        with Projector(self.patient, carm=carm) as projector:

            image = projector()

        # save image
        image_utils.save(self.path, image) 

    def empty_file(self):
        """
        empty_file
        
        Descriptions
        --------------------------------
        remove previously generated files; create an image with white background
        """
        image_utils.save(self.path, np.ones((1536, 1536))) 



