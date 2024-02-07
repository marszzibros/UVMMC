#! python3
"""Minimal projection example with DeepDRR."""

import deepdrr
from deepdrr import geo
from deepdrr.utils import test_utils, image_utils
from deepdrr.projector import Projector
import numpy as np

class Generate:
    def __init__(self, file, path = "projector.png"):
        self.patient = deepdrr.Volume.from_nifti(file, use_thresholding=True)
        self.patient.facedown()
        self.path = path

    def deepdrr_run(self, x, y, z, a, b):
        print("generating")
        # define the simulated C-arm
        carm = deepdrr.MobileCArm(self.patient.center_in_world + geo.v(float(x) ,-float(y),-float(z) -250), 
                                alpha=-np.rad2deg(float(a)),
                                beta=-np.rad2deg(float(b)))

        # project in the AP view
        with Projector(self.patient, carm=carm) as projector:

            image = projector()

        image_utils.save(self.path, image) 
        print("done")
    def empty_file(self):
        image_utils.save(self.path, np.ones((1536, 1536))) 



