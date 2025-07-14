import tkinter as tk

def show_main_ui():
    label.config(text="Welcome to Iran Archive!")

root = tk.Tk()
root.title("Iran Archive")
root.geometry("400x200")

label = tk.Label(root, text="Updating...", font=("Arial", 16))
label.pack(expand=True)

root.after(2000, show_main_ui)

root.mainloop()
