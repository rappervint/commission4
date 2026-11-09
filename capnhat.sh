#!/bin/bash
# ==============================================================================
# SCRIPT CẬP NHẬT TỰ ĐỘNG CHO PYTHONANYWHERE
# Chạy lệnh: ~/capnhat.sh
# ==============================================================================

echo "=========================================================="
echo "  [1/3] ĐANG KIỂM TRA & KÉO MÃ NGUỒN MỚI TỪ GIT..."
echo "=========================================================="

# Tìm thư mục chứa dự án trên PythonAnywhere
PROJECT_DIR=""
for dir in ~/commission4 ~/4percent ~/4% ~/commission; do
    if [ -d "$dir/.git" ]; then
        PROJECT_DIR="$dir"
        break
    fi
done

# Nếu không tìm thấy các tên mặc định, tìm thư mục hiện tại hoặc bất kỳ repo nào có app.py
if [ -z "$PROJECT_DIR" ]; then
    if [ -f "./app.py" ] && [ -d "./.git" ]; then
        PROJECT_DIR="$(pwd)"
    else
        echo "❌ Lỗi: Chưa tìm thấy thư mục dự án Git trên PythonAnywhere!"
        echo "Vui lòng đặt tên thư mục dự án là: ~/commission4"
        exit 1
    fi
fi

cd "$PROJECT_DIR" || exit 1
echo "-> Thư mục dự án: $PROJECT_DIR"

# Kéo code mới nhất từ Git (hỗ trợ cả nhánh main và master)
git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || git pull

echo ""
echo "=========================================================="
echo "  [2/3] CẬP NHẬT CÁC THƯ VIỆN PYTHON (NẾU CÓ)..."
echo "=========================================================="
pip install --user -r requirements.txt --quiet

echo ""
echo "=========================================================="
echo "  [3/3] TỰ ĐỘNG RELOAD WEB APP TRÊN PYTHONANYWHERE..."
echo "=========================================================="

# Tìm file WSGI của tài khoản trên PythonAnywhere và touch để reload app tức thì
WSGI_FILE=$(ls /var/www/*_wsgi.py 2>/dev/null | head -n 1)

if [ -n "$WSGI_FILE" ]; then
    touch "$WSGI_FILE"
    echo "✅ Đã tự động Reload Web App thành công!"
    echo "-> File WSGI đã cập nhật: $WSGI_FILE"
else
    echo "⚠️  Không tìm thấy file WSGI trong /var/www/."
    echo "-> Vui lòng vào tab Web trên pythonanywhere.com và bấm nút xanh 'Reload'."
fi

echo ""
echo "=========================================================="
echo "  🎉 CẬP NHẬT HOÀN TẤT! HỆ THỐNG ĐÃ SẴN SÀNG."
echo "=========================================================="
