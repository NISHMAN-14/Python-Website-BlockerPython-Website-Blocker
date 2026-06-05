import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  # Change for Linux/macOS
redirect = "127.0.0.1"
websites_to_block = []
running = False

def add_website():
    website = website_entry.get().strip()
    if website:
        websites_to_block.append(website)
        website_listbox.insert(tk.END, website)
        website_entry.delete(0, tk.END)

def remove_website():
    selected = website_listbox.curselection()
    if selected:
        index = selected[0]
        websites_to_block.remove(website_listbox.get(index))
        website_listbox.delete(index)

def blocker():
    global running
    while running:
        now = datetime.now()
        if 3 <= now.hour < 16:
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in websites_to_block:
                    if website not in content:
                        file.write(f"{redirect} {website}\n")
        else:
            with open(hosts_path, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in websites_to_block):
                        file.write(line)
                file.truncate()
        time.sleep(5)

def start_blocker():
    global running
    if not running:
        running = True
        t = threading.Thread(target=blocker)
        t.start()
        messagebox.showinfo("Started", "Website blocker started.")

def stop_blocker():
    global running
    running = False
    messagebox.showinfo("Stopped", "Website blocker stopped.")

# GUI
root = tk.Tk()
root.title("Website Blocker")

frame = tk.Frame(root)
frame.pack(pady=10)

website_entry = tk.Entry(frame, width=40)
website_entry.grid(row=0, column=0, padx=5)

add_button = tk.Button(frame, text="Add Website", command=add_website)
add_button.grid(row=0, column=1, padx=5)

remove_button = tk.Button(frame, text="Remove Selected", command=remove_website)
remove_button.grid(row=1, column=1, pady=5)

website_listbox = tk.Listbox(root, width=50)
website_listbox.pack(pady=10)

start_button = tk.Button(root, text="Start Blocking", command=start_blocker, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Blocking", command=stop_blocker, bg="red", fg="white")
stop_button.pack(pady=5)

root.mainloop()
