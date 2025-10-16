#!/usr/bin/env python3
"""
Pythva错误处理和调试模块
提供统一的错误处理、日志记录和调试功能
"""

import sys
import traceback
import logging
from typing import Optional, Dict, Any, List
from enum import Enum
from pathlib import Path


class ErrorSeverity(Enum):
    """错误严重程度"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ConversionError(Exception):
    """转换错误基类"""

    def __init__(self, message: str, line_number: Optional[int] = None,
                 column: Optional[int] = None, file_path: Optional[str] = None):
        super().__init__(message)
        self.line_number = line_number
        self.column = column
        self.file_path = file_path

    def __str__(self):
        location = ""
        if self.file_path:
            location += f"文件: {self.file_path}"
        if self.line_number:
            location += f", 行: {self.line_number}"
        if self.column:
            location += f", 列: {self.column}"

        if location:
            return f"{self.args[0]} ({location})"
        return self.args[0]


class SyntaxError(ConversionError):
    """语法错误"""
    pass


class TypeInferenceError(ConversionError):
    """类型推断错误"""
    pass


class ImportError(ConversionError):
    """导入错误"""
    pass


class PluginError(ConversionError):
    """插件错误"""
    pass


class ConfigurationError(ConversionError):
    """配置错误"""
    pass


class ErrorReporter:
    """错误报告器"""

    def __init__(self, debug_mode: bool = False, verbose: bool = False):
        """初始化错误报告器"""
        self.debug_mode = debug_mode
        self.verbose = verbose
        self.errors: List[ConversionError] = []
        self.warnings: List[str] = []

        # 配置日志
        self._setup_logging()

    def _setup_logging(self):
        """设置日志记录"""
        log_level = logging.DEBUG if self.debug_mode else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stderr)
            ]
        )
        self.logger = logging.getLogger('pythva')

    def report_error(self, error: ConversionError, severity: ErrorSeverity = ErrorSeverity.ERROR):
        """报告错误"""
        self.errors.append(error)

        if severity == ErrorSeverity.DEBUG and not self.debug_mode:
            return

        if severity == ErrorSeverity.CRITICAL:
            self.logger.critical(str(error))
        elif severity == ErrorSeverity.ERROR:
            self.logger.error(str(error))
        elif severity == ErrorSeverity.WARNING:
            self.logger.warning(str(error))
        elif severity == ErrorSeverity.INFO:
            self.logger.info(str(error))
        else:
            self.logger.debug(str(error))

    def report_warning(self, message: str, line_number: Optional[int] = None,
                      file_path: Optional[str] = None):
        """报告警告"""
        warning = f"警告: {message}"
        if file_path:
            warning += f" (文件: {file_path}"
        if line_number:
            warning += f", 行: {line_number}"
        if file_path or line_number:
            warning += ")"

        self.warnings.append(warning)
        self.logger.warning(warning)

    def report_info(self, message: str):
        """报告信息"""
        if self.verbose:
            self.logger.info(message)

    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0

    def has_critical_errors(self) -> bool:
        """是否有严重错误"""
        return any(
            ErrorSeverity.ERROR in str(error) or ErrorSeverity.CRITICAL in str(error)
            for error in self.errors
        )

    def get_error_summary(self) -> str:
        """获取错误摘要"""
        if not self.errors:
            return "无错误"

        summary = f"总共 {len(self.errors)} 个错误"
        if self.warnings:
            summary += f", {len(self.warnings)} 个警告"

        return summary

    def print_detailed_report(self):
        """打印详细错误报告"""
        print("\n" + "="*50)
        print("PYTHVA 转换报告")
        print("="*50)

        if self.errors:
            print(f"\n错误 ({len(self.errors)} 个):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print(f"\n警告 ({len(self.warnings)} 个):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        print(f"\n{self.get_error_summary()}")
        print("="*50)

    def save_report(self, file_path: str):
        """保存错误报告到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("PYTHVA 转换报告\n")
            f.write("="*50 + "\n")

            if self.errors:
                f.write(f"\n错误 ({len(self.errors)} 个):\n")
                for i, error in enumerate(self.errors, 1):
                    f.write(f"  {i}. {error}\n")

            if self.warnings:
                f.write(f"\n警告 ({len(self.warnings)} 个):\n")
                for i, warning in enumerate(self.warnings, 1):
                    f.write(f"  {i}. {warning}\n")

            f.write(f"\n{self.get_error_summary()}\n")


class DebugTracer:
    """调试跟踪器"""

    def __init__(self, enabled: bool = False):
        """初始化调试跟踪器"""
        self.enabled = enabled
        self.trace_data: List[Dict[str, Any]] = []

    def trace(self, event: str, node_type: str = "", details: Dict[str, Any] = None):
        """添加跟踪信息"""
        if not self.enabled:
            return

        trace_info = {
            'event': event,
            'node_type': node_type,
            'details': details or {},
            'line_number': traceback.extract_stack()[-2].lineno
        }

        self.trace_data.append(trace_info)

    def get_trace_report(self) -> str:
        """获取跟踪报告"""
        if not self.trace_data:
            return "无跟踪信息"

        report = "调试跟踪报告:\n"
        for i, trace in enumerate(self.trace_data, 1):
            report += f"  {i}. {trace['event']}"
            if trace['node_type']:
                report += f" ({trace['node_type']})"
            if trace['details']:
                report += f" - {trace['details']}"
            report += f" (行: {trace['line_number']})\n"

        return report

    def save_trace(self, file_path: str):
        """保存跟踪信息到文件"""
        import json
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.trace_data, f, indent=2, ensure_ascii=False)


def handle_conversion_error(error: Exception, reporter: ErrorReporter,
                          context: Optional[str] = None):
    """统一错误处理"""
    if isinstance(error, ConversionError):
        reporter.report_error(error)
    else:
        # 未知错误
        message = f"未知错误: {str(error)}"
        if context:
            message += f" (上下文: {context})"

        conversion_error = ConversionError(message)
        reporter.report_error(conversion_error, ErrorSeverity.ERROR)


def create_syntax_error(message: str, line_number: Optional[int] = None,
                       file_path: Optional[str] = None) -> SyntaxError:
    """创建语法错误"""
    return SyntaxError(message, line_number, file_path=file_path)


def create_type_error(message: str, line_number: Optional[int] = None,
                     file_path: Optional[str] = None) -> TypeInferenceError:
    """创建类型推断错误"""
    return TypeInferenceError(message, line_number, file_path=file_path)


# 全局错误报告器
_global_reporter: Optional[ErrorReporter] = None


def get_error_reporter() -> ErrorReporter:
    """获取全局错误报告器"""
    global _global_reporter
    if _global_reporter is None:
        _global_reporter = ErrorReporter()
    return _global_reporter


def reset_error_reporter():
    """重置全局错误报告器"""
    global _global_reporter
    _global_reporter = ErrorReporter()


if __name__ == "__main__":
    # 测试错误处理
    reporter = ErrorReporter(debug_mode=True, verbose=True)

    # 测试不同类型的错误
    syntax_error = create_syntax_error("无效的语法", line_number=10, file_path="test.py")
    reporter.report_error(syntax_error)

    type_error = create_type_error("无法推断类型", line_number=20)
    reporter.report_error(type_error)

    reporter.report_warning("这只是一个警告", line_number=15)

    reporter.print_detailed_report()