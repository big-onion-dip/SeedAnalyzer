import tkinter as tk
from tkinter import messagebox
from camera import init_camera, open_camera, close_camera, capture_image
from serial_communication import SerialCommunication
from image_analysis import analyze_image
import json
import os

# 读取配置文件
def load_config():
    with open('../resources/config.json', 'r') as f:
        return json.load(f)

# 主程序类
class SeedAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Seed Analyzer")
        
        self.config = load_config()
        self.serial_comm = SerialCommunication()
        
        # GUI 组件
        self.create_widgets()

        # 初始化摄像头
        try:
            init_camera()
            self.camera_opened = False
        except Exception as e:
            messagebox.showerror("错误", f"初始化摄像头失败: {str(e)}")

    def create_widgets(self):
        # 串口连接
        self.port_label = tk.Label(self.master, text="选择串口:")
        self.port_label.pack()

        self.port_list = tk.Listbox(self.master)
        self.port_list.pack()

        self.connect_button = tk.Button(self.master, text="连接串口", command=self.connect_serial)
        self.connect_button.pack()

        # 拍照和分析按钮
        self.capture_button = tk.Button(self.master, text="拍照并分析", command=self.capture_and_analyze)
        self.capture_button.pack()

    def connect_serial(self):
        selected_port = self.port_list.get(tk.ACTIVE)
        if selected_port:
            port = selected_port.split(" - ")[0]
            try:
                self.serial_comm.connect(port)
                messagebox.showinfo("成功", "串口连接成功！")
            except Exception as e:
                messagebox.showerror("错误", f"连接串口失败: {str(e)}")

    def capture_and_analyze(self):
        if not self.camera_opened:
            # 打开摄像头
            try:
                open_camera(0, self.master.winfo_id())
                self.camera_opened = True
            except Exception as e:
                messagebox.showerror("错误", f"打开摄像头失败: {str(e)}")
                return

        # 拍照并分析
        try:
            save_path = "../output/photo.jpg"
            capture_image(0, save_path)
            traits = analyze_image(save_path, self.config['min_seed_area'], self.config['max_seed_area'], self.config['save_binary_image'])
            messagebox.showinfo("分析结果", f"分析完成，共检测到 {len(traits)} 个种子。")
        except Exception as e:
            messagebox.showerror("错误", f"分析失败: {str(e)}")
        finally:
            close_camera(0)

# 启动程序
if __name__ == "__main__":
    root = tk.Tk()
    app = SeedAnalyzerApp(root)
    root.mainloop()