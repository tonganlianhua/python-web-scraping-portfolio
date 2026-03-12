# 网易云音乐爬虫

from .scraper import Music163Scraper
from .api_client import NetEaseMusicAPI
from .export import DataExporter
from .analyzer import MusicAnalyzer

__version__ = "1.0.0"
__all__ = [
    "Music163Scraper",
    "NetEaseMusicAPI",
    "DataExporter",
    "MusicAnalyzer"
]
