"""
Script tạo dữ liệu mẫu (Sample Data) kiểm thử ứng dụng Quản lý Doanh thu & Hoa hồng 4%.
Chạy script này bằng lệnh:
    python seed_sample_data.py
"""

import sqlite3
import os
from datetime import date
from dateutil.relativedelta import relativedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'revenue.db')


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    # Ensure tables exist
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_info TEXT NOT NULL,
                order_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                price REAL NOT NULL DEFAULT 0,
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            );
        """)

    cursor = conn.cursor()

    # Determine dates around today
    today = date.today()
    sample_orders = [
        {
            'customer': '51H-899.23 (Anh Tuấn)',
            'date': today.strftime('%Y-%m-%d'),
            'items': [
                ('Bảo dưỡng cấp 4 vạn km', 1850000, 1),
                ('Thay 4 bugi Iridium Denso', 320000, 4),
                ('Vệ sinh họng nạp buồng đốt', 650000, 1)
            ]
        },
        {
            'customer': '30F-456.78 (Chị Ngọc)',
            'date': (today - relativedelta(days=2)).strftime('%Y-%m-%d'),
            'items': [
                ('Phủ Ceramic 9H cao cấp', 6500000, 1),
                ('Dán phim cách nhiệt 3M Crystalline', 9200000, 1)
            ]
        },
        {
            'customer': '60A-789.12 (Anh Hoàng)',
            'date': (today - relativedelta(days=4)).strftime('%Y-%m-%d'),
            'items': [
                ('Thay nhớt động cơ Motul 5W30', 280000, 4),
                ('Lọc nhớt chính hãng', 180000, 1),
                ('Cân chỉnh thước lái góc đặt bánh xe', 450000, 1)
            ]
        },
        {
            'customer': '51K-334.56 (Anh Khánh)',
            'date': (today - relativedelta(days=7)).strftime('%Y-%m-%d'),
            'items': [
                ('Độ đèn Bi-Laser Aozoom Thor', 8500000, 1),
                ('Cảm biến áp suất lốp Steelmate', 1950000, 1)
            ]
        }
    ]

    print("--- ĐANG TẠO DỮ LIỆU MẪU KIỂM THỬ ---")
    with conn:
        for ord_data in sample_orders:
            cursor.execute("""
                INSERT INTO orders (customer_info, order_date)
                VALUES (?, ?)
            """, (ord_data['customer'], ord_data['date']))
            order_id = cursor.lastrowid

            total_revenue = 0
            for name, price, qty in ord_data['items']:
                cursor.execute("""
                    INSERT INTO order_items (order_id, item_name, price, quantity)
                    VALUES (?, ?, ?, ?)
                """, (order_id, name, price, qty))
                total_revenue += (price * qty)

            comm = round(total_revenue * 0.04)
            print(f"-> Tạo đơn #{order_id}: {ord_data['customer']} ({ord_data['date']}) | Doanh thu: {total_revenue:,} đ | Hoa hồng 4%: {comm:,} đ")

    conn.close()
    print("------------------------------------------")
    print("HOÀN TẤT! Đã nạp thành công 4 đơn hàng mẫu.")
    print("Bạn có thể khởi động app (python app.py) để xem dữ liệu ngay.")


if __name__ == '__main__':
    seed()
