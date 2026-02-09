"""
数据管理和日志记录模块
"""
import os
import json
import datetime
from pathlib import Path


class DataManager:
    """管理数据保存和日志记录"""
    
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = base_dir
        self.output_dir = os.path.join(base_dir, "output")
        self.create_base_dirs()
    
    def create_base_dirs(self):
        """创建基础目录"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_chart_folder(self, chart_name: str) -> str:
        """为每个图表创建新的文件夹"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f"{chart_name}_{timestamp}"
        folder_path = os.path.join(self.output_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def save_chart_data(self, folder_path: str, data: dict, method: str = "unknown"):
        """
        保存图表数据和元信息
        
        Args:
            folder_path: 图表存放的文件夹路径
            data: 数据字典
            method: 统计方法名称
        """
        metadata = {
            "timestamp": datetime.datetime.now().isoformat(),
            "method": method,
            "data": data,
            "datetime_format": "%Y-%m-%d %H:%M:%S"
        }
        
        metadata_path = os.path.join(folder_path, "data.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return metadata_path
    
    def save_log_file(self, folder_path: str, log_content: str):
        """保存日志文件"""
        log_path = os.path.join(folder_path, "log.txt")
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(log_content)
        return log_path
    
    def get_output_dir(self):
        """获取输出目录"""
        return self.output_dir


# 全局实例
_data_manager = None


def get_data_manager():
    """获取全局数据管理器"""
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager
