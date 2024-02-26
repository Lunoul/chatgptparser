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
        text_area.delete(1.0, tk.END)
        for item in contents:
            if item.lower().endswith(".lnk") or item.lower().endswith(".url"):
                item = os.path.splitext(item)[0]
            text_area.insert(tk.END, item + "\n")
    else:
        print("Please select a folder first.")

root = tk.Tk()
root.title("File and Folder Lister")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

select_button = tk.Button(button_frame, text="Select folder", command=select_folder)
select_button.grid(row=0, column=0, padx=(20, 10))

start_button = tk.Button(button_frame, text="Start", command=display_files_and_folders)
start_button.grid(row=0, column=1, padx=(10, 20))

text_area = tk.Text(root, width=50, height=20)
text_area.pack(pady=10)

root.mainloop()
