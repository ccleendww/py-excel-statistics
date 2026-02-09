"""
清空列表按钮模块
"""
import tkinter as tk
from tkinter import messagebox


class ClearListButton:
    """清空列表按钮"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="清空列表",
            command=self.clear_list,
            bg="#FF9800",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button
    
    def clear_list(self):
        """清空激活列表"""
        if not self.ui.active_list:
            messagebox.showwarning("警告", "没有选中的列表")
            return
        
        if messagebox.askyesno("确认", f"确定要清空 {self.ui.active_list} 吗？"):
            self.ui.data_lists[self.ui.active_list] = []
            self.ui.update_list_display()
