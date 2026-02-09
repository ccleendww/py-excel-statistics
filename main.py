from tkinter import font
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from collections import defaultdict
import datetime

# 导入按钮模块
from buttons.fetch_data import FetchDataButton
from buttons.clear_list import ClearListButton
from buttons.delete_list import DeleteListButton
from buttons.sum_button import SumButton
from buttons.average_button import AverageButton
from buttons.plot_bar_chart import PlotBarChartButton
from buttons.anova_button import AnovaButton
from buttons.refresh_button import RefreshButton

import ui_config as config
from excel_connector import ExcelConnector
from logger import log_info, log_error, log_debug

HAS_PLOTTING = False
HAS_SCIPY = False


try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.backends.backend_svg
    sns.set_theme(style="whitegrid")
    HAS_PLOTTING = True
except Exception:
    plt = None
    sns = None

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
    HAS_SCIPY = True
except Exception:
    pd = None
    np = None
    stats = None


class ExcelMonitorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel 数据管理工具")
        self.root.geometry("800x700")
        self.excel_connector = ExcelConnector()  # 使用新的连接器
        self.selected_cells = []
        self.running = True
        
        # 数据列表管理：{list_name: [values]}
        self.data_lists = {}
        self.list_counter = 0
        self.active_list = None
        
        # 条件标志
        self.HAS_PLOTTING = HAS_PLOTTING
        self.HAS_SCIPY = HAS_SCIPY
        
        # 配置引用
        self.config = config

        # 创建按钮实例
        self.fetch_data_btn = FetchDataButton(self)
        self.clear_list_btn = ClearListButton(self)
        self.delete_list_btn = DeleteListButton(self)
        self.sum_btn = SumButton(self)
        self.avg_btn = AverageButton(self)
        self.plot_btn = PlotBarChartButton(self)
        self.anova_btn = AnovaButton(self)
        self.refresh_btn = RefreshButton(self)
        
        # 创建UI组件
        self.setup_ui()
        
        # 启动后台线程监听Excel
        self.monitor_thread = threading.Thread(target=self.monitor_excel_selection, daemon=True)
        self.monitor_thread.start()

        # 用于避免重复更新UI显示的同一选择
        self._last_selected_for_display = None
        # 启动自动刷新（0.5s 间隔，配置可在 ui_config 中调整）
        self.start_auto_fetch()
        
        # 处理窗口关闭
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """设置UI界面"""
        # 标题
        # 使用配置的字体族和大小（回退到 Arial）
        try:
            title_font_family = self.config_font_family()
            title_font_size = getattr(self.config, 'TITLE_FONT_SIZE', 14)
            title_label = tk.Label(self.root, text="Excel 数据管理工具", font=(title_font_family, title_font_size, "bold"))
        except Exception:
            title_label = tk.Label(self.root, text="Excel 数据管理工具", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        default_font = font.Font(family=title_font_family if 'title_font_family' in locals() else 'Arial', size=getattr(self.config, 'TEXT_FONT_SIZE', 12))
        
        # 主容器（上下分割）
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== 上半部分：当前选中的单元格信息 =====
        info_frame = ttk.LabelFrame(main_container, text="当前选中的单元格", padding=10)
        info_frame.pack(fill=tk.BOTH, padx=0, pady=(0, 10), expand=False, side=tk.TOP)
        
        scrollbar = ttk.Scrollbar(info_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.data_text = tk.Text(info_frame, height=8, width=80, yscrollcommand=scrollbar.set)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.data_text.yview)
        
        # ===== 中间部分：数据列表管理 =====
        list_frame = ttk.LabelFrame(main_container, text="数据列表", padding=10)
        list_frame.pack(fill=tk.BOTH, padx=0, pady=(0, 10), expand=True, side=tk.TOP)
        
        # 列表展示（Listbox）
        scrollbar_list = ttk.Scrollbar(list_frame)
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        
        list_font = (self.config_font_family(), getattr(self.config, 'LISTBOX_FONT_SIZE', 14))
        self.list_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar_list.set, font=list_font)
        self.list_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar_list.config(command=self.list_listbox.yview)
        self.list_listbox.bind('<<ListboxSelect>>', self.on_list_select)
        
        # ===== 按钮框架 1：数据操作按钮 =====
        button_frame1 = ttk.Frame(self.root)
        button_frame1.pack(pady=5)
        
        # 列顺: 获取 / 清空 / 删除 / 刷新(手动)
        self.fetch_data_btn.create_button(button_frame1).grid(row=0, column=0, padx=5)
        self.clear_list_btn.create_button(button_frame1).grid(row=0, column=1, padx=5)
        self.delete_list_btn.create_button(button_frame1).grid(row=0, column=2, padx=5)
        self.refresh_btn.create_button(button_frame1).grid(row=0, column=3, padx=5)
        
        # ===== 按钮框架 2：分析和计算按钮 =====
        button_frame2 = ttk.Frame(self.root)
        button_frame2.pack(pady=5)
        
        self.sum_btn.create_button(button_frame2).grid(row=0, column=0, padx=5)
        self.avg_btn.create_button(button_frame2).grid(row=0, column=1, padx=5)
        self.plot_btn.create_button(button_frame2).grid(row=0, column=2, padx=5)
        self.anova_btn.create_button(button_frame2).grid(row=0, column=3, padx=5)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="正在监听 Excel...", fg="green", font=("Arial", 14))
        self.status_label.pack(pady=5)
    
    
    def on_list_select(self, event):
        """当选择列表时"""
        selection = self.list_listbox.curselection()
        if selection:
            index = selection[0]
            list_names = list(self.data_lists.keys())
            self.active_list = list_names[index]
            self.update_list_display()
    def config_font_family(self):
        """返回配置中首选字体族名（回退到 Arial）"""
        try:
            fam = getattr(self.config, 'DEFAULT_FONT_FAMILY', None)
            if fam:
                return fam
        except Exception:
            pass
        return "Arial"
    
    def update_list_display(self):
        """更新列表显示"""
        self.list_listbox.delete(0, tk.END)
        
        for list_name, values in self.data_lists.items():
            marker = ">> " if list_name == self.active_list else "   "
            display_text = f"{marker}{list_name}: {len(values)} 个数据 {values[:5]}"
            if len(values) > 5:
                display_text += f"... (总计: {len(values)})"
            self.list_listbox.insert(tk.END, display_text)
    
    def get_selected_cells(self):
        """获取Excel中选中的所有单元格"""
        cells_data, error_msg = self.excel_connector.get_selected_cells()
        if error_msg:
            log_error(error_msg)
        return cells_data if cells_data is not None else []
    
    def monitor_excel_selection(self):
        """后台线程监听Excel选择变化"""
        last_selection = None
        error_count = 0
        
        while self.running:
            try:
                current_selection = self.get_selected_cells()
                
                # 如果选择发生了变化，更新UI
                if current_selection != last_selection:
                    self.selected_cells = current_selection
                    self.root.after(0, self.update_display)
                    last_selection = current_selection
                    
                    if current_selection:
                        self.root.after(0, lambda: self.status_label.config(
                            text="✓ 已检测到选中的单元格", fg="green"))
                        error_count = 0
                    
            except Exception as e:
                error_count += 1
                log_error(f"监听线程错误({error_count}): {e}")
                if error_count > 5:
                    self.root.after(0, lambda: self.status_label.config(
                        text="✗ 无法连接到 Excel（详见日志）", fg="red"))
                    error_count = 0
            
            time.sleep(0.5)  # 每500毫秒检查一次

    def start_auto_fetch(self):
        """使用 tkinter 的 after 启动自动抓取循环"""
        interval_ms = int(getattr(self.config, 'AUTO_REFRESH_INTERVAL', 0.5) * 1000)
        try:
            self.root.after(interval_ms, self._auto_fetch)
        except Exception:
            pass

    def _auto_fetch(self):
        """自动刷新：检查Excel选择变化并更新UI显示（不自动创建列表）"""
        try:
            # 获取当前选择
            current_selection = self.get_selected_cells()
            
            # 如果选择发生了变化，更新UI显示
            if current_selection != self._last_selected_for_display:
                self.selected_cells = current_selection
                self.root.after(0, self.update_display)
                self._last_selected_for_display = current_selection
            # 继续循环
        except Exception as e:
            log_debug(f"自动刷新错误: {e}")
        finally:
            interval_ms = int(getattr(self.config, 'AUTO_REFRESH_INTERVAL', 0.5) * 1000)
            try:
                self.root.after(interval_ms, self._auto_fetch)
            except Exception:
                pass
    
    def update_display(self):
        """更新显示面板"""
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        
        if not self.selected_cells:
            # 没有选中数据时，显示诊断信息
            diagnostic = self.excel_connector.diagnose()
            display_text = "未选中任何单元格\n\n诊断信息:\n" + diagnostic
            self.data_text.insert(tk.END, display_text)
            self.data_text.config(state=tk.DISABLED)
            return
        
        display_text = f"选中单元格数量: {len(self.selected_cells)}\n"
        display_text += "=" * 50 + "\n"
        
        for i, cell in enumerate(self.selected_cells, 1):
            display_text += f"地址: {cell['address']} | 值: {cell['value']}\n"
        
        self.data_text.insert(tk.END, display_text)
        self.data_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        """处理窗口关闭"""
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ExcelMonitorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()