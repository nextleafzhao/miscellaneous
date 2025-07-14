#!/usr/bin/env python3
"""日出日落时间计算工具"""
import argparse
import re
from datetime import date, datetime
from astral import LocationInfo
from astral.sun import sun
import pytz
import sys

def parse_coordinate(coord_str):
    """
    解析多种格式的经纬度字符串：
    - 浮点数 (39.9042)
    - 带方向标识 (116.4074E)
    
    返回：浮点数坐标
    """
    # 尝试直接解析为浮点数
    try:
        return float(coord_str)
    except ValueError:
        pass
    
    # 解析带方向的十进制格式
    match = re.match(r'([-]?\d+\.?\d*)\s*([NSEW])', coord_str, re.IGNORECASE)
    if match:
        coord, direction = match.groups()
        coord = float(coord)
        if direction.upper() in ('S', 'W'):
            coord = -coord
        return coord
    
    raise ValueError(f"无法解析的坐标格式: {coord_str}")

def determine_timezone(longitude, latitude):
    """时区确定算法（基于地理位置）"""
    # 中国（统一使用北京时间）
    if 73 < longitude < 135 and 18 < latitude < 54:
        return "Asia/Shanghai"
    
    # 美国本土
    if -125 < longitude < -66 and 24 < latitude < 50:
        if longitude >= -77.0:    return "America/New_York"
        elif longitude >= -90.0:  return "America/Chicago"
        elif longitude >= -105.0: return "America/Denver"
        else:                    return "America/Los_Angeles"
    
    # 欧洲主要国家
    if -10 < longitude < 40 and 35 < latitude < 70:
        if 2 < longitude < 7 and 45 < latitude < 55:   return "Europe/Paris"
        elif -6 < longitude < 2 and 50 < latitude < 60: return "Europe/London"
        elif 11 < longitude < 16 and 47 < latitude < 55: return "Europe/Berlin"
    
    # 亚洲其他地区
    if 135 < longitude < 145 and 35 < latitude < 45:   return "Asia/Tokyo"
    if 126 < longitude < 132 and 33 < latitude < 39:   return "Asia/Seoul"
    if 72 < longitude < 80 and 8 < latitude < 13:      return "Asia/Colombo"
    
    # 澳洲
    if 113 < longitude < 154 and -45 < latitude < -10:
        if 150 < longitude < 154: return "Australia/Sydney"
        else:                     return "Australia/Perth"
    
    # 基于UTC偏移的通用算法
    utc_offset = round(longitude / 15)
    utc_offset = max(-12, min(14, utc_offset))
    
    # 返回标准IANA时区
    if utc_offset == 0:
        return "UTC"
    elif utc_offset > 0:
        return f"Etc/GMT-{utc_offset}"  # 注意符号规则
    else:
        return f"Etc/GMT+{abs(utc_offset)}"

def parse_date(date_str):
    """解析多种日期格式"""
    formats = [
        "%Y-%m-%d",   # ISO格式 (2023-08-15)
        "%Y/%m/%d",   # 斜杠格式 (2023/08/15)
        "%Y%m%d",     # 紧凑格式 (20230815)
        "%d-%m-%Y",   # 欧洲格式 (15-08-2023)
        "%d/%m/%Y",   # 美国格式 (08/15/2023)
        "%b %d %Y",   # 文本月份 (Aug 15 2023)
        "%d %b %Y"    # 文本月份 (15 Aug 2023)
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"无法识别的日期格式: {date_str}")

def calculate_sun_times(latitude, longitude, date_input=None):
    # 日期处理（支持多种格式）
    target_date = date.today()
    if date_input:
        target_date = parse_date(date_input)
    
    # 时区确定
    timezone_str = determine_timezone(longitude, latitude)
    try:
        local_tz = pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        # 时区回退机制
        utc_offset = round(longitude / 15)
        timezone_str = "Etc/GMT" + ("+" if utc_offset <= 0 else "-") + str(abs(utc_offset))
        local_tz = pytz.timezone(timezone_str)
    
    # 天文计算
    location = LocationInfo(
        name="Custom Location",
        region="Custom",
        timezone=timezone_str,
        latitude=latitude,
        longitude=longitude
    )
    
    try:
        s = sun(location.observer, date=target_date, tzinfo=local_tz)
    except Exception as e:
        # 更具体的错误处理
        if "sun remains below horizon" in str(e):
            raise RuntimeError("错误：该地区当日处于极夜，没有日出日落")
        elif "sun remains above horizon" in str(e):
            raise RuntimeError("错误：该地区当日处于极昼，没有日落")
        else:
            raise RuntimeError(f"天文计算错误: {str(e)}")
    
    return {
        "date": target_date,
        "timezone": timezone_str,
        "dawn": s["dawn"].strftime("%H:%M:%S"),
        "sunrise": s["sunrise"].strftime("%H:%M:%S"),
        "noon": s["noon"].strftime("%H:%M:%S"),
        "sunset": s["sunset"].strftime("%H:%M:%S"),
        "dusk": s["dusk"].strftime("%H:%M:%S")
    }

def main():
    parser = argparse.ArgumentParser(
        description="计算当地日出日落时间",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("latitude", help="纬度（支持：39.9042, 39.9042N）")
    parser.add_argument("longitude", help="经度（支持：116.4074,116.4074E）")
    parser.add_argument("-d", "--date", help="日期（多种格式支持）", default=None)
    
    args = parser.parse_args()
    
    try:
        # 解析坐标
        lat = parse_coordinate(args.latitude)
        lon = parse_coordinate(args.longitude)
        
        # 验证坐标范围
        if not (-90 <= lat <= 90):
            raise ValueError("纬度必须在 -90 到 90 之间")
        if not (-180 <= lon <= 180):
            raise ValueError("经度必须在 -180 到 180 之间")
        
        # 计算日出日落
        result = calculate_sun_times(lat, lon, args.date)
        
        # 输出结果
        print(f"\n日期: {result['date']} (时区: {result['timezone']})")
        print(f"位置: 经度 {lon}, 纬度 {lat}")
        print("=" * 40)
        print(f"天文晨光开始: {result['dawn']}")
        print(f"日出时间:     {result['sunrise']}")
        print(f"太阳正午:     {result['noon']}")
        print(f"日落时间:     {result['sunset']}")
        print(f"天文昏影结束: {result['dusk']}\n")
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()