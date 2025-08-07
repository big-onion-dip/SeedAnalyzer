# 🌱 SeedAnalyzer - 种子图像分析系统

> 基于图像识别与串口读取的种子特征提取与千粒重计算软件

---

## 📦 项目简介

**SeedAnalyzer** 是一个集成了图像识别与串口数据读取的图形界面程序，适用于种子图像的自动分析。软件支持摄像头拍照、种子识别、主轴测量、粘连种子分割、串口读取重量与种子数量，并自动计算千粒重。适用于农业科研、品种选育等场景。

---

## 🧩 功能亮点

* 📸 **摄像头拍照**：通过调用高拍仪 SDK 实现快速拍照。
* 🧠 **图像识别**：自动识别种子区域，支持分水岭与凸缺陷分割粘连种子。
* 🧮 **特征提取**：提取面积、长轴、短轴等关键特征。
* ⚖️ **串口读取重量**：自动读取串口天平重量。
* 📊 **千粒重计算**：自动根据种子数和总重计算千粒重。
* 💾 **结果导出**：支持图像结果与统计表导出。
* 🖥️ **图形界面**：简洁直观的 Tkinter + ttkbootstrap UI。

---

## 🛠️ 项目结构

```
SeedAnalyzer/
│
├── src/
│   ├── main.py              # 主程序入口
│   ├── gui.py               # 图形用户界面 (Tkinter)
│   ├── serial_manager.py    # 串口连接与读取模块
│   ├── camera_controller.py # 摄像头控制模块（调用 DLL）
│   ├── image_analyzer.py    # 图像分析与种子特征提取模块
│   └── utils.py             # 工具函数模块
│
├── output_seeds/           # 输出图像与结果表目录
├── CamLib.dll              # 高拍仪摄像头 SDK（Windows 下必需）
├── requirements.txt        # 依赖包列表
└── README.md               # 项目说明文档（本文件）
```

---

## ▶️ 快速开始

### 🖥️ 环境要求

* Python 3.9+
* Windows 10+
* 安装摄像头 DLL 驱动：确保 `CamLib.dll` 位于 `src/` 或系统路径中。

### 📦 安装依赖

```bash
pip install -r requirements.txt
```

### 🚀 运行程序

```bash
python src/main.py
```

---

## 🧰 打包为可执行程序（Windows）

使用 [`pyinstaller`](https://pyinstaller.org/) 将程序打包为 `.exe`：

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 打包命令

在 `src/` 目录下运行：

```bash
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "CamLib.dll;." ^
    --add-data "../output_seeds;output_seeds" ^
    main.py
```

**说明**：

* `--onefile` 打包为单一可执行文件
* `--windowed` 隐藏控制台窗口
* `--add-data` 添加 DLL 和输出目录资源

打包后的可执行文件位于 `dist/main.exe`

---

## 📊 依赖列表（requirements.txt）

```txt
numpy
pandas
opencv-python
Pillow
scipy
scikit-image
pyserial
ttkbootstrap
```

---

## 📷 图像分析说明

图像处理流程如下：

1. 拍照后读取图像
2. 二值化处理 + 距离变换
3. 峰值标记 + 分水岭分割
4. 标记区域提取 + 过滤面积
5. 特征测量（面积、主轴等）

---

## 🧪 串口模块说明

自动连接天平串口，默认设置：

```python
serial.Serial(
    port="COM6",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)
```

---

## 📁 结果导出

程序自动将以下结果保存至 `output_seeds/` 目录：

* 处理后的图像文件（标注种子编号、主轴等）
* 对应的特征统计表（.csv）
* 种子数量与重量记录表

---

## 👨‍💻 开发者

* **作者**：程文聪
* **联系邮箱**：17362070907@163.com
* **项目版本**：v1.3.0
* **许可证**：MIT License

---

如需进一步扩展功能或部署为实验室系统，请联系作者协助定制。

---
