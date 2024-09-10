import os

file_names = os.listdir("sample_datasets/")


for file in file_names:
    try:
        if file != "cache":
            name = file.split(".")[0]
            os.system(f"python3 test_filter.py {name}")
    except:
        print(file)