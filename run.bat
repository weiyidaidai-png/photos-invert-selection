@echo off
title 照片筛选工具

echo ========================================
echo        照片筛选工具 - Invert Selection
echo ========================================
echo.
echo 功能：将文件夹B中与文件夹A重复的照片删除
echo 支持格式：JPG/PNG/HEIC/GIF/BMP/TIFF
echo.
echo 正在启动工具，请稍候...
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python环境！
    echo 请先安装Python 3.x版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 运行Python脚本
python photo_filter.py

echo.
echo 工具已退出
pause
exit /b 0
