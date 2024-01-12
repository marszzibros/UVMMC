import dicom2nifti
import os

dicom2nifti.dicom_series_to_nifti("THIN_ST_TORSO", "THIN_ST_TORSO", reorient_nifti=True)
os.system("gzip THIN_ST_TORSO.nii")

