"""
平均值按钮模块
"""
import tkinter as tk
from tkinter import messagebox


class AverageButton:
    """平均值按钮"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="平均值",
            command=self.calculate_average,
            bg="#00BCD4",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button
    
    def calculate_average(self):
        """计算激活列表的平均值"""
        if not self.ui.active_list:
            messagebox.showwarning("警告", "没有选中的列表")
            return
        
        values = self.ui.data_lists[self.ui.active_list]
        if not values:
            messagebox.showwarning("警告", f"{self.ui.active_list} 为空")
            return
        
        avg = sum(values) / len(values)
        messagebox.showinfo("平均值结果", f"{self.ui.active_list} 的平均值: {avg:.2f}")
