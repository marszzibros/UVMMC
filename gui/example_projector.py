#! python3
"""Minimal projection example with DeepDRR."""

import deepdrr
from deepdrr import geo
from deepdrr.utils import test_utils, image_utils
from deepdrr.projector import Projector
import sys
import numpy as np
import time


def main():
    start = time.time()
    print("Generating")
    patient = deepdrr.Volume.from_nifti(
        sys.argv[1], use_thresholding=True
    )
    patient.facedown()
	
    # define the simulated C-arm
    carm = deepdrr.MobileCArm(patient.center_in_world + geo.v(float(sys.argv[2]),-float(sys.argv[3]) + 30,-float(sys.argv[4]) - 100), 
                              alpha=-np.rad2deg(float(sys.argv[5])) * 2.7,
                              beta=-np.rad2deg(float(sys.argv[6])) * 2.7)

    # project in the AP view
    with Projector(patient, carm=carm) as projector:

        image = projector()

    path = "example_projector.png"
    image_utils.save(path, image)
    print("Done")
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()
    


