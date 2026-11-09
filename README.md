# Ứng Dụng Quản Lý Doanh Thu & Hoa Hồng Cá Nhân 4%

Ứng dụng web được xây dựng chuyên biệt để theo dõi doanh thu và tự động tính hoa hồng 4% theo chu kỳ chốt sổ lệch (từ ngày 09 tháng trước đến ngày 08 tháng này), hỗ trợ xuất bảng kê ảnh sắc nét (scale 2x) gửi trực tiếp qua Zalo. Tối ưu triển khai trên máy chủ đám mây **PythonAnywhere**.

---

## 🚀 Tính Năng Nổi Bật

1. **Bảo Mật Truy Cập Bằng Mã PIN 4 Số**:
   - Mặc định: `1995` (có thể đổi qua biến môi trường `APP_PIN`).
   - Bàn phím số cảm ứng phong cách Dark Mode kính mờ hiện đại, hỗ trợ cả bàn phím vật lý máy tính và bàn phím cảm ứng di động.
   - Quản lý phiên làm việc an toàn với `Flask Session`.

2. **Chu Kỳ Chốt Sổ Lệch (Ngày 9 tháng trước -> 23:59 Ngày 8 tháng này)**:
   - Tự động nhận diện kỳ chốt sổ dựa trên ngày hiện tại.
   - Bộ điều hướng nhanh: Xem kỳ trước, kỳ sau hoặc trở về kỳ hiện tại chỉ với 1 cú click.
   - Thống kê tự động: Tổng doanh thu, Tổng hoa hồng 4%, Số lượng hóa đơn.

3. **Quản Lý Hóa Đơn & Món Hàng Động (Dynamic Rows)**:
   - 1 Hóa đơn chứa nhiều món / dịch vụ.
   - Tự do thêm/xóa dòng món, xem trước thành tiền từng món và tổng hoa hồng đơn tức thì.
   - Hỗ trợ sửa đơn (load lại toàn bộ thông tin và danh sách món để cập nhật).
   - Xóa đơn an toàn (tự động xóa cascade các món con trong SQLite).

4. **Xuất Ảnh Bảng Kê Gửi Zalo Sắc Nét**:
   - Sử dụng thư viện `html2canvas` với độ phân giải cao `scale: 2`.
   - Tự động ẩn các nút thao tác (Sửa/Xóa) khi xuất ảnh.
   - Tự động tải file ảnh PNG về máy để chia sẻ nhanh chóng qua Zalo.

---

## 🛠️ Cấu Trúc Dự Án

```
4%/
│── app.py                    # Backend Flask, Router, API & Logic SQLite, Chu kỳ ngày 8
│── wsgi_pythonanywhere.py     # File cấu hình WSGI mẫu cho PythonAnywhere
│── requirements.txt          # Danh sách thư viện: Flask, python-dateutil
│── templates/
│   ├── login.html            # Giao diện khóa mã PIN bảo mật
│   └── index.html            # Giao diện Dashboard, quản lý đơn & script html2canvas
└── README.md                 # Hướng dẫn chi tiết sử dụng và triển khai
```

---

## 💻 Hướng Dẫn Chạy Cục Bộ (Local Development)

### 1. Cài đặt môi trường ảo và thư viện
```bash
python -m venv venv
# Trên Windows:
venv\Scripts\activate
# Trên Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Khởi chạy ứng dụng
```bash
python app.py
```
Mở trình duyệt truy cập: `http://localhost:5000`
- Mã PIN mặc định: `1995`

---

## ☁️ Hướng Dẫn Triển Khai Lên PythonAnywhere

### Bước 1: Tạo tài khoản và tải code lên
1. Đăng ký tài khoản miễn phí tại [pythonanywhere.com](https://www.pythonanywhere.com).
2. Mở tab **Consoles** -> Chọn **Bash console**.
3. Clone hoặc tạo thư mục chứa mã nguồn:
   ```bash
   mkdir -p ~/commission4
   cd ~/commission4
   ```
4. Tải các file dự án lên thư mục này (hoặc dùng git clone).

### Bước 2: Cài đặt thư viện
Trong cửa sổ Bash console của PythonAnywhere:
```bash
pip install --user -r requirements.txt
```

### Bước 3: Cấu hình Web App trên PythonAnywhere
1. Vào tab **Web** trên thanh điều hướng của PythonAnywhere.
2. Nhấp **Add a new web app** -> Chọn **Manual configuration** -> Chọn phiên bản **Python 3.10** (hoặc Python mới nhất).
3. Tại phần **Code**:
   - **Source code**: nhập `/home/<your-username>/commission4`
   - **Working directory**: nhập `/home/<your-username>/commission4`
4. Tại mục **WSGI configuration file**:
   - Nhấp vào link file (ví dụ: `/var/www/<your-username>_pythonanywhere_com_wsgi.py`).
   - Xóa toàn bộ nội dung mặc định và sao chép nội dung từ file `wsgi_pythonanywhere.py` vào.
   - Nhớ thay `<your-username>` bằng tên tài khoản của bạn.
   - Lưu lại (nút **Save** ở góc trên bên phải).
5. Quay lại tab **Web** và nhấn nút màu xanh lá **Reload <your-username>.pythonanywhere.com**.

### Bước 4: Truy cập và sử dụng
- Truy cập vào địa chỉ: `https://<your-username>.pythonanywhere.com`
- Nhập mã PIN `1995` để bắt đầu quản lý đơn hàng và tính hoa hồng 4%.
