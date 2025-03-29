# TXT to STR 转换器

一个简单易用的Windows文本文件转换工具，可以将TXT文件转换为STR格式。

## 功能特点

- 简洁的图形用户界面
- 支持自定义输出路径
- 实时显示转换状态
- 支持批量文件转换
- 完全兼容Windows系统

## 系统要求

- Windows 7/8/10/11
- Python 3.6 或更高版本

## 安装方法

1. 下载最新版本的发布包
2. 解压到任意目录
3. 运行 `txttostr.exe`

## 使用方法

1. 点击"选择文件"按钮选择要转换的TXT文件
2. 点击"选择输出路径"按钮选择保存位置
3. 点击"开始转换"按钮进行转换
4. 等待转换完成提示

## 开发环境设置

1. 克隆项目到本地
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行开发版本：
   ```
   python src/main.py
   ```

## 项目结构

```
txttostr/
├── src/
│   ├── main.py          # 主程序入口
│   ├── gui.py           # 图形界面相关代码
│   └── converter.py     # 文件转换核心逻辑
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明文档
```

## 许可证

MIT License 