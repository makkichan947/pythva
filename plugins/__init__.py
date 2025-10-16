#!/usr/bin/env python3
"""
Pythva插件系统
提供插件管理和扩展功能
"""

from .base import Plugin, PluginManager, get_plugin_manager, register_plugin
from .builtin import *

__all__ = ['Plugin', 'PluginManager', 'get_plugin_manager', 'register_plugin']