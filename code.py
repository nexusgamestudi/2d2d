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
        self.title_label.config(text="".join(shuffled))
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
        for field in self.entries:
            self.fields[field] = self.entries[field].get()
        try:
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(self.fields, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("ذخیره", "اطلاعات با موفقیت ذخیره شد.")
        except Exception as e:
            messagebox.showerror("خطا", f"در ذخیره اطلاعات مشکلی پیش آمد:\n{e}")

    def load_data(self):
        if not os.path.exists(data_file):
            messagebox.showwarning("هشدار", "هیچ اطلاعاتی برای بارگذاری وجود ندارد.")
            return
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                self.fields = json.load(f)
            self.render_form()
            messagebox.showinfo("بارگذاری", "اطلاعات با موفقیت بارگذاری شد.")
        except Exception as e:
            messagebox.showerror("خطا", f"در بارگذاری اطلاعات مشکلی پیش آمد:\n{e}")

    def get_modified_form(self):
        result = "\n".join(f"{key}: {self.entries[key].get()}" for key in self.entries)
        messagebox.showinfo("فرم اصلاح شده", result)

    def add_field(self):
        new_field = simpledialog.askstring("فیلد جدید", "نام فیلد جدید را وارد کنید:")
        if new_field and new_field.strip() != "":
            self.fields[new_field] = ""
            self.render_form()

    def change_bg_color(self):
        colors = ["#f0f0f0", "#ccffcc", "#ffcccc", "#e6e6fa", "#d0f0c0"]
        current = self.root.cget("bg")
        new_color = random.choice([c for c in colors if c != current])
        self.root.config(bg=new_color)
        self.form_frame.config(bg=new_color)
        for widget in self.form_frame.winfo_children():
            widget.config(bg=new_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = IranArshiveApp(root)
    root.mainloop()
