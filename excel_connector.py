"""
Excel 诊断和连接模块
"""
import win32com.client
import pythoncom
from logger import log_info, log_error, log_debug, log_exception


class ExcelConnector:
    """
    负责连接和获取 Excel 数据，提供诊断功能
    """
    
    def __init__(self):
        self.excel = None
        self.retry_count = 0
        self.max_retries = 3
    
    def _init_com(self):
        """
        初始化 COM（在多线程环境中必需）
        """
        try:
            pythoncom.CoInitialize()
            log_debug("COM 已初始化")
        except Exception as e:
            log_debug(f"COM 初始化: {e}")
    
    def get_excel_app(self):
        """
        尝试获取 Excel 应用实例，支持重试
        """
        try:
            self._init_com()  # 初始化 COM
            self.excel = win32com.client.GetActiveObject("Excel.Application")
            self.retry_count = 0
            log_info("✓ 已连接到 Excel 应用")
            return self.excel
        except Exception as e:
            self.retry_count += 1
            log_error(f"无法连接到 Excel（尝试 {self.retry_count}/{self.max_retries}）: {e}")
            return None
    
    def get_selected_cells(self):
        """
        获取 Excel 中选中的单元格数据，带完整错误处理
        """
        try:
            self._init_com()  # 初始化 COM
            
            # 尝试连接（如果未连接或连接失败）
            if self.excel is None or self.retry_count >= self.max_retries:
                self.excel = self.get_excel_app()
            
            if self.excel is None:
                log_error("Excel 应用未可用，无法获取选中数据")
                return None, "❌ Excel 应用未运行或无法访问"
            
            # 检查是否有活跃的工作簿
            try:
                active_workbook = self.excel.ActiveWorkbook
                log_debug(f"活跃工作簿: {active_workbook.Name}")
            except Exception as wb_e:
                log_error(f"无活跃工作簿: {wb_e}")
                return None, "❌ 没有打开的 Excel 工作簿"
            
            # 获取选中的范围
            selection = self.excel.Selection
            log_debug(f"选中对象类型: {type(selection)}")
            
            # 检查选中是否为空
            if selection is None:
                log_error("Selection 为 None")
                return None, "❌ 获取选择范围失败"
            
            cells_data = []
            
            # 检查是否是区域选择
            if hasattr(selection, 'Areas') and selection.Areas.Count > 0:
                log_debug(f"多区域选择: {selection.Areas.Count} 个区域")
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
                    # 尝试迭代单元格
                    cell_count = 0
                    for cell in selection:
                        cells_data.append({
                            'address': cell.Address,
                            'value': cell.Value,
                            'row': cell.Row,
                            'column': cell.Column
                        })
                        cell_count += 1
                    log_debug(f"单元格迭代成功: {cell_count} 个")
                except TypeError:
                    # 单个单元格的情况
                    log_debug("单个单元格模式")
                    cells_data.append({
                        'address': selection.Address,
                        'value': selection.Value,
                        'row': selection.Row,
                        'column': selection.Column
                    })
            
            if not cells_data:
                log_debug("未选中任何单元格")
                return [], "⚠️ 未选中任何单元格（请在 Excel 中选择数据）"
            
            log_info(f"✓ 成功获取 {len(cells_data)} 个单元格数据")
            return cells_data, None
            
        except Exception as e:
            log_exception("获取选中数据异常", e)
            return None, f"❌ 错误: {str(e)}"
    
    def diagnose(self):
        """
        诊断 Excel 连接状态
        """
        try:
            self._init_com()  # 初始化 COM
        except Exception:
            pass
        
        status = []
        
        # 检查 Excel 是否运行
        try:
            excel = win32com.client.GetActiveObject("Excel.Application")
            status.append("✓ Excel 应用已运行")
            
            # 检查工作簿
            try:
                wb = excel.ActiveWorkbook
                status.append(f"✓ 活跃工作簿: {wb.Name}")
            except Exception as e:
                status.append(f"❌ 工作簿: {e}")
            
            # 检查选择
            try:
                sel = excel.Selection
                if sel:
                    status.append(f"✓ 选择: {sel.Address} ({sel.Value})")
                else:
                    status.append("⚠️ 选择对象为空")
            except Exception as e:
                status.append(f"❌ 选择: {e}")
                
        except Exception as e:
            status.append(f"❌ Excel 应用: {e}")
        
        return "\n".join(status)
