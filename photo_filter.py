import os
import sys
from tkinter import Tk, Label, Button, Entry, filedialog, Text, Scrollbar, END, N, S, E, W
from tkinter import ttk
import datetime

class PhotoFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("照片筛选工具 - Invert Selection")
        self.root.geometry("800x600")

        # 支持的照片扩展名
        self.supported_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.gif', '.bmp', '.tiff')

        # 保存选择的文件夹路径
        self.folder_a = ""
        self.folder_b = ""

        # 日志文本
        self.log_text = ""

        self.setup_ui()

    def setup_ui(self):
        # 风格化组件
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        style.configure("TLabel", padding=4, background="#f0f0f0")

        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(N, S, E, W))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

        # 文件夹A选择
        Label(main_frame, text="基准文件夹 (A):").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.entry_a = Entry(main_frame, width=50)
        self.entry_a.grid(row=0, column=1, sticky=(E, W), padx=5, pady=5)
        Button(main_frame, text="浏览", command=self.select_folder_a).grid(row=0, column=2, padx=5, pady=5)

        # 文件夹B选择
        Label(main_frame, text="待筛选文件夹 (B):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.entry_b = Entry(main_frame, width=50)
        self.entry_b.grid(row=1, column=1, sticky=(E, W), padx=5, pady=5)
        Button(main_frame, text="浏览", command=self.select_folder_b).grid(row=1, column=2, padx=5, pady=5)

        # 运行按钮
        self.run_button = Button(main_frame, text="开始筛选", command=self.run_filter, bg="#4CAF50", fg="white")
        self.run_button.grid(row=2, column=1, pady=15)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=1, pady=10)

        # 状态标签
        self.status_label = Label(main_frame, text="准备就绪", fg="green")
        self.status_label.grid(row=4, column=1, pady=5)

        # 日志区域
        Label(main_frame, text="操作日志:").grid(row=5, column=0, sticky=W, padx=5, pady=5)

        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(N, S, E, W), padx=5, pady=5)

        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = Text(log_frame, height=15, width=70, wrap="word")
        scrollbar = Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(N, S, E, W))
        scrollbar.grid(row=0, column=1, sticky=(N, S))

        # 清空日志按钮
        Button(main_frame, text="清空日志", command=self.clear_log).grid(row=7, column=2, pady=10)

        # 导出日志按钮
        Button(main_frame, text="导出日志", command=self.export_log).grid(row=7, column=1, pady=10)

    def select_folder_a(self):
        folder = filedialog.askdirectory(title="选择基准文件夹 (A)")
        if folder:
            self.folder_a = folder
            self.entry_a.delete(0, END)
            self.entry_a.insert(0, folder)
            self.log(f"已选择基准文件夹: {folder}")

    def select_folder_b(self):
        folder = filedialog.askdirectory(title="选择待筛选文件夹 (B)")
        if folder:
            self.folder_b = folder
            self.entry_b.delete(0, END)
            self.entry_b.insert(0, folder)
            self.log(f"已选择待筛选文件夹: {folder}")

    def get_files_without_extension(self, folder_path):
        """获取文件夹中所有支持的照片文件（不含扩展名）"""
        files = set()
        if not os.path.exists(folder_path):
            return files

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                name, ext = os.path.splitext(filename)
                if ext.lower() in self.supported_extensions:
                    files.add(name)
        return files

    def log(self, message):
        """添加日志消息"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(END, log_message)
        self.log_text.see(END)
        self.root.update_idletasks()

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, END)
        self.log("日志已清空")

    def export_log(self):
        """导出日志到文件"""
        if not self.log_text.get(1.0, END).strip():
            self.log("没有日志可导出")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="导出日志文件"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.log_text.get(1.0, END))
                self.log(f"日志已导出到: {file_path}")
            except Exception as e:
                self.log(f"导出日志失败: {str(e)}")

    def run_filter(self):
        """执行筛选操作"""
        # 验证文件夹路径
        if not self.folder_a:
            self.log("请先选择基准文件夹 (A)")
            return
        if not self.folder_b:
            self.log("请先选择待筛选文件夹 (B)")
            return
        if self.folder_a == self.folder_b:
            self.log("基准文件夹和待筛选文件夹不能相同")
            return

        # 禁用运行按钮
        self.run_button.config(state="disabled")
        self.status_label.config(text="正在分析文件...", fg="orange")
        self.progress["value"] = 0
        self.root.update_idletasks()

        try:
            # 获取文件夹A中的所有文件（不含扩展名）
            files_a = self.get_files_without_extension(self.folder_a)
            self.log(f"基准文件夹 (A) 中找到 {len(files_a)} 个支持的照片文件")

            # 获取文件夹B中的所有文件（含完整路径和扩展名）
            files_b = []
            for filename in os.listdir(self.folder_b):
                file_path = os.path.join(self.folder_b, filename)
                if os.path.isfile(file_path):
                    name, ext = os.path.splitext(filename)
                    if ext.lower() in self.supported_extensions:
                        files_b.append((name, ext, file_path))

            self.log(f"待筛选文件夹 (B) 中找到 {len(files_b)} 个支持的照片文件")

            # 计算进度条步长
            step = 100 / len(files_b) if files_b else 100

            # 执行筛选
            deleted_count = 0
            kept_count = 0
            deleted_files = []
            kept_files = []

            for i, (name, ext, file_path) in enumerate(files_b):
                self.progress["value"] = i * step
                self.root.update_idletasks()

                if name in files_a:
                    # 文件在A中存在，删除B中的文件
                    try:
                        os.unlink(file_path)  # 使用unlink而不是remove，更通用
                        deleted_count += 1
                        deleted_files.append(f"{name}{ext}")
                        self.log(f"已删除: {name}{ext}")
                    except Exception as e:
                        self.log(f"删除失败: {name}{ext} - {str(e)}")
                else:
                    # 文件在A中不存在，保留
                    kept_count += 1
                    kept_files.append(f"{name}{ext}")
                    self.log(f"保留文件: {name}{ext}")

            # 更新进度条到100%
            self.progress["value"] = 100
            self.root.update_idletasks()

            # 显示结果统计
            self.log("\n" + "="*50)
            self.log("筛选完成！")
            self.log(f"基准文件夹 (A) 文件总数: {len(files_a)}")
            self.log(f"待筛选文件夹 (B) 原文件总数: {len(files_b)}")
            self.log(f"已删除重复文件数量: {deleted_count}")
            self.log(f"保留独有文件数量: {kept_count}")
            self.log("="*50)

            # 显示结果列表（可选）
            if deleted_files:
                self.log(f"\n删除的文件列表 ({deleted_count}个):")
                for file in deleted_files:
                    self.log(f"  - {file}")

            if kept_files:
                self.log(f"\n保留的文件列表 ({kept_count}个):")
                for file in kept_files:
                    self.log(f"  - {file}")

            self.status_label.config(text=f"筛选完成！删除{deleted_count}个，保留{kept_count}个", fg="green")

        except Exception as e:
            self.log(f"筛选过程中发生错误: {str(e)}")
            self.status_label.config(text="筛选失败", fg="red")

        finally:
            # 启用运行按钮
            self.run_button.config(state="normal")

def main():
    # 创建Tkinter根窗口
    root = Tk()

    # 设置窗口图标（可选，这里使用默认图标）
    try:
        if sys.platform == "win32":
            root.iconbitmap(default="")
    except:
        pass

    # 创建应用程序实例
    app = PhotoFilterApp(root)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
