@echo off
chcp 65001 > nul
echo ======================================================
echo   DANG DONG BO CODE LEN GITHUB
echo ======================================================

git status -s
echo.
set /p commit_msg="Nhap ghi chu commit (Nhan Enter de dung mac dinh): "
if "%commit_msg%"=="" set commit_msg=update ung dung quan ly hoa hong 4%%

git add .
git commit -m "%commit_msg%"
git push origin main

echo.
echo ======================================================
echo   DA DAY CODE LEN GITHUB THANH CONG!
echo   Tren PythonAnywhere ban chi can go: ~/capnhat.sh
echo ======================================================
pause
