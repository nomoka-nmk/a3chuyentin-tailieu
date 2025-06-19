import os
import json
import random
import string
import shutil
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QListWidget, QLineEdit, QLabel, QPushButton, QFileDialog, 
                            QMessageBox, QFormLayout, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor

class DocumentManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A3 Chuyên Tin - Tài Liệu")
        self.setGeometry(100, 100, 1100, 750)
        self.setWindowIcon(QIcon('favicon.ico'))
        self.documents = []
        self.current_file_path = None
        self.json_path = os.path.join("assets", "documents", "documents.json")
        self.files_dir = os.path.join("assets", "documents", "files")
        os.makedirs(self.files_dir, exist_ok=True)
        self.setup_ui()
        self.load_data()
    def setup_ui(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(50, 50, 50))
        self.setPalette(palette)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        list_frame = QWidget()
        list_frame.setMinimumWidth(300)
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("DANH SÁCH TÀI LIỆU")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333;
            padding: 10px;
            border-bottom: 2px solid #4285F4;
        """)
        list_layout.addWidget(title)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #f0f7ff;
            }
            QListWidget::item:selected {
                background-color: #4285F4;
                color: white;
                border-radius: 4px;
            }
        """)
        self.list_widget.itemSelectionChanged.connect(self.on_select)
        list_layout.addWidget(self.list_widget)
        main_layout.addWidget(list_frame)
        info_frame = QWidget()
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(15)
        info_title = QLabel("THÔNG TIN TÀI LIỆU")
        info_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333;
            padding: 10px;
            border-bottom: 2px solid #4285F4;
        """)
        info_layout.addWidget(info_title)
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(15)
        form_layout.setContentsMargins(10, 10, 10, 10)
        self.inputs = {
            "id": QLineEdit(),
            "displayName": QLineEdit(),
            "type": QLineEdit(),
            "description": QLineEdit(),
            "tags": QLineEdit(),
            "uploadDate": QDateEdit(),
            "fileName": QLabel("Chưa có file")
        }
        input_style = """
            QLineEdit, QDateEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 1px solid #4285F4;
            }
        """
        for widget in self.inputs.values():
            if isinstance(widget, (QLineEdit, QDateEdit)):
                widget.setStyleSheet(input_style)
        self.inputs["uploadDate"].setDate(QDate.currentDate())
        self.inputs["uploadDate"].setCalendarPopup(True)
        self.inputs["uploadDate"].setDisplayFormat("dd/MM/yyyy")
        self.inputs["uploadDate"].setStyleSheet(input_style)
        fields = [
            ("Mã tài liệu:", self.inputs["id"]),
            ("Tên hiển thị:", self.inputs["displayName"]),
            ("Loại file:", self.inputs["type"]),
            ("Mô tả:", self.inputs["description"]),
            ("Tags (cách nhau bằng dấu phẩy):", self.inputs["tags"]),
            ("Ngày upload:", self.inputs["uploadDate"]),
            ("File đính kèm:", self.inputs["fileName"])
        ]
        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            form_layout.addRow(label, widget)
        self.btn_file = QPushButton("📁 CHỌN FILE")
        self.btn_file.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
        """)
        self.btn_file.clicked.connect(self.select_file)
        form_layout.addRow(self.btn_file)
        info_layout.addWidget(form_widget)
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(15)
        buttons = [
            ("➕ THÊM MỚI", self.add_document, "#34A853"),
            ("✏️ CẬP NHẬT", self.update_document, "#4285F4"),
            ("🗑️ XÓA", self.delete_document, "#EA4335"),
            ("💾 LƯU DỮ LIỆU", self.save_data, "#FBBC05")
        ]
        for text, handler, color in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 6px;
                    padding: 12px 20px;
                    font-size: 14px;
                    border: none;
                    min-width: 120px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn_layout.addWidget(btn)
        info_layout.addWidget(btn_frame)
        main_layout.addWidget(info_frame)
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
                    self.documents.sort(key=lambda x: int(x["id"][3:]))
            else:
                self.documents = []
            self.update_list()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc file JSON:\n{str(e)}")
            self.documents = []
    def save_data(self):
        try:
            self.documents.sort(key=lambda x: int(x["id"][3:]))
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Thành công", "Đã lưu dữ liệu thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu file:\n{str(e)}")
    def update_list(self):
        self.list_widget.clear()
        for doc in self.documents:
            self.list_widget.addItem(f"{doc['id']} - {doc['displayName']}")
    def on_select(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        index = self.list_widget.row(selected_items[0])
        doc = self.documents[index]
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                widget.setText(str(doc.get(key, "")))
            elif isinstance(widget, QDateEdit):
                date_str = doc.get("uploadDate", "")
                if date_str:
                    date = QDate.fromString(date_str, "yyyy-MM-dd")
                    widget.setDate(date)
            elif key == "fileName":
                widget.setText(doc.get("fileName", "Chưa có file"))
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Chọn file tài liệu", 
            "", 
            "All Files (*);;PDF Files (*.pdf);;Word Documents (*.docx);;Excel Files (*.xlsx)"
        )
        if file_path:
            self.current_file_path = file_path
            self.inputs["fileName"].setText(os.path.basename(file_path))
    def generate_id(self):
        if not self.documents:
            return "doc001"
        max_id = max(int(doc["id"][3:]) for doc in self.documents)
        return f"doc{max_id + 1:03d}"
    def generate_random_filename(self, original_name):
        ext = os.path.splitext(original_name)[1]
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_str}{ext}"
    def add_document(self):
        if not self.current_file_path:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file đính kèm")
            return
        new_id = self.generate_id()
        original_name = os.path.basename(self.current_file_path)
        new_filename = self.generate_random_filename(original_name)
        dest_path = os.path.join(self.files_dir, new_filename)
        shutil.copy(self.current_file_path, dest_path)
        date = self.inputs["uploadDate"].date()
        upload_date = date.toString("yyyy-MM-dd")
        new_doc = {
            "id": new_id,
            "fileName": new_filename,
            "displayName": self.inputs["displayName"].text(),
            "type": self.inputs["type"].text(),
            "description": self.inputs["description"].text(),
            "uploadDate": upload_date,
            "tags": [tag.strip() for tag in self.inputs["tags"].text().split(",") if tag.strip()]
        }
        self.documents.append(new_doc)
        self.update_list()
        self.clear_form()
        QMessageBox.information(self, "Thành công", "Đã thêm tài liệu mới!")
    def update_document(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn tài liệu để cập nhật")
            return
        index = self.list_widget.row(selected_items[0])
        doc = self.documents[index]
        date = self.inputs["uploadDate"].date()
        upload_date = date.toString("yyyy-MM-dd")
        doc.update({
            "displayName": self.inputs["displayName"].text(),
            "type": self.inputs["type"].text(),
            "description": self.inputs["description"].text(),
            "uploadDate": upload_date,
            "tags": [tag.strip() for tag in self.inputs["tags"].text().split(",") if tag.strip()]
        })
        if self.current_file_path:
            original_name = os.path.basename(self.current_file_path)
            new_filename = self.generate_random_filename(original_name)
            dest_path = os.path.join(self.files_dir, new_filename)
            shutil.copy(self.current_file_path, dest_path)
            old_file = os.path.join(self.files_dir, doc["fileName"])
            if os.path.exists(old_file):
                os.remove(old_file)
            doc["fileName"] = new_filename
        self.update_list()
        QMessageBox.information(self, "Thành công", "Đã cập nhật tài liệu!")
    def delete_document(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn tài liệu để xóa")
            return
        reply = QMessageBox.question(
            self, "Xác nhận", 
            "Bạn có chắc chắn muốn xóa tài liệu này?", 
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        index = self.list_widget.row(selected_items[0])
        doc = self.documents.pop(index)
        file_path = os.path.join(self.files_dir, doc["fileName"])
        if os.path.exists(file_path):
            os.remove(file_path)
        self.update_list()
        self.clear_form()
        QMessageBox.information(self, "Thành công", "Đã xóa tài liệu!")
    def clear_form(self):
        for widget in self.inputs.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
        self.inputs["fileName"].setText("Chưa có file")
        self.current_file_path = None
if __name__ == "__main__":
    app = QApplication([])
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = DocumentManager()
    window.show()
    app.exec_()