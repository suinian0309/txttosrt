import os
import re
from typing import List, Tuple

class TimeStamp:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def to_srt_format(self) -> str:
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d},000"

    @staticmethod
    def from_string(time_str: str) -> 'TimeStamp':
        try:
            parts = time_str.strip().split(':')
            if len(parts) == 2:
                # 处理 M:SS 格式 (如 0:00, 1:23)
                minutes = int(parts[0])
                seconds = int(parts[1])
                return TimeStamp(0, minutes, seconds)
            elif len(parts) == 3:
                # 处理 H:MM:SS 格式
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return TimeStamp(hours, minutes, seconds)
            else:
                raise ValueError(f"无效的时间格式: {time_str}")
        except ValueError as e:
            raise ValueError(f"无法解析时间字符串 '{time_str}': {str(e)}")

def is_time_stamp(text: str) -> bool:
    """检查是否为时间戳格式"""
    patterns = [
        r'^\d{1,2}:\d{2}$',           # 匹配 M:SS 格式
        r'^\d{1,2}:\d{2}:\d{2}$',     # 匹配 H:MM:SS 格式
        r'^\d{1,2}:\d{2}\.\d{3}$',    # 匹配 M:SS.mmm 格式
        r'^\d{1,2}:\d{2}:\d{2}\.\d{3}$' # 匹配 H:MM:SS.mmm 格式
    ]
    return any(re.match(pattern, text.strip()) for pattern in patterns)

def convert_time_to_srt(time_str):
    """将各种时间格式转换为SRT格式的时间戳 (00:00:00,000)"""
    time_str = time_str.strip()
    
    # 如果已经是完整的SRT格式，直接返回
    if re.match(r'^\d{2}:\d{2}:\d{2},\d{3}$', time_str):
        return time_str
        
    # 处理不同的输入格式
    parts = time_str.replace('.', ',').split(':')
    
    if len(parts) == 2:  # M:SS 或 M:SS,mmm
        minutes, seconds = parts
        hours = '00'
    else:  # H:MM:SS 或 H:MM:SS,mmm
        hours, minutes, seconds = parts
    
    # 处理毫秒部分
    if ',' in seconds:
        seconds, milliseconds = seconds.split(',')
        milliseconds = milliseconds.ljust(3, '0')[:3]
    else:
        milliseconds = '000'
    
    # 确保所有部分都是两位数
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    seconds = seconds.zfill(2)
    
    return f"{hours}:{minutes}:{seconds},{milliseconds}"

def convert_file(input_file, output_dir=None):
    """将TXT文件转换为SRT格式"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"找不到输入文件: {input_file}")
    
    # 确定输出文件路径
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}.srt")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 处理文件内容
    subtitle_index = 1
    output_lines = []
    current_start_time = None
    current_end_time = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 检查是否已经是SRT格式（包含序号和箭头）
        if re.match(r'^\d+\s+\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}$', line):
            # 如果已有待处理的字幕，先保存它
            if current_start_time is not None and current_text:
                output_lines.extend([
                    str(subtitle_index),
                    f"{current_start_time} --> {current_end_time or current_start_time}",
                    '\n'.join(current_text),
                    ''
                ])
                subtitle_index += 1
            
            # 提取时间戳
            time_match = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', line)
            if time_match:
                current_start_time = time_match.group(1)
                current_end_time = time_match.group(2)
                current_text = []
            continue
            
        # 检查行首是否为时间戳
        first_part = line.split(maxsplit=1)[0]
        if is_time_stamp(first_part):
            # 如果已有待处理的字幕，先保存它
            if current_start_time is not None and current_text:
                output_lines.extend([
                    str(subtitle_index),
                    f"{current_start_time} --> {current_end_time or current_start_time}",
                    '\n'.join(current_text),
                    ''
                ])
                subtitle_index += 1
            
            # 处理新的时间戳和文本
            current_start_time = convert_time_to_srt(first_part)
            # 设置结束时间为开始时间加3秒
            current_end_time = convert_time_to_srt(f"{int(first_part.split(':')[0])}:{int(first_part.split(':')[1]) + 3}")
            current_text = [line.split(maxsplit=1)[1] if len(line.split(maxsplit=1)) > 1 else '']
        elif current_start_time is not None:
            # 将这行添加到当前字幕文本中
            current_text.append(line)
    
    # 处理最后一条字幕
    if current_start_time is not None and current_text:
        output_lines.extend([
            str(subtitle_index),
            f"{current_start_time} --> {current_end_time or current_start_time}",
            '\n'.join(current_text),
            ''
        ])
    
    # 写入输出文件，确保使用UTF-8编码，并添加BOM标记
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(output_lines))
    
    return output_file 