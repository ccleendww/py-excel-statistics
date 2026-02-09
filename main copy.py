import win32com.client
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

HAS_PLOTTING = False
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    # 设置样式（可选）
    sns.set_theme(style="whitegrid")
    HAS_PLOTTING = True
except Exception:
    plt = None
    sns = None

class ExcelMonitorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel 单元格监听器")
        self.root.geometry("600x500")
        self.excel = None
        self.selected_cells = []
        self.running = True
        
        # 创建UI组件
        self.setup_ui()
        
        # 启动后台线程监听Excel
        self.monitor_thread = threading.Thread(target=self.monitor_excel_selection, daemon=True)
        self.monitor_thread.start()
        
        # 处理窗口关闭
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """设置UI界面"""
        # 标题
        title_label = tk.Label(self.root, text="Excel 选中单元格数据显示", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # 信息框架
        info_frame = ttk.LabelFrame(self.root, text="选中的单元格信息", padding=10)
        info_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        # 用于显示数据的文本框
        scrollbar = ttk.Scrollbar(info_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.data_text = tk.Text(info_frame, height=15, width=60, yscrollcommand=scrollbar.set)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.data_text.yview)
        
        # 按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # 计算按钮
        self.sum_button = tk.Button(button_frame, text="求和", command=self.calculate_sum, 
                                     bg="#4CAF50", fg="white", font=("Arial", 10), width=12)
        self.sum_button.grid(row=0, column=0, padx=5)
        
        self.avg_button = tk.Button(button_frame, text="平均值", command=self.calculate_average,
                                     bg="#2196F3", fg="white", font=("Arial", 10), width=12)
        self.avg_button.grid(row=0, column=1, padx=5)
        
        self.count_button = tk.Button(button_frame, text="计数", command=self.calculate_count,
                                       bg="#FF9800", fg="white", font=("Arial", 10), width=12)
        self.count_button.grid(row=0, column=2, padx=5)
        
        self.refresh_button = tk.Button(button_frame, text="刷新", command=self.refresh_data,
                                         bg="#9C27B0", fg="white", font=("Arial", 10), width=12)
        self.refresh_button.grid(row=0, column=3, padx=5)
        
        self.plot_button = tk.Button(button_frame, text="柱形图", command=self.plot_bar_chart,
                         bg="#607D8B", fg="white", font=("Arial", 10), width=12)
        self.plot_button.grid(row=0, column=4, padx=5)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="正在监听 Excel...", fg="green", font=("Arial", 10))
        self.status_label.pack(pady=5)
    
    def get_selected_cells(self):
        """获取Excel中选中的所有单元格"""
        try:
            self.excel = win32com.client.GetActiveObject("Excel.Application")
            selection = self.excel.Selection
            
            cells_data = []
            
            # 检查是否是区域选择
            if hasattr(selection, 'Areas'):
                # 多个区域选择
                for area in selection.Areas:
                    for cell in area:
                        cells_data.append({
                            'address': cell.Address,
                            'value': cell.Value,
                            'row': cell.Row,
                            'column': cell.Column
                        })
            else:
                # 单个或连续区域选择
                try:
                    for cell in selection:
                        cells_data.append({
                            'address': cell.Address,
                            'value': cell.Value,
                            'row': cell.Row,
                            'column': cell.Column
                        })
                except TypeError:
                    # 单个单元格
                    cells_data.append({
                        'address': selection.Address,
                        'value': selection.Value,
                        'row': selection.Row,
                        'column': selection.Column
                    })
            
            return cells_data
            
        except Exception as e:
            return []
    
    def monitor_excel_selection(self):
        """后台线程监听Excel选择变化"""
        last_selection = None
        
        while self.running:
            try:
                current_selection = self.get_selected_cells()
                
                # 如果选择发生了变化，更新UI
                if current_selection != last_selection:
                    self.selected_cells = current_selection
                    self.root.after(0, self.update_display)
                    last_selection = current_selection
                    
                    if current_selection:
                        self.root.after(0, lambda: self.status_label.config(text="✓ 已检测到选中的单元格", fg="green"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text="✗ 无法连接到 Excel", fg="red"))
            
            time.sleep(0.5)  # 每500毫秒检查一次
    
    def update_display(self):
        """更新显示面板"""
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        
        if not self.selected_cells:
            self.data_text.insert(tk.END, "未选中任何单元格")
            self.data_text.config(state=tk.DISABLED)
            return
        
        # 显示选中单元格信息
        display_text = f"选中单元格数量: {len(self.selected_cells)}\n"
        display_text += "=" * 50 + "\n\n"
        
        for i, cell in enumerate(self.selected_cells, 1):
            display_text += f"单元格 {i}:\n"
            display_text += f"  地址: {cell['address']}\n"
            display_text += f"  值: {cell['value']}\n"
            display_text += f"  行列: 行 {cell['row']}, 列 {cell['column']}\n"
            display_text += "-" * 50 + "\n"
        
        self.data_text.insert(tk.END, display_text)
        self.data_text.config(state=tk.DISABLED)
    
    def calculate_sum(self):
        """计算所有选中单元格的和"""
        if not self.selected_cells:
            messagebox.showwarning("警告", "没有选中任何单元格")
            return
        
        try:
            total = sum(float(cell['value']) for cell in self.selected_cells 
                       if cell['value'] is not None and isinstance(cell['value'], (int, float)))
            messagebox.showinfo("求和结果", f"选中数值单元格的和: {total:.2f}")
        except ValueError:
            messagebox.showerror("错误", "存在无法转换为数字的值")
    
    def calculate_average(self):
        """计算所有选中单元格的平均值"""
        if not self.selected_cells:
            messagebox.showwarning("警告", "没有选中任何单元格")
            return
        
        try:
            values = [float(cell['value']) for cell in self.selected_cells 
                     if cell['value'] is not None and isinstance(cell['value'], (int, float))]
            if not values:
                messagebox.showerror("错误", "没有可计算的数值")
                return
            
            avg = sum(values) / len(values)
            messagebox.showinfo("平均值结果", f"选中数值单元格的平均值: {avg:.2f}")
        except ValueError:
            messagebox.showerror("错误", "存在无法转换为数字的值")
    
    def calculate_count(self):
        """计算选中单元格的数量"""
        if not self.selected_cells:
            messagebox.showwarning("警告", "没有选中任何单元格")
            return
        
        total_count = len(self.selected_cells)
        value_count = len([c for c in self.selected_cells if c['value'] is not None])
        messagebox.showinfo("计数结果", f"总单元格数: {total_count}\n含有数据的单元格: {value_count}")
    
    def refresh_data(self):
        """手动刷新获取选中的数据"""
        self.selected_cells = self.get_selected_cells()
        self.update_display()
        
        if self.selected_cells:
            # messagebox.showinfo("刷新成功", f"已获取 {len(self.selected_cells)} 个选中的单元格")
            pass
        else:
            messagebox.showinfo("刷新成功", "未检测到选中的单元格")

    def plot_bar_chart(self):
        """使用选中数据绘制柱形图并保存为 SVG"""
        if not self.selected_cells:
            messagebox.showwarning("警告", "没有选中任何单元格")
            return

        # 只使用数值类型的数据进行绘图
        labels = []
        values = []
        for cell in self.selected_cells:
            val = cell['value']
            if val is None:
                continue
            if isinstance(val, (int, float)):
                labels.append(cell['address'])
                values.append(float(val))

        if not values:
            messagebox.showerror("错误", "没有可用于绘图的数值单元格")
            return

        try:
            plt.figure(figsize=(max(6, len(values)*0.6), 4))
            sns.barplot(x=labels, y=values, palette="viridis")
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('单元格')
            plt.ylabel('值')
            plt.title('选中单元格柱形图')
            plt.tight_layout()
            



            # 生成带时间戳的文件名，避免覆盖
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"excel_selection_plot_{timestamp}.svg"
            plt.savefig(filename, format='svg')
            # plt.close()
            plt.show(block=False)

            # messagebox.showinfo("绘图完成", f"柱形图已保存为: {filename}")
        except Exception as e:
            messagebox.showerror("绘图错误", f"绘图或保存时出错: {e}")
    
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