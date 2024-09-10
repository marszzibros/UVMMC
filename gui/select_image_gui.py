import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import requests
import json

patients = []
files = []
parts = []



with os.scandir("sample_datasets") as entries:
    for entry in entries:
        if entry.is_file():
            files.append(os.path.join('sample_datasets',entry.name))
            patients.append(entry.name.split('_')[0])

            if "H-N" in entry.name:
                parts.append('H')

            if "TORSO" in entry.name:
                parts.append('T')

data = {'patients' : patients,
        'files'    : files,
        'parts'    : parts}

df = pd.DataFrame(data)

file_lists = np.concatenate(df.groupby('patients').agg({'parts':np.sort, 'files':list})['files'].values)

def execute_command():
    count = 0
    user_id = userid_entry.get()
    if user_id:
        mysql_url = f'https://jjung2.w3.uvm.edu/uvmmc/api/read.php?group_id={user_id}'

        response = requests.get(mysql_url)

        # Check for successful request
        if response.status_code == 200:
            # Get the JSON content
            json_data = response.json()

            # Create DataFrame
            try:
                df = pd.DataFrame(json_data['data'])
                target_done = np.array(df['target'])
            except (json.JSONDecodeError, KeyError):
                print("Error: Could not parse JSON response or missing data.")
                target_done = []

        else:
            print("Error:", response.status_code, response.reason)
            target_done = []

        for file in file_lists:
            if count > -1:
                not_done = True
                for done in target_done:
                    if done in file:
                        not_done = False
                        count += 1
                        break

                if not_done:
                    os.system(f"python ct_viewer_gui_temp.py {file} {user_id}")
                    count += 1
                    print(f"{count}/{len(file_lists)}")

            else:
                count +=1
    else:
        messagebox.showwarning("Empty Entry", "Please enter a value in the additional entry box before executing the command.")
    

# Create the main window
root = tk.Tk()
root.title("File Browser")


# Additional entry box
userid_entry = tk.Entry(root, width=40)
userid_entry.grid(row=2, column=1, padx=10, pady=10)

# Button to execute command
button_execute_command = tk.Button(root, text="Execute Command", command=execute_command)
button_execute_command.grid(row=4, column=1, pady=10)

# Start the Tkinter event loop
root.mainloop()
