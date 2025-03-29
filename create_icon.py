from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个 256x256 的图像，使用 RGBA 模式（支持透明度）
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    circle_color = (33, 150, 243, 255)  # Material Design 蓝色
    circle_margin = 10
    draw.ellipse([circle_margin, circle_margin, size - circle_margin, size - circle_margin], fill=circle_color)
    
    # 添加文字
    text = "TXT"
    try:
        # 尝试使用微软雅黑字体
        font = ImageFont.truetype("msyh.ttc", 100)
    except:
        # 如果找不到，使用默认字体
        font = ImageFont.load_default()
    
    # 获取文字大小并计算居中位置
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    
    # 绘制文字
    draw.text((text_x, text_y), text, fill="white", font=font)
    
    # 保存为 ICO 文件
    image.save("app.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

if __name__ == "__main__":
    create_icon() 