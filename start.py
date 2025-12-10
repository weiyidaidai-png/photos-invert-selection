#!/usr/bin/env python3
"""
照片筛选工具启动脚本
"""

import os
import sys

def main():
    # 确保在正确的工作目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("========================================")
    print("       照片筛选工具 - Invert Selection")
    print("========================================")
    print()
    print("功能：将文件夹B中与文件夹A重复的照片删除")
    print("支持格式：JPG/PNG/HEIC/GIF/BMP/TIFF")
    print()
    print("正在启动工具，请稍候...")
    print()

    try:
        # 导入并运行主应用程序
        import photo_filter
        photo_filter.main()
    except ImportError as e:
        print(f"错误：无法导入主模块 - {e}")
        print("请检查 photo_filter.py 文件是否存在且完整")
    except Exception as e:
        print(f"错误：启动应用程序失败 - {e}")
        import traceback
        traceback.print_exc()

    print()
    print("工具已退出")
    input("按回车键关闭窗口...")

if __name__ == "__main__":
    main()
