"""
方差分析(ANOVA)按钮模块
"""
import tkinter as tk
from tkinter import messagebox
import datetime


class AnovaButton:
    """方差分析(ANOVA)按钮"""
    
    def __init__(self, parent_ui):
        self.ui = parent_ui
        self.button = None
    
    def create_button(self, parent):
        """创建按钮"""
        self.button = tk.Button(
            parent,
            text="方差分析(ANOVA)",
            command=self.perform_anova,
            bg="#E91E63",
            fg="white",
            font=(self.ui.config_font_family(), self.ui.config.BUTTON_FONT_SIZE),
            width=15
        )
        return self.button
    
    def perform_anova(self):
        """执行单因素方差分析"""
        if not self.ui.HAS_SCIPY:
            messagebox.showerror("错误", "未安装 pandas/scipy, 请先安装")
            return
        
        list_names = list(self.ui.data_lists.keys())
        active_lists = [name for name in list_names if self.ui.data_lists[name]]
        
        if len(active_lists) < 2:
            messagebox.showwarning("警告", "需要至少两个非空列表来进行方差分析")
            return
        
        try:
            import numpy as np
            from scipy import stats
            import matplotlib.pyplot as plt
            from data_manager import get_data_manager
            
            # 准备数据
            all_data = [self.ui.data_lists[name] for name in active_lists]
            
            # 执行单因素方差分析
            f_stat, p_value = stats.f_oneway(*all_data)
            
            # 计算均值和标准差
            means = [np.mean(data) for data in all_data]
            stds = [np.std(data) for data in all_data]
            standard_errors = [std / np.sqrt(len(data)) for std, data in zip(stds, all_data)]
            
            # 结果信息
            result_text = f"单因素方差分析 (ANOVA) 结果\n"
            result_text += "=" * 50 + "\n"
            result_text += f"F 统计量: {f_stat:.4f}\n"
            result_text += f"P 值: {p_value:.6f}\n"
            result_text += "=" * 50 + "\n"
            
            if p_value < 0.05:
                result_text += "结论: 组间存在显著差异 (p < 0.05)\n"
            else:
                result_text += "结论: 组间无显著差异 (p >= 0.05)\n"
            
            result_text += "=" * 50 + "\n"
            result_text += "各组统计量:\n"
            for name, mean, std in zip(active_lists, means, stds):
                result_text += f"{name}: 均值={mean:.4f}, 标准差={std:.4f}\n"
            
            messagebox.showinfo("ANOVA 分析结果", result_text)
            
            # 创建图表文件夹
            dm = get_data_manager()
            folder_path = dm.create_chart_folder("anova_analysis")
            
            # 绘制带误差线的条形图
            self._plot_anova_bars(active_lists, means, standard_errors, folder_path)
            
            # 保存数据
            data = {
                "method": "ANOVA",
                "f_statistic": float(f_stat),
                "p_value": float(p_value),
                "lists": active_lists,
                "means": [float(m) for m in means],
                "stds": [float(s) for s in stds],
                "significant": "Yes" if p_value < 0.05 else "No"
            }
            dm.save_chart_data(folder_path, data, method="ANOVA")
            
            # 保存详细日志
            log_content = self._generate_log(active_lists, means, stds, f_stat, p_value)
            dm.save_log_file(folder_path, log_content)
            
            # messagebox.showinfo("分析完成", f"已保存至: {folder_path}")
            
        except Exception as e:
            messagebox.showerror("分析错误", f"错误: {e}")
    
    def _plot_anova_bars(self, labels, means, errors, folder_path):
        """绘制带误差线的条形图"""
        if not self.ui.HAS_PLOTTING:
            return
        
        try:
            import numpy as np
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 6))
            x_pos = np.arange(len(labels))
            plt.bar(x_pos, means, yerr=errors, capsize=10, color='steelblue', 
                    edgecolor='black', error_kw={'elinewidth': 2, 'capthick': 2})
            plt.xticks(x_pos, labels, rotation=0)
            plt.ylabel('均值')
            plt.title('各组均值对比 (带标准误差线)')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            chart_path = f"{folder_path}/anova_chart.svg"
            plt.savefig(chart_path, format='svg')
            plt.show(block=False)
            
        except Exception as e:
            messagebox.showerror("绘图错误", f"错误: {e}")
    
    def _generate_log(self, active_lists, means, stds, f_stat, p_value):
        """生成日志内容"""
        log = f"""
===== 方差分析(ANOVA)统计信息 =====
时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
统计方法: 单因素方差分析 (One-way ANOVA)

===== 分析结果 =====
F 统计量: {f_stat:.6f}
P 值: {p_value:.8f}
显著性水平 (α): 0.05
结论: {'组间存在显著差异 (p < 0.05)' if p_value < 0.05 else '组间无显著差异 (p >= 0.05)'}

===== 各组统计量 =====
"""
        for name, mean, std in zip(active_lists, means, stds):
            log += f"{name}:\n  - 均值: {mean:.6f}\n  - 标准差: {std:.6f}\n"
        
        return log
