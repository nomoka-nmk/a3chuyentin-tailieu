import os
import json
import random
import string
import shutil
from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocumentManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("A3 Chuyên Tin - Tài Liệu")
        self.geometry("1200x800")
        self.iconbitmap('favicon.ico')
        self.documents = []
        self.current_file_path = None
        self.json_path = os.path.join("assets", "documents", "documents.json")
        self.files_dir = os.path.join("assets", "documents", "files")
        os.makedirs(self.files_dir, exist_ok=True)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=0)
        self.main_frame.pack(pady=0, padx=0, fill="both", expand=True)

        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#1A1A1A", corner_radius=0)
        header_frame.pack(fill="x")
        title_label = ctk.CTkLabel(
            header_frame,
            text="QUẢN LÝ TÀI LIỆU A3",
            font=ctk.CTkFont(family="Georgia", size=26, weight="bold"),
            text_color="#FFFFFF",
            padx=20,
            pady=15
        )
        title_label.pack(side="left")
        save_btn = ctk.CTkButton(
            header_frame,
            text="💾 Lưu Dữ Liệu",
            command=self.save_data,
            fg_color="#D4A017",
            hover_color="#B88A14",
            font=ctk.CTkFont(family="Georgia", size=14, weight="bold"),
            text_color="#FFFFFF",
            width=150
        )
        save_btn.pack(side="right", padx=20)

        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        list_panel = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=10, width=350)
        list_panel.pack(side="left", fill="y", padx=(0, 15))
        list_panel.pack_propagate(False)

        list_title = ctk.CTkLabel(
            list_panel,
            text="Danh Sách Tài Liệu",
            font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
            text_color="#1A1A1A",
            anchor="w",
            padx=15,
            pady=10
        )
        list_title.pack(fill="x")

        self.listbox = tk.Listbox(
            list_panel,
            bg="#FFFFFF",
            fg="#1A1A1A",
            selectbackground="#1A1A1A",
            selectforeground="#FFFFFF",
            font=("Georgia", 14),
            borderwidth=1,
            relief="flat",
            highlightthickness=0
        )
        self.listbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        details_panel = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=10)
        details_panel.pack(side="left", fill="both", expand=True)

        details_title = ctk.CTkLabel(
            details_panel,
            text="Chi Tiết Tài Liệu",
            font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
            text_color="#1A1A1A",
            anchor="w",
            padx=15,
            pady=10
        )
        details_title.pack(fill="x")

        form_frame = ctk.CTkFrame(details_panel, fg_color="transparent")
        form_frame.pack(fill="both", padx=15, pady=10)

        self.inputs = {
            "id": ctk.CTkEntry(form_frame, font=("Georgia", 14), fg_color="#F0F0F0", border_color="#1A1A1A", text_color="#1A1A1A"),
            "name": ctk.CTkEntry(form_frame, font=("Georgia", 14), fg_color="#F0F0F0", border_color="#1A1A1A", text_color="#1A1A1A"),
            "displayName": ctk.CTkEntry(form_frame, font=("Georgia", 14), fg_color="#F0F0F0", border_color="#1A1A1A", text_color="#1A1A1A"),
            "type": ctk.CTkEntry(form_frame, font=("Georgia", 14), fg_color="#F0F0F0", border_color="#1A1A1A", text_color="#1A1A1A"),
            "description": ctk.CTkEntry(form_frame, font=("Georgia", 14), fg_color="#F0F0F0", border_color="#1A1A1A", text_color="#1A1A1A"),
            "tags": ctk.CTkEntry(form_frame, font=("Georgia", 14), fg_color="#F0F0F0", border_color="#1A1A1A", text_color="#1A1A1A"),
            "uploadDate": DateEntry(
                form_frame,
                date_pattern="dd/mm/yyyy",
                font=("Georgia", 14),
                background="#1A1A1A",
                foreground="#FFFFFF",
                borderwidth=1,
                selectbackground="#1A1A1A",
                selectforeground="#FFFFFF"
            ),
            "fileName": ctk.CTkLabel(form_frame, text="Chưa có file", font=("Georgia", 14), text_color="#1A1A1A")
        }

        fields = [
            ("Mã tài liệu:", self.inputs["id"]),
            ("Tên file (không đuôi):", self.inputs["name"]),
            ("Tên hiển thị:", self.inputs["displayName"]),
            ("Loại file:", self.inputs["type"]),
            ("Mô tả:", self.inputs["description"]),
            ("Tags (cách nhau bằng dấu phẩy):", self.inputs["tags"]),
            ("Ngày upload:", self.inputs["uploadDate"]),
            ("File đính kèm:", self.inputs["fileName"])
        ]

        for i, (label_text, widget) in enumerate(fields):
            label = ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(family="Georgia", size=14, weight="bold"), text_color="#1A1A1A")
            label.grid(row=i, column=0, padx=10, pady=8, sticky="w")
            widget.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
            form_frame.grid_columnconfigure(1, weight=1)

        self.btn_file = ctk.CTkButton(
            form_frame,
            text="📁 Chọn File",
            command=self.select_file,
            fg_color="#2A2A2A",
            hover_color="#1A1A1A",
            font=ctk.CTkFont(family="Georgia", size=14, weight="bold"),
            text_color="#FFFFFF"
        )
        self.btn_file.grid(row=len(fields), column=0, columnspan=2, pady=15, sticky="ew")

        btn_frame = ctk.CTkFrame(details_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=10)

        buttons = [
            ("➕ Thêm Mới", self.add_document, "#28A745"),
            ("✏️ Cập Nhật", self.update_document, "#007BFF"),
            ("🗑️ Xóa", self.delete_document, "#DC3545")
        ]

        for text, handler, color in buttons:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=handler,
                fg_color=color,
                hover_color=self.darken_color(color),
                font=ctk.CTkFont(family="Georgia", size=14, weight="bold"),
                text_color="#FFFFFF",
                width=120
            )
            btn.pack(side="left", padx=10)

    def darken_color(self, hex_color, amount=20):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, val - amount) for val in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def load_data(self):
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
                    for doc in self.documents:
                        for file in os.listdir(self.files_dir):
                            if os.path.splitext(file)[0] == doc['fileName']:
                                doc['fileName'] = file
                                break
                    self.documents.sort(key=lambda x: int(x["id"]))
            else:
                self.documents = []
            self.update_list()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file JSON:\n{str(e)}")
            self.documents = []

    def save_data(self):
        try:
            documents_to_save = []
            for doc in self.documents:
                doc_copy = doc.copy()
                doc_copy['fileName'] = os.path.splitext(doc['fileName'])[0]
                documents_to_save.append(doc_copy)
            
            documents_to_save.sort(key=lambda x: int(x["id"]))
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(documents_to_save, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Thành công", "Đã lưu dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}")

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for doc in self.documents:
            self.listbox.insert(tk.END, f"{doc['id']} - {doc['displayName']}")

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        doc = self.documents[index]
        self.inputs["id"].delete(0, tk.END)
        self.inputs["id"].insert(0, doc.get("id", ""))
        self.inputs["name"].delete(0, tk.END)
        self.inputs["name"].insert(0, os.path.splitext(doc.get("fileName", ""))[0])
        self.inputs["displayName"].delete(0, tk.END)
        self.inputs["displayName"].insert(0, doc.get("displayName", ""))
        self.inputs["type"].delete(0, tk.END)
        self.inputs["type"].insert(0, doc.get("type", ""))
        self.inputs["description"].delete(0, tk.END)
        self.inputs["description"].insert(0, doc.get("description", ""))
        self.inputs["tags"].delete(0, tk.END)
        self.inputs["tags"].insert(0, ", ".join(doc.get("tags", [])))
        date_str = doc.get("uploadDate", "")
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            self.inputs["uploadDate"].set_date(date)
        self.inputs["fileName"].configure(text=doc.get("fileName", "Chưa có file"))
        self.current_file_path = None

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file tài liệu",
            filetypes=[
                ("All Files", "*.*"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.doc;*.docx"),
                ("Excel Files", "*.xls;*.xlsx"),
                ("Image Files", "*.png;*.jpg;*.jpeg"),
                ("Video Files", "*.mp4;*.avi;*.mkv"),
                ("Text Files", "*.txt")
            ]
        )
        if file_path:
            self.current_file_path = file_path
            self.inputs["fileName"].configure(text=os.path.basename(file_path))
            file_ext = os.path.splitext(file_path)[1].lower()
            suggested_type = {
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.mp4': 'video/mp4',
                '.avi': 'video/x-msvideo',
                '.mkv': 'video/x-matroska',
                '.txt': 'text/plain'
            }.get(file_ext, 'application/octet-stream')
            self.inputs["type"].delete(0, tk.END)
            self.inputs["type"].insert(0, suggested_type)

    def generate_id(self):
        if not self.documents:
            return "1"
        max_id = max(int(doc["id"]) for doc in self.documents)
        return str(max_id + 1)

    def generate_random_filename(self, original_name):
        ext = os.path.splitext(original_name)[1]
        name = self.inputs["name"].get().strip()
        if not name:
            name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        base_name = name
        counter = 1
        while True:
            new_filename = f"{base_name}{ext}"
            if not os.path.exists(os.path.join(self.files_dir, new_filename)):
                return new_filename
            base_name = f"{name}_{counter}"
            counter += 1

    def create_html_for_document(self, doc):
        file_ext = os.path.splitext(doc['fileName'])[1].lower()
        file_url = f"https://chuyentin-tailieu.a3sachhonaba.com/assets/documents/files/{doc['fileName']}"
        
        if file_ext == '.pdf':
            content = f"""
                <div class="content-box mb-12 bg-white dark:bg-gray-850 p-6 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                    <h2 class="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">PDF</h2>
                    <div class="w-full h-96 border-2 border-gray-300 dark:border-gray-600 rounded-md overflow-hidden" style="max-height: 100%; max-width: 100%; height: 100vh; width: 100vw;">
                        <iframe src="https://chuyentin-tailieu.a3sachhonaba.com/viewer/pdf/web/viewer.html?file={file_url}" class="w-full h-full" frameborder="0"></iframe>
                    </div>
                </div>
            """
        elif file_ext in ('.png', '.jpg', '.jpeg', '.webp'):
            content = f"""
                <div class="content-box mb-12 bg-white dark:bg-gray-850 p-6 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                    <h2 class="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Hình Ảnh</h2>
                    <div class="flex justify-center" style="max-height: 100%; max-width: 100%; height: 100vh; width: 100vw;">
                        <img src="{file_url}" alt="Nội dung hình ảnh" class="max-w-full h-auto rounded-md border-2 border-gray-300 dark:border-gray-600">
                    </div>
                </div>
            """
        elif file_ext in ('.mp4', '.avi', '.mkv', '.webm'):
            content = f"""
                <div class="content-box mb-12 bg-white dark:bg-gray-850 p-6 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                    <h2 class="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Video</h2>
                    <div class="aspect-w-16 aspect-h-9" style="max-height: 100%; max-width: 100%; height: 100vh; width: 100vw;">
                        <video controls class="w-full rounded-md border-2 border-gray-300 dark:border-gray-600">
                            <source src="{file_url}" type="video/mp4">
                            Trình duyệt của bạn không hỗ trợ video.
                        </video>
                    </div>
                </div>
            """
        else:
            content = f"""<div class="content-box mb-12 bg-white dark:bg-gray-850 p-6 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                    <h2 class="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Tài Liệu</h2>
                    <p class="text-gray-700 dark:text-gray-300">Nhấn vào nút bên dưới để tải xuống tài liệu</p>
                </div>"""

        html_content = f"""
<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A3 Chuyên Tin - Tài Liệu | {doc['displayName']}</title>
    <meta name="description" content="{doc['description']}, {', '.join(doc['tags'])}, THPT Chuyên Nguyễn Thị Minh Khai, A3 Chuyên Tin, A3 Sạch Hơn Aba, Chuyên Tin Học, NTMK, THPT, Tài Liệu Học Tập, Giáo Viên, Học Sinh">
    <meta property="og:title" content="{doc['description']}, {', '.join(doc['tags'])}, THPT Chuyên Nguyễn Thị Minh Khai, A3 Chuyên Tin, A3 Sạch Hơn Aba, Chuyên Tin Học, NTMK, THPT, Tài Liệu Học Tập, Giáo Viên, Học Sinh">
    <meta property="og:description" content="{doc['description']}, {', '.join(doc['tags'])}, THPT Chuyên Nguyễn Thị Minh Khai, A3 Chuyên Tin, A3 Sạch Hơn Aba, Chuyên Tin Học, NTMK, THPT, Tài Liệu Học Tập, Giáo Viên, Học Sinh">
    <meta name="author" content="A3 Chuyên Tin">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        dark: {{
                            800: '#1e293b',
                            850: '#1a243b',
                            900: '#0f172a',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        div {{
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }}
        
        .dark {{
            color-scheme: dark;
        }}
        
        .dark .content-box {{
            background-color: #1a243b;
            border-color: #2d3748;
        }}
        
        .dark iframe {{
            background-color: #1e293b;
        }}
    </style>
</head>
<body class="bg-gray-100 dark:bg-gray-900 p-6">
    <div class="max-w-6xl mx-auto">
        <div class="flex justify-end mb-4">
            <button id="dark-mode-toggle" class="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                <svg id="dark-icon" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
                <svg id="light-icon" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
            </button>
        </div>
        
        <h1 class="text-3xl font-bold text-center mb-8 text-blue-600 dark:text-blue-400">{doc['displayName']}</h1>
        
        {content}
        
        <div class="mb-8 text-center">
            <button id="downloadBtn" class="bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-800 text-white font-bold py-2 px-6 rounded-lg shadow-md transition duration-300">
                Tải Xuống Nội Dung
            </button>
        </div>
    </div>
    
    <script>
        function initDarkMode() {{
            const darkModeToggle = document.getElementById('dark-mode-toggle');
            const darkIcon = document.getElementById('dark-icon');
            const lightIcon = document.getElementById('light-icon');
            const isDarkMode = localStorage.getItem('darkMode') === 'true';
            
            if (isDarkMode) {{
                document.documentElement.classList.add('dark');
                darkIcon.classList.add('hidden');
                lightIcon.classList.remove('hidden');
            }} else {{
                document.documentElement.classList.remove('dark');
                darkIcon.classList.remove('hidden');
                lightIcon.classList.add('hidden');
            }}
            
            darkModeToggle.addEventListener('click', () => {{
                const isDark = document.documentElement.classList.toggle('dark');
                localStorage.setItem('darkMode', isDark);
                
                if (isDark) {{
                    darkIcon.classList.add('hidden');
                    lightIcon.classList.remove('hidden');
                }} else {{
                    darkIcon.classList.remove('hidden');
                    lightIcon.classList.add('hidden');
                }}
            }});
        }}

        function initDownloadButton() {{
            document.getElementById('downloadBtn').addEventListener('click', function() {{
                const url = '{file_url}';
                const fileName = url.split('/').pop() || 'download';
                
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                
                alert('Đã bắt đầu tải xuống: ' + fileName);
            }});
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            initDarkMode();
            initDownloadButton();
        }});
    </script>
</body>
</html>
"""
        
        html_filename = f"{os.path.splitext(doc['fileName'])[0]}.html"
        html_path = os.path.join(self.files_dir, html_filename)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def add_document(self):
        if not self.current_file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file đính kèm")
            return
        
        new_id = self.generate_id()
        original_name = os.path.basename(self.current_file_path)
        new_filename = self.generate_random_filename(original_name)
        dest_path = os.path.join(self.files_dir, new_filename)
        
        try:
            if os.path.abspath(self.current_file_path) != os.path.abspath(dest_path):
                shutil.copy(self.current_file_path, dest_path)
        except shutil.SameFileError:
            pass
        
        upload_date = self.inputs["uploadDate"].get_date().strftime("%Y-%m-%d")
        new_doc = {
            "id": new_id,
            "fileName": new_filename,
            "displayName": self.inputs["displayName"].get(),
            "type": self.inputs["type"].get(),
            "description": self.inputs["description"].get(),
            "uploadDate": upload_date,
            "tags": [tag.strip() for tag in self.inputs["tags"].get().split(",") if tag.strip()]
        }
        
        self.documents.append(new_doc)
        self.create_html_for_document(new_doc)
        
        self.update_list()
        self.clear_form()
        self.save_data()
        messagebox.showinfo("Thành công", "Đã thêm tài liệu mới!")

    def update_document(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài liệu để cập nhật")
            return
        
        index = selection[0]
        doc = self.documents[index]
        upload_date = self.inputs["uploadDate"].get_date().strftime("%Y-%m-%d")
        
        old_html_path = os.path.join(self.files_dir, f"{os.path.splitext(doc['fileName'])[0]}.html")
        if os.path.exists(old_html_path):
            os.remove(old_html_path)
        
        doc.update({
            "displayName": self.inputs["displayName"].get(),
            "type": self.inputs["type"].get(),
            "description": self.inputs["description"].get(),
            "uploadDate": upload_date,
            "tags": [tag.strip() for tag in self.inputs["tags"].get().split(",") if tag.strip()]
        })
        
        if self.current_file_path:
            original_name = os.path.basename(self.current_file_path)
            file_ext = os.path.splitext(original_name)[1]
            
            new_filename = os.path.splitext(doc["fileName"])[0] + file_ext
            dest_path = os.path.join(self.files_dir, new_filename)
            
            old_file = os.path.join(self.files_dir, doc["fileName"])
            if os.path.exists(old_file) and old_file != dest_path:
                os.remove(old_file)
            
            shutil.copy2(self.current_file_path, dest_path)
            
            doc["fileName"] = new_filename
        
        # Tạo HTML mới
        self.create_html_for_document(doc)
        
        self.update_list()
        self.clear_form()
        self.save_data()
        messagebox.showinfo("Thành công", "Đã cập nhật tài liệu!")

    def delete_document(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài liệu để xóa")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tài liệu này?"):
            index = selection[0]
            doc = self.documents.pop(index)
            
            file_path = os.path.join(self.files_dir, doc["fileName"])
            if os.path.exists(file_path):
                os.remove(file_path)
            
            html_path = os.path.join(self.files_dir, f"{os.path.splitext(doc['fileName'])[0]}.html")
            if os.path.exists(html_path):
                os.remove(html_path)
            
            self.update_list()
            self.clear_form()
            self.save_data()
            messagebox.showinfo("Thành công", "Đã xóa tài liệu!")

    def clear_form(self):
        for key, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, tk.END)
            elif isinstance(widget, DateEntry):
                widget.set_date(datetime.today())
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(text="Chưa có file")
        self.current_file_path = None

if __name__ == "__main__":
    app = DocumentManager()
    app.mainloop()