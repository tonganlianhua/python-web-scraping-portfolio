# -*- coding: utf-8 -*-
"""
链家房产信息爬虫配置文件
"""

# 城市配置
CITIES = {
    'bj': '北京',
    'sh': '上海', 
    'sz': '深圳',
    'gz': '广州',
    'hz': '杭州',
    'cd': '成都',
    'wh': '武汉',
    'nj': '南京'
}

# 户型映射
ROOM_TYPES = {
    '1': '一居',
    '2': '二居',
    '3': '三居',
    '4': '四居',
    '5': '五居及以上'
}

# 默认配置
DEFAULT_CONFIG = {
    'city': 'bj',  # 默认城市：北京
    'region': '',  # 默认区域：全部
    'price_min': 0,  # 默认最低价格
    'price_max': 0,  # 默认最高价格（0表示不限制）
    'room_type': '',  # 默认户型（空表示全部）
    'max_pages': 5,  # 默认最大爬取页数
    'delay_min': 1,  # 最小延迟时间（秒）
    'delay_max': 3,  # 最大延迟时间（秒）
    'timeout': 30,  # 请求超时时间（秒）
    'retry_times': 3,  # 重试次数
}

# 请求URL模板
URL_TEMPLATES = {
    'ershoufang': 'https://{city}.lianjia.com/ershoufang/{region}/',
    'ershoufang_with_params': 'https://{city}.lianjia.com/ershoufang/{region}/pg{page}/'
}

# 字段映射
FIELD_MAPPING = {
    'title': '标题',
    'price': '总价（万元）',
    'unit_price': '单价（元/平米）',
    'area': '面积（平米）',
    'room_type': '户型',
    'floor': '楼层',
    'orientation': '朝向',
    'decoration': '装修',
    'community': '小区',
    'address': '地址',
    'url': '房源链接',
    'region': '区域',
    'city': '城市'
}
