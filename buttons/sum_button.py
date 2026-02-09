"""
求和按钮模块
"""
import tkinter as tk
from tkinter import messagebox


class SumButton:
    """求和按钮"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="求和",
            command=self.calculate_sum,
            bg="#673AB7",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button
    
    def calculate_sum(self):
        """计算激活列表的和"""
        if not self.ui.active_list:
            messagebox.showwarning("警告", "没有选中的列表")
            return
        
        values = self.ui.data_lists[self.ui.active_list]
        if not values:
            messagebox.showwarning("警告", f"{self.ui.active_list} 为空")
            return
        
        total = sum(values)
        messagebox.showinfo("求和结果", f"{self.ui.active_list} 的和: {total:.2f}")
