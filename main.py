import os
import tkinter as tk
import tkinter.filedialog

def select_folder():
    global folder_path
    folder_path = tkinter.filedialog.askdirectory()

def display_files_and_folders():
    global folder_path
    if folder_path:
        ignore_files = []
        if include_subfolders_var.get():
            ignore_files = read_gitignore(folder_path)
            if not ignore_files:
                text_area.configure(state="normal")
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, "Error: The .gitignore file was not found (it should be in the main folder)")
                text_area.configure(state="disabled")
                return
            contents = find_files_in_subfolders(folder_path, ignore_files)
        else:
            contents = os.listdir(folder_path)
        result = []
        if exclude_gitignore_var.get():
            if ignore_files:
                for item in contents:
                    if item not in ignore_files and not item.startswith('.'):
                        if item.lower().endswith(".lnk") or item.lower().endswith(".url"):
                            item = os.path.splitext(item)[0]
                        result.append(item)
            else:
                for item in contents:
                    if not item.startswith('.'):
                        if item.lower().endswith(".lnk") or item.lower().endswith(".url"):
                            item = os.path.splitext(item)[0]
                        result.append(item)
        else:
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

def read_gitignore(path):
    gitignore_path = os.path.join(path, '.gitignore')
    ignore_files = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_files.append(line)
    return ignore_files

def find_files_in_subfolders(path, ignore_files):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(".lnk") or filename.lower().endswith(".url"):
                filename = os.path.splitext(filename)[0]
            relative_path = os.path.relpath(os.path.join(root, filename), path)
            if relative_path not in ignore_files and not relative_path.startswith('.') and not os.path.basename(root) in ignore_files:
                files.append(relative_path)
    return files

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

include_subfolders_var = tk.BooleanVar()
include_subfolders_checkbox = tk.Checkbutton(root, text="Учитывать файлы в подпапках", variable=include_subfolders_var)
include_subfolders_checkbox.pack(pady=(0, 10))

exclude_gitignore_var = tk.BooleanVar()
exclude_gitignore_checkbox = tk.Checkbutton(root, text="Убрать системные файлы/папки c .gitignore файла", variable=exclude_gitignore_var)
exclude_gitignore_checkbox.pack(pady=(0, 10))

copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard)
copy_button.pack(pady=(0, 10))

text_area = tk.Text(root, width=50, height=20, state="disabled")
text_area.pack(pady=10)

root.mainloop()
