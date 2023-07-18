import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("dgn转BIM工具_xay")
        self.create_widgets()

    def create_widgets(self):
        # 控件1：选择DgnV8Converter.exe文件路径
        self.label1 = tk.Label(self.master, text="DgnV8Converter.exe文件路径↓")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry1 = tk.Entry(self.master)
        self.entry1.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        # 设置默认值
        self.entry1.insert(0, r"\\10.138.10.199\dwzxbd\bdsw\bentley最新程序安装包及教学视频\imodelbridges\IModelBridgeForMstn\DgnV8Converter.exe")
        self.button1 = tk.Button(self.master, text="选择exe文件", command=self.load_converter_path)
        self.button1.grid(row=1, column=1, padx=5, pady=5)

        # 控件2：选择输入文件路径
        self.label2 = tk.Label(self.master, text="输入文件路径↓")
        self.label2.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry2 = tk.Entry(self.master)
        self.entry2.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        self.button2 = tk.Button(self.master, text="选择dgn文件", command=self.load_input_path)
        self.button2.grid(row=3, column=1, padx=5, pady=5)

        # 控件3：指定输出文件路径
        self.label3 = tk.Label(self.master, text="输出文件路径↓")
        self.label3.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry3 = tk.Entry(self.master)
        self.entry3.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        self.button3 = tk.Button(self.master, text="选择路径", command=self.choose_output_path)
        self.button3.grid(row=5, column=1, padx=5, pady=5)

        # 控件4：确定和取消按钮
        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.confirm_button = tk.Button(self.button_frame, text="确定", command=self.run_command)
        self.confirm_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.quit_button = tk.Button(self.button_frame, text="取消", fg="red", command=self.master.destroy)
        self.quit_button.pack(side=tk.LEFT, padx=5, pady=5)

    def load_converter_path(self):
        # 打开文件选择对话框，获取选择的文件路径
        filename = filedialog.askopenfilename()
        if filename:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, filename)
        else:
            messagebox.showwarning("警告", "请选择DgnV8Converter.exe文件路径！")

    def load_input_path(self):
        # 打开文件选择对话框，获取选择的文件路径
        filename = filedialog.askopenfilename()
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, filename)

        # 获取输入文件路径的目录
        input_dir = os.path.dirname(filename)

        # 如果未指定输出文件路径，则默认输出文件与输入文件在同一目录下，文件名为空
        if not self.entry3.get():
            self.entry3.delete(0, tk.END)
            self.entry3.insert(0, input_dir)

    def choose_output_path(self):
        # 打开文件夹选择对话框，获取选择的文件夹路径
        foldername = filedialog.askdirectory()
        self.entry3.delete(0, tk.END)
        self.entry3.insert(0, foldername)

    def run_command(self):
        # 获取控件1、2、3中的输入
        exe_path = self.entry1.get()
        input_path = self.entry2.get()
        output_path = self.entry3.get()

        # 如果未指定输出文件路径，则默认输出文件与输入文件在同一目录下，文件名为空
        if not os.path.basename(output_path):
            output_path = os.path.join(output_path, "")

        if not os.path.exists(exe_path):
            messagebox.showerror("错误", "无法访问DgnV8Converter.exe文件，请重新选择exe文件位置！")
        else:
            # 构建命令行参数
            command = f'"{exe_path}" -i="{input_path}" -o="{output_path}" --compress'

            # 执行命令
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 等待命令执行完成并获取控制台输出
            output, error = process.communicate()

            # 如果控制台输出中包含"Created"字段，则表示BIM文件生成成功
            if "Created" in str(output):
                # 弹出生成成功提示
                messagebox.showinfo("提示", "BIM文件生成成功！")
            else:
                # 弹出生成失败提示
                messagebox.showerror("错误", "BIM文件生成失败！请检查输入文件路径或输出文件路径是否正确。")
root = tk.Tk()
app = Application(master=root)
app.mainloop()