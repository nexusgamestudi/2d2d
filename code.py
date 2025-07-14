import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import os
import random

data_file = "form_data.json"

class IranArshiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ایران آرشیو")
        self.root.geometry("700x600")
        self.fields = {
            "نام": "",
            "نام خانوادگی": "",
            "شماره تماس": ""
        }
        self.entries = {}
        self.image_path = None

        self.title_label = tk.Label(root, text="", font=("B Nazanin", 28, "bold"), fg="blue")
        self.title_label.pack(pady=15)
        self.animate_title("Iran Archive")

        self.img_btn = tk.Button(root, text="بارگذاری عکس", command=self.load_image)
        self.img_btn.pack(pady=10)

        self.form_frame = tk.Frame(root)
        self.form_frame.pack(padx=20, pady=10, fill=tk.X)
        self.render_form()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        self.save_btn = tk.Button(btn_frame, text="ذخیره اطلاعات", width=15, command=self.save_data)
        self.save_btn.pack(side=tk.LEFT, padx=10)

        self.load_btn = tk.Button(btn_frame, text="بارگذاری اطلاعات", width=15, command=self.load_data)
        self.load_btn.pack(side=tk.LEFT, padx=10)

        self.get_btn = tk.Button(root, text="دریافت فرم اصلاح شده", width=20, command=self.get_modified_form)
        self.get_btn.pack(pady=10)

        self.add_field_btn = tk.Button(root, text="➕ اضافه کردن فیلد جدید", command=self.add_field)
        self.add_field_btn.pack(pady=10)

        self.color_btn = tk.Button(root, text="تغییر رنگ پس‌زمینه", command=self.change_bg_color)
        self.color_btn.pack(pady=10)

    def animate_title(self, text, step=0):
        if step > len(text):
            self.title_label.config(text=text)
            return
        shuffled = list(text)
        for i in range(len(shuffled)):
            if i < step:
                shuffled[i] = text[i]
            else:
                shuffled[i] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        self.title_label.config("".join(shuffled))
        self.root.after(100, lambda: self.animate_title(text, step+1))

    def load_image(self):
        path = filedialog.askopenfilename(title="انتخاب عکس", filetypes=[("فایل‌های عکس", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.image_path = path
            messagebox.showinfo("عکس", "عکس بارگذاری شد اما نمایش داده نمیشود.")

    def render_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        self.entries = {}
        for field in self.fields:
            lbl = tk.Label(self.form_frame, text=field+":", font=("B Nazanin", 14))
            lbl.pack(anchor="w", pady=5)
            entry = tk.Entry(self.form_frame, font=("B Nazanin", 14))
            entry.pack(fill=tk.X, pady=3)
            entry.insert(0, self.fields[field])
            self.entries[field] = entry

    def save_data(self):
       
