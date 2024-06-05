import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np

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
        for file in file_lists:
            os.system(f"python ct_viewer_gui_temp.py {file} {user_id}")
            count += 1
            print(f"{count}/{len(file_lists)}")
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
