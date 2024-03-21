from generate_deepdrr import Generate
import os
import requests
import pandas as pd
import shutil

# Function to extract case number
def extract_case_number(path):
    parts = path.split('/')
    for part in parts:
        if part.startswith('case'):
            return part

mysql_url = 'https://jjung2.w3.uvm.edu/uvmmc/api/read.php'

# Make a get request to insert data into the MySQL table
response = requests.get(mysql_url)

table = pd.DataFrame(response.json()['data'])
table['case_number'] = table['target'].apply(extract_case_number)

file_path = "test_folder/"
output_path = "regenerated"
 
if os.path.exists(output_path):
    try:
        shutil.rmtree(output_path)
    except OSError as e:
        print(f"Error: {output_path} : {e.strerror}")
else:
    try:
        os.makedirs(output_path)
    except OSError as e:
        print(f"Error: {output_path} : {e.strerror}")

for location in range(1,12):
    os.makedirs(f"{output_path}/{location}")

for i in range(0, len(table)):
    g = Generate(file = f"{file_path}/{table.iloc[i]['case_number']}.nii.gz", path=f"{output_path}/{table.iloc[i]['item_order']}/{table.iloc[i]['case_number']}_{table.iloc[i]['sample_name']}_{table.iloc[i]['x']}_{table.iloc[i]['y']}_{table.iloc[i]['z']}_{table.iloc[i]['a']}_{table.iloc[i]['b']}_{table.iloc[i]['group_id']}.png")
    g.deepdrr_run(table.iloc[i]['x'],table.iloc[i]['y'],table.iloc[i]['z'],table.iloc[i]['a'],table.iloc[i]['b'])
