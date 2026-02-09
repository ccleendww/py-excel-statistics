"""
删除列表按钮模块
"""
import tkinter as tk
from tkinter import messagebox


class DeleteListButton:
    """删除列表按钮"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="删除列表",
            command=self.delete_list,
            bg="#F44336",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button
    
    def delete_list(self):
        """删除激活列表"""
        if not self.ui.active_list:
            messagebox.showwarning("警告", "没有选中的列表")
            return
        
        if messagebox.askyesno("确认", f"确定要删除 {self.ui.active_list} 吗？"):
            del self.ui.data_lists[self.ui.active_list]
            self.ui.active_list = list(self.ui.data_lists.keys())[0] if self.ui.data_lists else None
            self.ui.update_list_display()
