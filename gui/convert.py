import dicom2nifti
import os
import threading

def process_file(file_path, name):
    try:
        dicom2nifti.dicom_series_to_nifti(file_path + name, "test_folder/" + name, reorient_nifti=True) 
        os.system("gzip test_folder/" + name + ".nii")
    except Exception as e:
        print(f"Attempt failed in {name}: {str(e)}")

file_path = "case_3/"
output_folder = "test_folder/"

threads = []

for name in os.listdir(file_path):
    print(name)
    thread = threading.Thread(target=process_file, args=(file_path, name))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All threads have finished.")