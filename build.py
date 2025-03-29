import os
import shutil
from nuitka.__main__ import main

def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__', 'TxtToStr.build', 'TxtToStr.dist', 'TxtToStr.onefile-build']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 清理 .py[co] 文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                os.remove(os.path.join(root, file))

def build():
    """使用Nuitka打包"""
    clean_build()
    
    # Nuitka打包参数
    args = [
        "--module=src",  # 将src作为模块打包
        "--include-package=src",  # 包含src包
        "--include-package=windnd",  # 包含windnd包
        "--include-package-data=src",  # 包含src包的数据文件
        "--windows-icon-from-ico=app.ico",  # 设置图标
        "--windows-company-name=C",  # 设置公司名
        "--windows-product-name=TxtToStr",  # 设置产品名
        "--windows-file-version=1.0.0",  # 设置文件版本
        "--windows-product-version=1.0.0",  # 设置产品版本
        "--windows-file-description=TXT字幕转换工具",  # 设置文件描述
        "--windows-disable-console",  # 禁用控制台
        "--assume-yes-for-downloads",  # 自动下载依赖
        "--enable-plugin=tk-inter",  # 启用tk-inter插件
        "--onefile",  # 打包成单文件
        "--output-dir=dist",  # 输出目录
        "--remove-output",  # 删除临时文件
        "--windows-uac-admin",  # 请求管理员权限
        "--windows-manifest-uac-auto-elevate",  # UAC自动提升
        "--jobs=4",  # 使用4个线程编译
        "src/main.py"  # 入口文件
    ]
    
    main(args)

if __name__ == "__main__":
    build() 