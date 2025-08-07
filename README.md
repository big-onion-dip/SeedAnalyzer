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
├── SeedAnalyzer.exe       # 可执行软件包，需密钥
├── main.py                # 主程序入口
├── gui.py                 # 图形用户界面 (Tkinter)
├── serial_manager.py      # 串口连接与读取模块（读取电子秤数据）
├── camera_controller.py   # 摄像头控制模块（调用 DLL 拍照）
├── image_analyzer.py      # 图像分析与种子特征提取模块（OpenCV + skimage）
├── utils.py               # 工具函数
│
├── output_seeds/          # 输出图像、特征表、统计结果等
├── resources/             # 资源文件夹
│   └── *.dll              # 摄像头 DLL 文件（如 CamLib.dll）
├── requirements.txt       # Python 依赖包列表
└── README.md              # 本说明文件

```

## ▶️ 快速开始-exe文件执行
1. 下载并安装 SeedAnalyzer.exe
2. 运行 SeedAnalyzer.exe
3. 完成，密钥请联系作者进行提供
---

## ▶️ 快速开始-python代码运行

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
