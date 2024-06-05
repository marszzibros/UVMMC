import dicom2nifti
import os
import threading
file_to_process = ["BONE_H-N-UXT_3X3", "BONE_L-EXT_3X3", "BONE_TORSO_3_X_3"]

def process_file(file_path, name, case_name):
    try:
        dicom2nifti.dicom_series_to_nifti(file_path + name, "test_folder/" + case_name + "/" + name, reorient_nifti=True) 
        os.system("gzip " + "test_folder/" + case_name + "/" + name +".nii")
    except Exception as e:
        print(f"Attempt failed in {name}: {str(e)}")

file_path = "../data"
output_folder = "test_folder/"

threads = []

for name in os.listdir(file_path):
    if name[-3:] != 'zip':
        os.system(f"mkdir test_folder/{name}")
        file_path_spec = file_path + "/" + name + "/omi/incomingdir/" + name + "/STANDARD_HEAD-NECK-U-EXT/"
        for ct_name_bone in file_to_process:
            
            thread = threading.Thread(target=process_file, args=(file_path_spec, ct_name_bone, name))
            thread.start()
            threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All threads have finished.")

print(os.listdir(file_path))