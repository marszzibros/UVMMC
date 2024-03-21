import os
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_directory():
    folder_path = filedialog.askdirectory(initialdir="/home/raymondlab/Documents/UVMMC/test_folder")
    entry_path.delete(0, tk.END)
    entry_path.insert(0, folder_path)

def submit_action():
    selected_directory = entry_path.get()
    if os.path.isdir(selected_directory):
        # Get a list of files in the selected path with the extension ".nii.gz"
        files = [f for f in os.listdir(selected_directory) if os.path.isfile(os.path.join(selected_directory, f)) and f.endswith(".nii.gz")]

        # Clear previous menu items
        file_menu['menu'].delete(0, 'end')

        if files:
            file_var.set(files[0])  # Set the first file as default
            for file in files:
                file_menu['menu'].add_command(label=file, command=lambda f=file: file_var.set(f))

            print(f"Selected Directory: {selected_directory}")
        else:
            messagebox.showinfo("No Files", "No '.nii.gz' files found in the selected path.")
    else:
        messagebox.showwarning("Invalid Directory", "Please select a valid directory.")

def execute_command():
    selected_file = file_var.get()
    selected_directory = entry_path.get()
    additional_entry_value = additional_entry.get()

    if selected_file:
        if additional_entry_value:
            full_file_path = os.path.join(selected_directory, selected_file)
            os.system(f"python ct_viewer_gui.py {full_file_path} {additional_entry_value}")
        else:
            messagebox.showwarning("Empty Entry", "Please enter a value in the additional entry box before executing the command.")
    else:
        messagebox.showwarning("No File Selected", "Please select a '.nii.gz' file before executing the command.")

# Create the main window
root = tk.Tk()
root.title("File Browser")

# Create and place widgets
label_path = tk.Label(root, text="Select Directory:")
label_path.grid(row=0, column=0, padx=10, pady=10)

entry_path = tk.Entry(root, width=40)
entry_path.grid(row=0, column=1, padx=10, pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_directory)
button_browse.grid(row=0, column=2, padx=10, pady=10)

button_submit = tk.Button(root, text="Submit", command=submit_action)
button_submit.grid(row=1, column=1, pady=20)

# Additional entry box
additional_entry = tk.Entry(root, width=40)
additional_entry.grid(row=2, column=1, padx=10, pady=10)

# OptionMenu to display the list of files
file_var = tk.StringVar(root)
file_menu = tk.OptionMenu(root, file_var, "")
file_menu.grid(row=3, column=1, pady=10)

# Button to execute command
button_execute_command = tk.Button(root, text="Execute Command", command=execute_command)
button_execute_command.grid(row=4, column=1, pady=10)

# Start the Tkinter event loop
root.mainloop()
