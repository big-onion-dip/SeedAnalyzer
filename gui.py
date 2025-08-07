import os
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import sys
from serial_communication import SerialManager
from camera import CameraManager
from image_analysis import analyze_image
from utils import extract_weight

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "output_seeds"))
os.makedirs(OUT_DIR, exist_ok=True)

class SeedAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SeedAnalyzer - V1.3.0 by LiuLab-CWC")
        self.geometry("1100x700")
        self.serial = SerialManager(self)
        self.camera = CameraManager(self)

        self.photo_counter = 0
        self.last_base_name = None
        self.latest_weight = None
        self.seed_count = 0
        self.records = []

        # 参数变量
        self.min_seed_area = tk.IntVar(value=1000)
        self.max_seed_area = tk.IntVar(value=5000)
        self.max_seed_length = tk.IntVar(value=100)
        self.filename_prefix = tk.StringVar(value="photo")
        self.save_binary_image = tk.BooleanVar(value=False)
        self.thousand_weight_var = tk.StringVar(value="N/A")

        self.init_ui()
        self.camera.init_camera()

    def init_ui(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="y")

        # 串口区
        frame_serial = tk.LabelFrame(left_frame, text="串口连接")
        frame_serial.pack(fill="x")
        self.combo_ports = ttk.Combobox(frame_serial, values=self.serial.list_ports(), state="readonly", width=40)
        self.combo_ports.pack(side="left", padx=5)
        ttk.Button(frame_serial, text="刷新", command=self.refresh_ports).pack(side="left", padx=5)
        ttk.Button(frame_serial, text="连接", command=self.connect_serial).pack(side="left", padx=5)
        self.btn_disconnect = ttk.Button(frame_serial, text="断开", command=self.disconnect_serial, state="disabled")
        self.btn_disconnect.pack(side="left", padx=5)

        self.text_serial = tk.Text(left_frame, height=6)
        self.text_serial.pack(fill="x", pady=5)

        # 参数设置
        frame_params = tk.LabelFrame(left_frame, text="分析参数")
        frame_params.pack(fill="x", pady=5)
        for label, var, width in [
            ("最小面积", self.min_seed_area, 8),
            ("最大面积", self.max_seed_area, 8),
            ("最大长轴", self.max_seed_length, 8),
            ("文件前缀", self.filename_prefix, 12),
        ]:
            tk.Label(frame_params, text=label).pack(side="left", padx=5)
            tk.Entry(frame_params, textvariable=var, width=width).pack(side="left")
        tk.Checkbutton(frame_params, text="输出二值图", variable=self.save_binary_image).pack(side="left", padx=10)

        # 视频区
        self.video_frame = tk.Frame(left_frame, width=480, height=360, bg="black")
        self.video_frame.pack(pady=10)

        # 按钮
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="拍照并分析", command=self.take_photo).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="保存重量", command=self.save_weight_to_txt).pack(side="left", padx=10)

        # 右侧信息区
        info_frame = tk.LabelFrame(right_frame, text="记录与统计")
        info_frame.pack(fill="both", expand=True)
        self.label_weight = tk.Label(info_frame, text="当前重量：N/A", font=("Arial", 12))
        self.label_weight.pack(pady=5)
        self.label_count = tk.Label(info_frame, text="种子数量：0", font=("Arial", 12))
        self.label_count.pack(pady=5)
        ttk.Label(info_frame, text="千粒重 (g)", font=("Arial", 12)).pack(pady=5)
        ttk.Label(info_frame, textvariable=self.thousand_weight_var, font=("Arial", 14, "bold"), foreground="blue").pack(pady=5)

        # 表格
        self.tree = ttk.Treeview(info_frame, columns=("文件前缀", "重量 (g)", "种子数", "千粒重"), show="headings", height=20)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        self.tree.pack(fill="both", pady=10)

        ttk.Button(info_frame, text="导出数据", command=self.export_to_excel).pack(pady=5)

    def refresh_ports(self):
        self.combo_ports["values"] = self.serial.list_ports()

    def connect_serial(self):
        self.serial.connect(self.combo_ports.get())

    def disconnect_serial(self):
        self.serial.disconnect()

    def take_photo(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.photo_counter += 1
        base_name = f"{self.filename_prefix.get()}_{timestamp}_{self.photo_counter}"
        self.last_base_name = base_name
        save_path = os.path.join(OUT_DIR, f"{base_name}.jpg")

        if self.camera.capture(save_path):
            traits, count = analyze_image(
                save_path,
                OUT_DIR,
                base_name,
                self.min_seed_area.get(),
                self.max_seed_area.get(),
                self.max_seed_length.get(),
                self.save_binary_image.get()
            )
            self.seed_count = count
            self.label_count.config(text=f"种子数量：{count}")
            try:
                weight = extract_weight(self.latest_weight)
                thousand = round(weight * 1000 / count, 2) if count > 0 else 0
                self.thousand_weight_var.set(str(thousand))
            except:
                self.thousand_weight_var.set("N/A")
            messagebox.showinfo("分析完成", f"识别 {count} 粒种子，已保存至：{OUT_DIR}")
        else:
            messagebox.showerror("拍照失败", "无法保存图像")

    def save_weight_to_txt(self):
        if not self.last_base_name:
            messagebox.showwarning("提示", "请先拍照生成文件名")
            return
        weight = extract_weight(self.latest_weight)
        self.add_record(self.filename_prefix.get(), weight, self.seed_count)
        txt_path = os.path.join(OUT_DIR, f"{self.last_base_name}_weight.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(str(weight))
        
        messagebox.showinfo("保存成功", f"保存重量至：{txt_path}")

    def add_record(self, prefix, weight, count):
        try:
            weight = extract_weight(self.latest_weight)
            thousand = round(weight * 1000 / count, 2) if count > 0 else 0
            self.thousand_weight_var.set(str(thousand))
        except:
            self.thousand_weight_var.set("N/A")
        self.records.append({"文件前缀": prefix, "重量 (g)": weight, "种子数": count, "千粒重": thousand})
        self.tree.insert("", "end", values=(prefix, weight, count, thousand))

    def export_to_excel(self):
        if not self.records:
            messagebox.showwarning("提示", "没有可导出的数据")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel 文件", "*.xlsx")])
        if path:
            pd.DataFrame(self.records).to_excel(path, index=False)
            messagebox.showinfo("导出成功", f"数据导出至：{path}")

    def on_closing(self):
        self.serial.close()
        self.camera.close()
        self.destroy()
