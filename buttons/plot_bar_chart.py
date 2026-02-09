"""
柱形图按钮模块
"""
import tkinter as tk
from tkinter import messagebox
import datetime
import json


class PlotBarChartButton:
    """柱形图按钮"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="柱形图",
            command=self.plot_bar_chart,
            bg="#607D8B",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button
    
    def plot_bar_chart(self):
        """绘制单个列表的柱形图"""
        if not self.ui.HAS_PLOTTING:
            messagebox.showerror("错误", "未安装 matplotlib, 请先安装")
            return
        
        if not self.ui.active_list:
            messagebox.showwarning("警告", "没有选中的列表")
            return
        
        values = self.ui.data_lists[self.ui.active_list]
        if not values:
            messagebox.showwarning("警告", f"{self.ui.active_list} 为空")
            return
        
        try:
            # 导入绘图库
            import matplotlib.pyplot as plt
            
            # 创建图表文件夹
            from data_manager import get_data_manager
            dm = get_data_manager()
            folder_path = dm.create_chart_folder(f"bar_chart_{self.ui.active_list.replace(' ', '_')}")
            
            # 绘制图表
            plt.figure(figsize=(10, 6))
            plt.bar(range(len(values)), values, color='steelblue', edgecolor='black')
            plt.xlabel('数据索引')
            plt.ylabel('值')
            plt.title(f'{self.ui.active_list} - 柱形图')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            # 保存图表
            chart_path = f"{folder_path}/chart.svg"
            plt.savefig(chart_path, format='svg')
            plt.show(block=False)
            
            # 保存数据和日志
            data = {
                "list_name": self.ui.active_list,
                "values": values,
                "count": len(values),
                "sum": sum(values),
                "average": sum(values) / len(values)
            }
            dm.save_chart_data(folder_path, data, method="Bar Chart")
            
            # 保存详细日志
            log_content = self._generate_log(self.ui.active_list, values)
            dm.save_log_file(folder_path, log_content)
            
            # messagebox.showinfo("绘图完成", f"已保存至: {folder_path}")
            
        except Exception as e:
            messagebox.showerror("绘图错误", f"错误: {e}")
    
    def _generate_log(self, list_name, values):
        """生成日志内容"""
        log = f"""
===== 柱形图统计信息 =====
时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
列表名称: {list_name}
统计方法: Bar Chart (柱形图)

===== 数据统计 =====
数据数量: {len(values)}
总和: {sum(values):.2f}
平均值: {sum(values) / len(values):.2f}
最大值: {max(values):.2f}
最小值: {min(values):.2f}

===== 原始数据 =====
{values}
"""
        return log
