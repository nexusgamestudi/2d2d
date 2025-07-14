import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
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

        self.image_panel = tk.Label(root)
        self.image_panel.pack(pady=10)

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
            img = Image.open(path)
            img.thumbnail((300,300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_panel.config(image=img_tk)
            self.image_panel.image = img_tk

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
        data = {}
        for field, entry in self.entries.items():
            data[field] = entry.get()
        if self.image_path:
            data["_image_path"] = self.image_path
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        messagebox.showinfo("ذخیره", "اطلاعات ذخیره شد!")

    def load_data(self):
        if os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for field in data:
                if field != "_image_path" and field not in self.fields:
                    self.fields[field] = ""
            self.fields.update({k: v for k, v in data.items() if k != "_image_path"})
            self.render_form()
            if "_image_path" in data and os.path.exists(data["_image_path"]):
                self.image_path = data["_image_path"]
                img = Image.open(self.image_path)
                img.thumbnail((300,300))
                img_tk = ImageTk.PhotoImage(img)
                self.image_panel.config(image=img_tk)
                self.image_panel.image = img_tk
            else:
                self.image_panel.config(image='')
                self.image_panel.image = None
            messagebox.showinfo("بارگذاری", "اطلاعات بارگذاری شد.")
        else:
            messagebox.showinfo("اطلاعات", "اطلاعاتی یافت نشد.")

    def get_modified_form(self):
        result = "فرم اصلاح شده:\n\n"
        for field, entry in self.entries.items():
            result += f"{field}: {entry.get()}\n"
        if self.image_path:
            result += f"\nمسیر عکس:\n{self.image_path}"
        else:
            result += "\nعکسی بارگذاری نشده."
        top = tk.Toplevel(self.root)
        top.title("فرم اصلاح شده")
        top.geometry("400x400")
        text = tk.Text(top, font=("B Nazanin", 12))
        text.pack(expand=True, fill=tk.BOTH)
        text.insert(tk.END, result)
        text.config(state=tk.DISABLED)

    def add_field(self):
        new_field = simpledialog.askstring("فیلد جدید", "نام فیلد جدید را وارد کنید:")
        if new_field:
            if new_field in self.fields:
                messagebox.showwarning("هشدار", "این فیلد قبلا وجود دارد.")
                return
            self.fields[new_field] = ""
            self.render_form()

    def change_bg_color(self):
        colors = ["#ffffff", "#f0f8ff", "#ffe4e1", "#e6e6fa", "#f5f5dc", "#fafad2"]
        current = self.root.cget("bg")
        next_color = colors[(colors.index(current) + 1) % len(colors)] if current in colors else colors[0]
        self.root.config(bg=next_color)
        self.form_frame.config(bg=next_color)
        self.image_panel.config(bg=next_color)
        for widget in self.form_frame.winfo_children():
            widget.config(bg=next_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=next_color)

root = tk.Tk()
app = IranArshiveApp(root)
root.mainloop()
