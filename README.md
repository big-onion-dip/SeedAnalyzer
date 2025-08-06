# SeedAnalyzer

SeedAnalyzer 是一个用于图像分析的应用程序，主要用于通过高拍仪捕捉种子图像并进行分析。该项目结合了串口通信和图像处理技术，适用于农业、科研等领域。

## 项目结构

```
SeedAnalyzer/
│
├── src/
│   ├── main.py                  # 主程序文件
│   ├── camera.py                # 与摄像头相关的功能
│   ├── serial_communication.py   # 串口通信相关功能
│   ├── image_analysis.py         # 图像分析相关功能
│   └── utils.py                 # 工具函数
│
├── resources/
│   ├── CamLib.dll               # DLL 文件
│   └── config.json              # 配置文件
│
├── output/                      # 输出目录
│
├── requirements.txt             # 项目依赖
└── README.md                    # 项目说明文档
```

## 安装

1. 克隆此仓库：

   ```bash
   git clone https://github.com/yourusername/SeedAnalyzer.git
   cd SeedAnalyzer
   ```

2. 安装所需的 Python 库：

   ```bash
   pip install -r requirements.txt
   ```

3. 确保将 `CamLib.dll` 文件放置在 `resources/` 目录中。

## 使用

1. 运行主程序：

   ```bash
   python src/main.py
   ```

2. 在应用程序中选择串口并连接设备。

3. 调整分析参数，如最小和最大种子面积。

4. 点击“拍照并分析”按钮捕捉图像并进行分析。

5. 分析结果将保存在 `output/` 目录中，包括可视化图像和特征数据的 CSV 文件。

## 配置

在 `resources/config.json` 文件中，您可以调整以下参数：

```json
{
    "min_seed_area": 1000,
    "max_seed_area": 5000,
    "filename_prefix": "photo",
    "save_binary_image": false
}
```

- `min_seed_area`: 最小种子面积。
- `max_seed_area`: 最大种子面积。
- `filename_prefix`: 输出文件名前缀。
- `save_binary_image`: 是否保存二值图像。

## 贡献

欢迎提交问题和拉取请求。如果您有任何建议或问题，请通过 GitHub 提交问题。

## 许可证

此项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。
