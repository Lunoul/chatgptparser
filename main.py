import tkinter as tk
import tkinter.filedialog
import os

def select_folder():
    global folder_path
    folder_path = tkinter.filedialog.askdirectory()

def display_files_and_folders():
    global folder_path
    if folder_path:
        contents = os.listdir(folder_path)
        result = []
        for item in contents:
            if item.lower().endswith(".lnk") or item.lower().endswith(".url"):
                item = os.path.splitext(item)[0]
            result.append(item)
        if use_commas_var.get():
            output = ", ".join(result)
        else:
            output = "\n".join(result)
        text_area.configure(state="normal")
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, output)
        text_area.configure(state="disabled")
        text_area.update_idletasks()
        text_area.see(tk.END)
    else:
        print("Please select a folder first.")

def copy_to_clipboard():
    text_area.configure(state="normal")
    text_area.clipboard_clear()
    text_area.clipboard_append(text_area.get(1.0, tk.END))
    text_area.configure(state="disabled")

root = tk.Tk()
root.title("File and Folder Lister")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

select_button = tk.Button(button_frame, text="Select folder", command=select_folder)
select_button.grid(row=0, column=0, padx=(20, 10))

start_button = tk.Button(button_frame, text="Start", command=display_files_and_folders)
start_button.grid(row=0, column=1, padx=(10, 20))

use_commas_var = tk.BooleanVar()
use_commas_checkbox = tk.Checkbutton(root, text="Ставить через запятую", variable=use_commas_var)
use_commas_checkbox.pack(pady=(0, 10))

copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard)
copy_button.pack(pady=(0, 10))

text_area = tk.Text(root, width=50, height=20, state="normal")
text_area.pack(pady=10)

root.mainloop()