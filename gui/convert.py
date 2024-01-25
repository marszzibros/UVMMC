import dicom2nifti
import os


file_path = "/media/marszzibros/New Volume/case-100968/STANDARD_HEAD-NECK/"

for name in os.listdir(file_path):

    print(name)
    try:
        dicom2nifti.dicom_series_to_nifti(file_path + name, "test_folder/" + name, reorient_nifti=True) 
        os.system("gzip test_folder/" + name + ".nii")
    except:
        print(f"attempt fail in {name}")

