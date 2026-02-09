"""
手动刷新按钮模块 - 在自动刷新失效时手动触发获取数据
"""
import tkinter as tk


class RefreshButton:
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None

    def create_button(self, parent):
        self.button = tk.Button(
            parent,
            text="刷新",
            command=self.manual_refresh,
            bg="#9C27B0",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=12
        )
        return self.button

    def manual_refresh(self):
        # 手动触发一次 fetch
        try:
            self.ui.fetch_data_btn.fetch_data()
        except Exception:
            # 作为兜底，直接调用主界面的刷新显示
            self.ui.selected_cells = self.ui.get_selected_cells()
            self.ui.update_display()
