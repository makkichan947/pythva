#!/usr/bin/env python3
"""
Pythva - 将Python代码转换为Java风格的语法
"""

from .core import convert_python_to_java_style
from .mapper import convert_with_mapping, SyntaxMapper
from .config import get_conversion_config, ConfigManager
from .errors import get_error_reporter, ConversionError
from .optimizer import convert_with_optimization, get_optimized_converter
from .plugins import get_plugin_manager, register_plugin

__version__ = "5.0.0"
__author__ = "Yaku Makki"

__all__ = [
    # 核心功能
    'convert_python_to_java_style',
    'convert_with_mapping',
    'SyntaxMapper',

    # 配置管理
    'get_conversion_config',
    'ConfigManager',

    # 错误处理
    'get_error_reporter',
    'ConversionError',

    # 性能优化
    'convert_with_optimization',
    'get_optimized_converter',

    # 插件系统
    'get_plugin_manager',
    'register_plugin',
]