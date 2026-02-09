# Excel 数据管理工具 - 更新说明

## 完成的功能需求

### 1. ✅ 分离按钮为独立模块
所有按钮逻辑已分离到 `buttons/` 目录：
- `fetch_data.py` - 获取数据按钮（自动创建列表）
- `clear_list.py` - 清空列表按钮
- `delete_list.py` - 删除列表按钮
- `sum_button.py` - 求和按钮
- `average_button.py` - 平均值按钮
- `plot_bar_chart.py` - 柱形图按钮
- `anova_button.py` - 方差分析(ANOVA)按钮
- `refresh_button.py` - 手动刷新按钮（新增）

### 2. ✅ 实现自动刷新功能（0.5秒间隔）
- `main.py` 中新增 `_auto_fetch()` 方法，每 0.5 秒自动检查 Excel 选区变化
- 使用 `tkinter.after()` 实现异步调度，避免阻塞 UI
- 智能避免重复添加相同选区数据（通过 `_last_fetched_key` 追踪）

### 3. ✅ 移除"添加列表"按钮
- 删除 `add_list()` 方法
- "获取数据"点击时自动创建新列表（如果没有或所有列表都为空）

### 4. ✅ 每次保存图片创建新文件夹及日志
- 新增 `data_manager.py` 模块管理所有保存文件
- `PlotBarChartButton` 和 `AnovaButton` 每次保存图表都创建独立文件夹
- 保存内容包括：
  - `chart.svg` 或 `anova_chart.svg` - 图表文件
  - `data.json` - 图表使用的数据和元信息
  - `log.txt` - 详细的统计信息和日志

### 5. ✅ 加入手动刷新按钮
- 新增 `RefreshButton` 模块（`buttons/refresh_button.py`）
- 在数据操作按钮行第4个位置：获取 / 清空 / 删除 / **刷新(手动)**

### 6. ✅ UI 配置文件（字体和大小）
- 新增 `ui_config.py` 配置文件
- 所有字体、大小、刷新间隔统一配置：
  ```python
  TITLE_FONT_SIZE = 14
  LISTBOX_FONT_SIZE = 14
  BUTTON_FONT_SIZE = 14
  TEXT_FONT_SIZE = 12
  AUTO_REFRESH_INTERVAL = 0.5  # 秒
  DEFAULT_FONT_FILE = "assets/JetBrainsMapleMono-Regular.ttf"
  ```
- 所有按钮已更新使用配置中的字体和大小

### 7. ✅ 默认字体配置
- `ui_config.py` 配置指向 `assets/JetBrainsMapleMono-Regular.ttf`
- UI 会尝试使用此字体，回退到 Arial（如果文件不存在）
- 创建了 `assets/` 目录（待添加字体文件）

## 项目结构

```
py_excel/
├── main.py                      # 主应用程序
├── ui_config.py                 # UI 配置文件（字体、大小、间隔）
├── data_manager.py              # 数据和文件管理模块
├── buttons/                     # 各个按钮的独立模块
│   ├── __init__.py
│   ├── fetch_data.py           # 获取数据（自动创建列表）
│   ├── clear_list.py           # 清空列表
│   ├── delete_list.py          # 删除列表
│   ├── sum_button.py           # 求和
│   ├── average_button.py       # 平均值
│   ├── plot_bar_chart.py       # 柱形图（带日志）
│   ├── anova_button.py         # 方差分析（带日志）
│   └── refresh_button.py       # 手动刷新
├── assets/                      # 字体资源目录
│   └── JetBrainsMapleMono-Regular.ttf (待添加)
├── output/                      # 图表和日志输出目录（自动创建）
│   └── bar_chart_列表1_20260209_120000/
│       ├── chart.svg
│       ├── data.json
│       └── log.txt
└── README_UPDATE.md            # 本文件
```

## 使用说明

### 快速启动
```bash
python main.py
```

### 工作流程
1. **在 Excel 中选择数据** → UI 自动显示选中的单元格（实时刷新）
2. **点击"获取数据"** → 自动创建新列表并添加数据（或在手动刷新按钮失效时使用）
3. **管理列表**：清空、删除列表
4. **分析数据**：求和、平均值、柱形图、ANOVA 分析
5. **查看结果**：每个图表都保存在独立文件夹，含数据和日志

### 配置修改
编辑 `ui_config.py` 可调整：
- 字体族名和大小
- 自动刷新间隔（默认 0.5 秒）
- 默认字体文件路径

### 字体配置
1. 将 `JetBrainsMapleMono-Regular.ttf` 放在 `assets/` 目录
2. 修改 `ui_config.py` 中的 `DEFAULT_FONT_FILE` 路径（如需）
3. 重启应用，UI 会自动尝试加载配置的字体

## 技术亮点

- **模块化设计**：每个按钮独立模块，易于维护和扩展
- **非阻塞自动刷新**：使用 `tkinter.after()` 异步调度，UI 流畅
- **智能重复检测**：避免相同数据重复添加
- **完整日志系统**：每次分析都保存数据和统计信息
- **灵活配置**：所有 UI 参数集中管理

## 依赖
- `tkinter` - 内置
- `win32com` - Excel 交互
- `matplotlib`、`seaborn` - 绘图（可选）
- `pandas`、`scipy` - 统计分析（可选）

