#!/usr/bin/env python3
"""
Excel 连接诊断工具 - 快速检查 Excel 连接状态
"""
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

from excel_connector import ExcelConnector
from logger import log_info

def main():
    print("\n" + "="*60)
    print("Excel 连接诊断工具")
    print("="*60 + "\n")
    
    connector = ExcelConnector()
    
    print("正在诊断 Excel 连接状态...\n")
    diagnose_result = connector.diagnose()
    print(diagnose_result)
    
    print("\n" + "-"*60)
    print("尝试获取选中的单元格...\n")
    
    cells, error = connector.get_selected_cells()
    
    if error:
        print(f"错误: {error}")
        print("\n故障排除建议:")
        print("1. 确保 Excel 已打开")
        print("2. 在 Excel 中选择至少一个单元格")
        print("3. 检查防火墙和防病毒软件是否阻止了 COM 调用")
        print("4. 查看日志文件: logs/app_*.log")
    else:
        if cells:
            print(f"✓ 成功获取 {len(cells)} 个单元格:\n")
            for cell in cells[:5]:  # 只显示前5个
                print(f"  - {cell['address']}: {cell['value']}")
            if len(cells) > 5:
                print(f"  ... 还有 {len(cells) - 5} 个")
        else:
            print("⚠️ 未选中任何单元格（请在 Excel 中选择数据）")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
