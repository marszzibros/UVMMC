import tkinter as tk
from tkinter import filedialog, messagebox
from vidtofrm import vidtofrm 
import subprocess
import threading
import os

dir_list = []
dir_list_status = []

# Function to update the log box
def update_log(message):
    log_box.config(state=tk.NORMAL)  # Enable editing
    log_box.insert(tk.END, message + "\n")
    log_box.config(state=tk.DISABLED)  # Disable editing
    log_box.see(tk.END)  # Scroll to the end of the log

#
def background_work():
    gpu = False

    submit_button["state"] = "disabled"
    try:
        if subprocess.check_output('nvidia-smi'):
            gpu = True
    except Exception:
        gpu = False


    input_path = input_entry.get()
    output_path = output_entry.get()

    global dir_list
    global dir_list_status

    dir_list = os.listdir(input_path)
    dir_list_status = ["Wait" for i in range(len(dir_list))]

    count = 0

    for file in os.listdir(input_path):
        try:
            if ".avi" in file or ".mp4" in file:
                vid = vidtofrm(input_path + "/" + file, 5, 2, gpu)
                dir_list_status[count] = "Proc"
                vid.extframes()
                vid.make_vid(output_path + "/" + file[:-4] + "_output.mp4")
                dir_list_status[count] = "Done"
            else:
                dir_list_status[count] = "Name"
        except Exception as e:
            error_message = f"{file} caused an error: {str(e)}"
            update_log(error_message)
            write = open(output_path + "/log.txt", "a")  # Append to log file
            write.write(error_message + "\n")
            write.close()
            dir_list_status[count] = "Error"
        count += 1 

def schedule_check(t):
    """
    Schedule the execution of the `check_if_done()` function after
    one second.
    """
    # Clear the log box
    log_box.config(state=tk.NORMAL)
    log_box.delete('1.0', tk.END)
    log_box.config(state=tk.DISABLED)

    text = ""

    global dir_list
    global dir_list_status

    for i in range(len(dir_list)):
        text += f"{dir_list[i]:10s} -- "
        if dir_list_status[i] == "Wait":
            text += f"Waiting\n"
        elif dir_list_status[i] == "Done":
            text += f"Finished\n"
        elif dir_list_status[i] == "Name":
            text += f"Not supporting format\n"
        elif dir_list_status[i] == "Error":
            text += f"Unexpected error\n"
        elif dir_list_status[i] == "Proc":
            input = open("log.txt", "r")
            process = input.readline().rstrip('\n')
            text += f"{process}\n"
            input.close()
        else:
            text += f"failed\n"
    update_log(text)
    window.after(2000, check_if_done, t)

def check_if_done(t):
    # If the thread has finished, re-enable the button and show a message.
    if not t.is_alive():
        # Clear the log box
        log_box.config(state=tk.NORMAL)
        log_box.delete('1.0', tk.END)
        log_box.config(state=tk.DISABLED)

        text = ""

        global dir_list
        global dir_list_status

        for i in range(len(dir_list)):
            text += f"{dir_list[i]:10s} -- "
            if dir_list_status[i] == "Wait":
                text += f"Waiting\n"
            elif dir_list_status[i] == "Done":
                text += f"Finished\n"
            elif dir_list_status[i] == "Name":
                text += f"Not supporting format\n"
            elif dir_list_status[i] == "Error":
                text += f"Unexpected error\n"
            elif dir_list_status[i] == "Proc":
                input = open("log.txt", "r")
                process = input.readline().rstrip('\n')
                text += f"{process}\n"
                input.close()
            else:
                text += f"failed\n"
        update_log(text)
        submit_button["state"] = "normal"
    else:
        # Otherwise check again after one second.
        schedule_check(t)


# submit button for text remover
def submit():
    input_path = input_entry.get()
    output_path = output_entry.get()
    
    # Clear the log box
    log_box.config(state=tk.NORMAL)
    log_box.delete('1.0', tk.END)
    log_box.config(state=tk.DISABLED)
    
    # messagebox saying that users need to specify the input or output locations
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please specify both input and output paths.")
    else:
        t = threading.Thread(target=background_work)
        t.start()
        schedule_check(t)


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

file = []

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

# Log Box
log_box = tk.Text(window, height=15, width=80, state=tk.DISABLED)
log_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W)

# Run the main loop
window.mainloop()