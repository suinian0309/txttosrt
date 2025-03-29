import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from converter import convert_file, is_time_stamp
import os
import subprocess
import windnd

LAST_DIR_FILE = ".last_dir"

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("TXT转SRT字幕工具 - by：C")
        self.master.geometry("800x650")
        
        # 设置主题颜色
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196F3"  # Material Design 蓝色
        self.button_bg = "#2196F3"
        self.button_fg = "white"
        self.hover_color = "#1976D2"
        self.tab_selected_bg = "#ffffff"  # 选中时为白色背景
        self.tab_normal_bg = "#e0e0e0"    # 未选中时为浅灰色背景
        self.tab_text_color = "#333333"    # 文字统一使用深灰色
        
        # 设置窗口背景色
        self.master.configure(bg=self.bg_color)
        
        # 创建主框架
        self.main_frame = tk.Frame(self.master, padx=30, pady=30, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both')
        
        # 创建标题
        self.title_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.title_frame.pack(fill='x', pady=(0, 20))
        
        self.title_label = tk.Label(
            self.title_frame,
            text="TXT转SRT字幕工具",
            font=("Microsoft YaHei UI", 16, "bold"),
            bg=self.bg_color,
            fg="#333333"
        )
        self.title_label.pack(side='left')
        
        # 创建选项卡
        self.style = ttk.Style()
        self.style.configure(
            "Custom.TNotebook",
            background=self.bg_color,
            padding=[10, 5],
            tabmargins=[2, 5, 2, 0]
        )
        self.style.configure(
            "Custom.TNotebook.Tab",
            padding=[15, 5],
            font=("Microsoft YaHei UI", 10),
            background=self.tab_normal_bg,
            foreground=self.tab_text_color
        )
        self.style.map(
            "Custom.TNotebook.Tab",
            background=[("selected", self.tab_selected_bg), ("!selected", self.tab_normal_bg)],
            foreground=[("selected", self.tab_text_color), ("!selected", self.tab_text_color)]
        )
        
        self.tab_control = ttk.Notebook(self.main_frame, style="Custom.TNotebook")
        self.tab_control.pack(expand=True, fill='both')
        
        # 文件转换选项卡
        self.file_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.file_tab, text='文件转换')
        
        # 文本编辑选项卡
        self.text_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.text_tab, text='文本编辑')
        
        self.setup_file_tab()
        self.setup_text_tab()
        
        # 存储批量文件列表
        self.batch_files = []
        
        # 设置拖放支持
        windnd.hook_dropfiles(self.master, func=self.handle_drop)
        
        # 加载上次使用的输出目录
        self.load_last_output_dir()
        
    def create_button(self, parent, text, command):
        """创建统一风格的按钮"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Microsoft YaHei UI", 9),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.configure(background=self.hover_color))
        btn.bind("<Leave>", lambda e: btn.configure(background=self.button_bg))
        return btn
        
    def create_entry_frame(self, parent, label_text):
        """创建统一风格的输入框架"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill='x', pady=10)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Microsoft YaHei UI", 10),
            bg=self.bg_color,
            fg="#333333"
        )
        label.pack(side='left')
        
        return frame
        
    def setup_file_tab(self):
        # 添加说明文本
        self.guide_label = tk.Label(
            self.file_tab,
            text="支持的TXT文件格式：\n1. 每行以时间戳开头（如：0:00 或 1:23:45）\n2. 时间戳后面是字幕文本",
            font=("Microsoft YaHei UI", 9),
            bg=self.bg_color,
            fg="#666666",
            justify=tk.LEFT
        )
        self.guide_label.pack(anchor='w', pady=(0, 20))
        
        # 文件选择
        self.file_frame = self.create_entry_frame(self.file_tab, "选择文件：")
        
        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(
            self.file_frame,
            textvariable=self.file_path,
            width=50,
            font=("Microsoft YaHei UI", 9),
            relief="solid",
            bd=1
        )
        self.file_entry.pack(side='left', padx=5)
        
        self.file_button = self.create_button(self.file_frame, "浏览", self.select_file)
        self.file_button.pack(side='left', padx=2)
        
        self.batch_button = self.create_button(self.file_frame, "批量选择", self.select_batch_files)
        self.batch_button.pack(side='left', padx=2)
        
        # 输出路径选择
        self.output_frame = self.create_entry_frame(self.file_tab, "输出路径：")
        
        self.output_path = tk.StringVar()
        self.output_entry = tk.Entry(
            self.output_frame,
            textvariable=self.output_path,
            width=50,
            font=("Microsoft YaHei UI", 9),
            relief="solid",
            bd=1
        )
        self.output_entry.pack(side='left', padx=5)
        
        self.output_button = self.create_button(self.output_frame, "浏览", self.select_output)
        self.output_button.pack(side='left')
        
        # 转换按钮
        self.convert_button = self.create_button(self.file_tab, "开始转换", self.start_conversion)
        self.convert_button.pack(pady=20)
        
        # 状态显示
        self.status_label = tk.Label(
            self.file_tab,
            text="就绪",
            font=("Microsoft YaHei UI", 9),
            bg=self.bg_color,
            fg="#666666"
        )
        self.status_label.pack(pady=10)
        
        # 打开结果文件按钮
        self.open_result_button = self.create_button(self.file_tab, "打开结果文件", self.open_result_file)
        self.open_result_button.pack(pady=5)
        
    def setup_text_tab(self):
        # 文本编辑区域
        self.text_frame = tk.Frame(self.text_tab, bg=self.bg_color)
        self.text_frame.pack(fill='both', expand=True, pady=10)
        
        # 添加文本编辑说明
        self.text_guide = tk.Label(
            self.text_frame,
            text="在下方输入要转换的文本：",
            font=("Microsoft YaHei UI", 10),
            bg=self.bg_color,
            fg="#333333"
        )
        self.text_guide.pack(anchor='w', pady=(0, 5))
        
        self.text_edit = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            height=15,
            font=("Microsoft YaHei UI", 10),
            relief="solid",
            bd=1,
            padx=5,
            pady=5
        )
        self.text_edit.pack(fill='both', expand=True)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.text_edit)
        scrollbar.pack(side='right', fill='y')
        self.text_edit.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_edit.yview)
        
        # 输出路径选择
        self.text_output_frame = self.create_entry_frame(self.text_tab, "输出路径：")
        
        self.text_output_path = tk.StringVar()
        self.text_output_entry = tk.Entry(
            self.text_output_frame,
            textvariable=self.text_output_path,
            width=50,
            font=("Microsoft YaHei UI", 9),
            relief="solid",
            bd=1
        )
        self.text_output_entry.pack(side='left', padx=5)
        
        self.text_output_button = self.create_button(self.text_output_frame, "浏览", self.select_text_output)
        self.text_output_button.pack(side='left')
        
        # 转换按钮
        self.text_convert_button = self.create_button(self.text_tab, "转换文本", self.convert_text)
        self.text_convert_button.pack(pady=20)
        
    def save_last_output_dir(self):
        """保存最后使用的输出目录"""
        try:
            with open(LAST_DIR_FILE, 'w', encoding='utf-8') as f:
                f.write(self.output_path.get() + '\n')
                f.write(self.text_output_path.get())
            # 在Windows上设置文件为隐藏
            if os.name == 'nt':
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(LAST_DIR_FILE, 0x02)
        except Exception as e:
            print(f"保存目录信息时出错：{str(e)}")
            
    def load_last_output_dir(self):
        """加载上次使用的输出目录"""
        try:
            if os.path.exists(LAST_DIR_FILE):
                with open(LAST_DIR_FILE, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) >= 1:
                        last_dir = lines[0].strip()
                        if os.path.exists(last_dir):
                            self.output_path.set(last_dir)
                    if len(lines) >= 2:
                        last_text_dir = lines[1].strip()
                        if os.path.exists(last_text_dir):
                            self.text_output_path.set(last_text_dir)
        except Exception as e:
            print(f"加载目录信息时出错：{str(e)}")
            
    def handle_drop(self, files):
        """处理文件拖放"""
        if files:
            file_path = files[0].decode('gbk')  # Windows 使用 GBK 编码
            if file_path.lower().endswith('.txt'):
                if self.tab_control.select() == self.tab_control.tabs()[0]:  # 文件转换选项卡
                    self.file_path.set(file_path)
                    self.batch_files = [file_path]
                else:  # 文本编辑选项卡
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.text_edit.delete("1.0", tk.END)
                            self.text_edit.insert("1.0", f.read())
                    except Exception as e:
                        messagebox.showerror("错误", f"读取文件时出错：{str(e)}")
            
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择TXT文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            self.batch_files = [file_path]
            
    def select_batch_files(self):
        file_paths = filedialog.askopenfilenames(
            title="选择多个TXT文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_paths:
            self.batch_files = list(file_paths)
            self.file_path.set(f"已选择 {len(file_paths)} 个文件")
            
    def select_output(self):
        output_path = filedialog.askdirectory(title="选择输出目录")
        if output_path:
            self.output_path.set(output_path)
            self.save_last_output_dir()
            
    def select_text_output(self):
        output_path = filedialog.askdirectory(title="选择输出目录")
        if output_path:
            self.text_output_path.set(output_path)
            self.save_last_output_dir()
            
    def start_conversion(self):
        if not self.batch_files:
            messagebox.showerror("错误", "请选择要转换的文件！")
            return
            
        if not self.output_path.get():
            messagebox.showerror("错误", "请选择输出路径！")
            return
            
        try:
            self.status_label.config(text="正在转换...")
            self.convert_button.config(state='disabled')
            self.master.update()
            
            success_count = 0
            for file_path in self.batch_files:
                try:
                    convert_file(file_path, self.output_path.get())
                    success_count += 1
                except Exception as e:
                    messagebox.showerror("错误", f"转换文件 {os.path.basename(file_path)} 时出错：{str(e)}")
            
            self.status_label.config(text=f"转换完成！成功转换 {success_count}/{len(self.batch_files)} 个文件")
            messagebox.showinfo("成功", f"成功转换 {success_count}/{len(self.batch_files)} 个文件！")
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出现错误：{str(e)}")
        finally:
            self.convert_button.config(state='normal')
            
    def convert_text(self):
        if not self.text_edit.get("1.0", tk.END).strip():
            messagebox.showerror("错误", "请输入要转换的文本！")
            return
            
        if not self.text_output_path.get():
            messagebox.showerror("错误", "请选择输出路径！")
            return
            
        try:
            # 创建临时文件
            temp_file = os.path.join(self.text_output_path.get(), "temp.txt")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.get("1.0", tk.END))
            
            # 转换文件
            convert_file(temp_file, self.text_output_path.get())
            
            # 删除临时文件
            os.remove(temp_file)
            
            messagebox.showinfo("成功", "文本转换完成！")
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出现错误：{str(e)}")
            
    def open_result_file(self):
        if not self.output_path.get():
            messagebox.showerror("错误", "请先选择输出路径！")
            return
            
        try:
            # 使用系统默认程序打开输出目录
            if os.name == 'nt':  # Windows
                os.startfile(self.output_path.get())
            else:  # macOS 和 Linux
                subprocess.run(['xdg-open', self.output_path.get()])
        except Exception as e:
            messagebox.showerror("错误", f"打开输出目录时出错：{str(e)}") 