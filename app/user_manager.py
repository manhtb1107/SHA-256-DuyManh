import json
import os
import hashlib
import random
import logging

# --- KHAI BÁO BIẾN TOÀN CỤC ---
USERS_DB_FILE = "users_database.json"
users = {}

def load_users():
    """Tải dữ liệu người dùng từ file JSON khi server khởi động."""
    global users
    if os.path.exists(USERS_DB_FILE):
        try:
            # Mở file với encoding utf-8 để hỗ trợ tên người dùng tiếng Việt
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            logging.info(f"Đã tải {len(users)} người dùng từ {USERS_DB_FILE}")
        except json.JSONDecodeError:
            logging.error(f"Lỗi đọc file {USERS_DB_FILE}. Bắt đầu với database trống.")
            users = {}
    else:
        logging.info("Không tìm thấy database. Sẽ tạo file mới khi có đăng ký.")

def save_users():
    """Lưu dữ liệu người dùng hiện tại ra file JSON."""
    # Ghi file với encoding utf-8
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    logging.info(f"Đã lưu dữ liệu người dùng vào {USERS_DB_FILE}")

def hash_password(password):
    """Mã hóa mật khẩu bằng thuật toán SHA-256 cho mục đích bảo mật."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_avatar_color():
    """Tạo một mã màu hex ngẫu nhiên để làm màu nền cho avatar."""
    return f"#{random.randint(0, 0xFFFFFF):06x}"
