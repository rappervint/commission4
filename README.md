# Ứng Dụng Quản Lý Doanh Thu & Hoa Hồng Cá Nhân 4%

Ứng dụng web được xây dựng chuyên biệt để theo dõi doanh thu và tự động tính hoa hồng 4% theo chu kỳ chốt sổ lệch (từ ngày 09 tháng trước đến ngày 08 tháng này), hỗ trợ xuất bảng kê ảnh sắc nét (scale 2x) gửi trực tiếp qua Zalo. Tối ưu triển khai trên máy chủ đám mây **PythonAnywhere**.

---

## ⚡ Cập Nhật Tự Động Trên PythonAnywhere Với `~/capnhat.sh`

Dự án đã tích hợp sẵn script [`capnhat.sh`](file:///e:/4%/capnhat.sh) giúp tự động:
1. Kéo mã nguồn mới nhất từ Git (`git pull origin main`).
2. Cài đặt các gói thư viện mới nếu có (`pip install --user -r requirements.txt`).
3. Tự động tìm và `touch` file WSGI để **Reload Web App ngay tức khắc** mà không cần mở trình duyệt vào tab Web bấm Reload thủ công!
4. Bảo vệ an toàn dữ liệu: file cơ sở dữ liệu `revenue.db` đã được đưa vào `.gitignore`, đảm bảo khi update code không bao giờ bị mất hoặc ghi đè dữ liệu hóa đơn thật.

### Thiết lập 1 lần duy nhất trên PythonAnywhere:
Mở cửa sổ **Bash console** trên PythonAnywhere và chạy:
```bash
# 1. Tạo symlink script ra thư mục home
ln -s ~/commission4/capnhat.sh ~/capnhat.sh

# 2. Cấp quyền thực thi
chmod +x ~/capnhat.sh ~/commission4/capnhat.sh
```

### Các lần cập nhật tiếp theo:
Mỗi khi bạn đẩy code mới lên GitHub, trên PythonAnywhere bạn chỉ cần gõ đúng 1 dòng lệnh:
```bash
~/capnhat.sh
```
Hệ thống sẽ tự động cập nhật và khởi động lại web app trong 3 giây!

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

4. **Xuất Ảnh Bảng Kê Gửi Zalo Sắc Nét & Xuất CSV (Excel)**:
   - Sử dụng thư viện `html2canvas` với độ phân giải cao `scale: 2`.
   - Tự động ẩn các nút thao tác (Sửa/Xóa) khi xuất ảnh.
   - Tự động tải file ảnh PNG về máy để chia sẻ nhanh chóng qua Zalo.
   - Hỗ trợ xuất file CSV chuẩn mã hóa UTF-8 BOM hiển thị tiếng Việt hoàn hảo trên Excel.

---

## 🛠️ Cấu Trúc Dự Án

```
4%/
│── app.py                    # Backend Flask, Router, API & Logic SQLite, Chu kỳ ngày 8
│── capnhat.sh                # Script 1-click cập nhật và reload app trên PythonAnywhere
│── wsgi_pythonanywhere.py     # File cấu hình WSGI mẫu cho PythonAnywhere
│── requirements.txt          # Danh sách thư viện: Flask, python-dateutil
│── seed_sample_data.py       # Script nạp dữ liệu kiểm thử nhanh
│── .gitignore                # Chặn commit database tránh ghi đè dữ liệu thật
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

### 2. Nạp dữ liệu mẫu kiểm thử (Tùy chọn)
```bash
python seed_sample_data.py
```

### 3. Khởi chạy ứng dụng
```bash
python app.py
```
Mở trình duyệt truy cập: `http://localhost:5000`
- Mã PIN mặc định: `1995`

---

## ☁️ Hướng Dẫn Triển Khai Lên PythonAnywhere Lần Đầu

### Bước 1: Đưa code lên GitHub
1. Tạo 1 repository mới trên GitHub (ví dụ: `commission4`).
2. Tại máy tính của bạn, liên kết và đẩy code lên:
   ```bash
   git remote add origin https://github.com/<your-username>/commission4.git
   git push -u origin main
   ```

### Bước 2: Kéo code về PythonAnywhere
1. Đăng nhập [pythonanywhere.com](https://www.pythonanywhere.com) -> Mở tab **Consoles** -> Chọn **Bash**.
2. Clone repository vào thư mục `~/commission4`:
   ```bash
   git clone https://github.com/<your-username>/commission4.git ~/commission4
   cd ~/commission4
   pip install --user -r requirements.txt
   ```
3. Tạo phím tắt lệnh `~/capnhat.sh`:
   ```bash
   ln -s ~/commission4/capnhat.sh ~/capnhat.sh
   chmod +x ~/capnhat.sh ~/commission4/capnhat.sh
   ```

### Bước 3: Cấu hình Web App trên PythonAnywhere
1. Vào tab **Web** -> **Add a new web app** -> **Manual configuration** -> **Python 3.10** (hoặc mới hơn).
2. Tại mục **Code**:
   - **Source code**: `/home/<username>/commission4`
   - **Working directory**: `/home/<username>/commission4`
3. Tại mục **WSGI configuration file**:
   - Nhấp vào file `/var/www/<username>_pythonanywhere_com_wsgi.py`.
   - Dán nội dung từ file [`wsgi_pythonanywhere.py`](file:///e:/4%/wsgi_pythonanywhere.py) vào (nhớ thay `<your-username>` bằng username thực tế của bạn).
   - Nhấn **Save**.
4. Bấm nút màu xanh **Reload <username>.pythonanywhere.com**.
