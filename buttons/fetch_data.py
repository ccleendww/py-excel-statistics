"""
获取数据按钮模块 - 自动创建列表
"""
import tkinter as tk
from tkinter import messagebox


class FetchDataButton:
    """获取数据按钮 - 自动创建列表的功能"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="获取数据",
            command=self.fetch_data,
            bg="#2196F3",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button
    
    def fetch_data(self):
        """获取当前选中的数据并创建新列表添加数据"""
        if not self.ui.selected_cells:
            messagebox.showwarning("警告", "没有选中任何单元格")
            return
        
        # 提取数值
        values = []
        for cell in self.ui.selected_cells:
            val = cell['value']
            if val is not None and isinstance(val, (int, float)):
                values.append(float(val))
        
        if not values:
            messagebox.showwarning("警告", "选中的单元格中没有数值数据")
            return
        
        # 总是创建新列表
        self.ui.list_counter += 1
        list_name = f"列表 {self.ui.list_counter}"
        self.ui.data_lists[list_name] = values
        self.ui.active_list = list_name
        self.ui.update_list_display()
