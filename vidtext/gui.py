import tkinter as tk
from tkinter import filedialog, messagebox
from vidtofrm import vidtofrm 
import subprocess
import os

"""
simple GUI for the text remover.

tkinter is used, will check if GPU is available

if GPU, it will run vidtofrm faster
if not, it will be slower.

when browsing input or output directory, do not click on files; directory.
"""


# submit button for text remover ()
def submit():
    input_path = input_entry.get()
    output_path = output_entry.get()
    
    gpu = False
    # messagebox saying that users need to specify the input or output locations
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please specify both input and output paths.")
    # if specified
    else:

        # check if nvidia GPU is available, if so, use GPU
        try:
            if subprocess.check_output('nvidia-smi'):
                gpu = True
        # if not do not use GPU
        except Exception:
            gpu = False

        # will check the input directory if videos are available (extension .mp4 or .avi)
        for file in os.listdir(input_path):
            try:
                if ".api" in file or ".mp4" in file:
                    vid = vidtofrm(input_path + "/" + file, 5, 2, gpu)
                    vid.extframes()
                    vid.make_vid(output_path + "/" + file[:-4] + "_output.mp4")
            except:
                write = open(output_path + "/log.txt" , "w")
                write.write(f"{file} caused an error\n")
                write.close()

# browse input directory
def browse_input():
    input_path = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_path)

# browse output directory
def browse_output():
    output_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_path)

# Create the main window
window = tk.Tk()
window.title("Directory Paths")

# Input Directory Entry
input_label = tk.Label(window, text="Input Directory:")
input_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

input_entry = tk.Entry(window, width=40)
input_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

input_button = tk.Button(window, text="Browse", command=browse_input)
input_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

# Output Directory Entry
output_label = tk.Label(window, text="Output Directory:")
output_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

output_entry = tk.Entry(window, width=40)
output_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

output_button = tk.Button(window, text="Browse", command=browse_output)
output_button.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)

# Submit Button
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.grid(row=2, column=0, columnspan=3, pady=20)

# Run the main loop
window.mainloop()