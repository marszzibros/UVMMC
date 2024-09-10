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

file_path = ""
output_path = "regenerated_new"
x_coor = []
y_coor = []

patient = []
mark = []
landmark = []
operator = []
file_path_list = []
part = []



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
for location in range(1,21):
    os.makedirs(f"{output_path}/{location}")

for location in range(1,21):
    os.makedirs(f"{output_path}/{location}/H")
    os.makedirs(f"{output_path}/{location}/T")

for i in range(0, len(table)):
    try:
        if "H-N" in table.iloc[i]['sample_name']:
            g = Generate(file = f"{table.iloc[i]['sample_name']}", path=f"{output_path}/{table.iloc[i]['item_order']}/H/{table.iloc[i]['case_number']}_{table.iloc[i]['group_id']}.png")
            g.deepdrr_regenerate(table.iloc[i]['x'],table.iloc[i]['y'],table.iloc[i]['z'],table.iloc[i]['a'],table.iloc[i]['b'])
            file_path_list.append(f"{output_path}/{table.iloc[i]['item_order']}/H/{table.iloc[i]['case_number']}_{table.iloc[i]['group_id']}.png")
            part.append("upper")

        if "TORSO" in table.iloc[i]['sample_name']:
            g = Generate(file = f"{table.iloc[i]['sample_name']}", path=f"{output_path}/{table.iloc[i]['item_order']}/T/{table.iloc[i]['case_number']}_{table.iloc[i]['group_id']}.png")
            g.deepdrr_regenerate(table.iloc[i]['x'],table.iloc[i]['y'],table.iloc[i]['z'],table.iloc[i]['a'],table.iloc[i]['b'])
            file_path_list.append(f"{output_path}/{table.iloc[i]['item_order']}/T/{table.iloc[i]['case_number']}_{table.iloc[i]['group_id']}.png")
            part.append("lower")

        x_coor.append(table.iloc[i]['x'])
        y_coor.append(table.iloc[i]['y'])
        operator.append(table.iloc[i]['group_id'])
        landmark.append(table.iloc[i]['item_order'])
        patient.append(table.iloc[i]['target'])

    except Exception as e:
        print(e)

df = {'x_coor' : x_coor,
'y_coor' : y_coor,
'operator' : operator,
'landmark' : landmark,
'patient' : patient,
'file_path_list' : file_path_list,
'part' : part}


df = pd.DataFrame(df)

df.to_csv("regenerated_new.csv")

