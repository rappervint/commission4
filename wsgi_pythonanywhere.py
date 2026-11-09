# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CẤU HÌNH WSGI MẪU CHO PYTHONANYWHERE (WSGI CONFIGURATION FILE)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Hướng dẫn:
# 1. Tại trang Dashboard PythonAnywhere -> Chọn tab "Web".
# 2. Nhấp vào liên kết tại mục "WSGI configuration file"
#    (thường có dạng: /var/www/<your-username>_pythonanywhere_com_wsgi.py).
# 3. Sao chép toàn bộ nội dung file này dán vào và lưu lại.
# 4. Thay thế '<your-username>' bằng tên tài khoản PythonAnywhere thực tế của bạn.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import sys
import os

# 1. Đường dẫn thư mục chứa mã nguồn ứng dụng trên PythonAnywhere
# Ví dụ: nếu bạn clone/upload vào /home/yourusername/commission4/
path = '/home/<your-username>/commission4'
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Thiết lập các biến môi trường bảo mật (tùy chọn nhưng khuyến nghị)
os.environ['APP_PIN'] = '1995'  # Mã PIN đăng nhập (mặc định 1995, bạn có thể đổi)
os.environ['SECRET_KEY'] = 'thay_the_bang_chuoi_bao_mat_ngau_nhien_tai_day_1995'

# 3. Kích hoạt Virtualenv (nếu bạn sử dụng virtualenv trên PythonAnywhere)
# activate_this = '/home/<your-username>/.virtualenvs/myenv/bin/activate_this.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))

# 4. Import ứng dụng Flask (PythonAnywhere yêu cầu biến có tên là 'application')
from app import app as application
