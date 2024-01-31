from vedo import *
import dicom2nifti
import os

file_path = "test_folder/"
img_path = "img_folder/"

for name in os.listdir(file_path):
    print(name)
    try:
        plt = Plotter()
        ct = Volume(f"{file_path}{name}")
        plt += ct
        plt.look_at("xz")
        plt.camera.Azimuth(180)
        plt = show(interactive=False).screenshot(f'{img_path}{name[:-7]}.png')
    except:
        print(f"{name} img save error")

