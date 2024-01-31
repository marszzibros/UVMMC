import nibabel as nib

img = nib.load('test_folder/BONE_H-N-UXT_3X3.nii.gz')
header = img.header

print(header)