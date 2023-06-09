import os
import tkinter as tk
from tkinter import filedialog, messagebox

def search_files(directory, pattern):
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if pattern.lower() in file.lower():
                results.append(os.path.join(root, file))
    return results

def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(tk.END, directory)

def search():
    directory = directory_entry.get()
    pattern = pattern_entry.get()

    if not directory or not pattern:
        messagebox.showwarning("Warning", "Please enter both a directory and a file pattern.")
        return

    found_files = search_files(directory, pattern)

    if found_files:
        result_text.delete(1.0, tk.END)
        for file_path in found_files:
            result_text.insert(tk.END, file_path + "\n")
    else:
        messagebox.showinfo("No Files Found", "No files matching the pattern were found.")

# Create the main window
window = tk.Tk()
window.title("File Search Engine")

# Create and place the widgets
directory_label = tk.Label(window, text="Directory:")
directory_label.pack()
directory_entry = tk.Entry(window, width=50)
directory_entry.pack()
browse_button = tk.Button(window, text="Browse", command=browse_directory)
browse_button.pack()

pattern_label = tk.Label(window, text="File Pattern:")
pattern_label.pack()
pattern_entry = tk.Entry(window, width=50)
pattern_entry.pack()

search_button = tk.Button(window, text="Search", command=search)
search_button.pack()

result_label = tk.Label(window, text="Results:")
result_label.pack()
result_text = tk.Text(window, height=10, width=80)
result_text.pack()

# Start the main loop
window.mainloop()
