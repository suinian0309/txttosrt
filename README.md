# TXT to SRT 转换器

一个简单易用的 Windows 文本文件转换工具，可以将 TXT 文件转换为 SRT 字幕格式。

## 功能特点

- 简洁的图形用户界面
- 支持自定义输出路径
- 实时显示转换状态
- 支持批量文件转换
- 完全兼容 Windows 系统
- 使用 Nuitka 打包，确保最佳性能

## 系统要求

- Windows 7/8/10/11
- Python 3.6 或更高版本（仅开发环境需要）

## 安装方法

1. 下载最新版本的发布包
2. 解压到任意目录
3. 运行 `txttosrt.exe`

## 使用方法

1. 点击"选择文件"按钮选择要转换的 TXT 文件
2. 点击"选择输出路径"按钮选择保存位置
3. 点击"开始转换"按钮进行转换
4. 等待转换完成提示

## 开发环境设置

1. 克隆项目到本地
2. 创建并激活虚拟环境：
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
4. 运行开发版本：
   ```
   python src/main.py
   ```

## 构建发布版本

1. 确保已安装所有依赖
2. 运行构建脚本：
   ```
   python build.py
   ```
3. 构建完成后，可执行文件将在 `dist` 目录中

## 项目结构

```
txttosrt/
├── src/                    # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── gui.py             # 图形界面相关代码
│   └── converter.py       # 文件转换核心逻辑
├── build.py               # 构建脚本
├── requirements.txt       # 项目依赖
├── app.ico               # 应用程序图标
├── app.manifest          # 应用程序清单
├── config.json           # 配置文件
└── README.md             # 项目说明文档
```

## 许可证

MIT License 