#!/usr/bin/env python3
"""
Pythva插件基类和插件管理器
定义插件接口和插件系统核心功能
"""

import importlib
import inspect
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type
from pathlib import Path

from ..errors import PluginError, get_error_reporter
from ..config import PluginConfig


class Plugin(ABC):
    """插件基类"""

    def __init__(self, name: str, version: str = "1.0.0", description: str = ""):
        """初始化插件"""
        self.name = name
        self.version = version
        self.description = description
        self.enabled = True
        self.settings: Dict[str, Any] = {}

    @abstractmethod
    def activate(self) -> bool:
        """激活插件"""
        pass

    @abstractmethod
    def deactivate(self) -> bool:
        """停用插件"""
        pass

    def is_activated(self) -> bool:
        """检查插件是否已激活"""
        return self.enabled

    def get_info(self) -> Dict[str, str]:
        """获取插件信息"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'enabled': str(self.enabled)
        }

    def configure(self, settings: Dict[str, Any]):
        """配置插件"""
        self.settings.update(settings)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """获取插件设置"""
        return self.settings.get(key, default)


class ConversionPlugin(Plugin):
    """转换插件基类"""

    @abstractmethod
    def preprocess(self, code: str) -> str:
        """预处理代码"""
        return code

    @abstractmethod
    def postprocess(self, code: str) -> str:
        """后处理代码"""
        return code

    def transform_node(self, node) -> Optional[Any]:
        """转换AST节点（可选）"""
        return node


class PluginManager:
    """插件管理器"""

    def __init__(self, plugin_config: Optional[PluginConfig] = None):
        """初始化插件管理器"""
        self.plugin_config = plugin_config or PluginConfig()
        self.plugins: Dict[str, Plugin] = {}
        self.conversion_plugins: List[ConversionPlugin] = []
        self.error_reporter = get_error_reporter()

        # 加载插件
        self._load_plugins()

    def _load_plugins(self):
        """加载插件"""
        # 加载内置插件
        self._load_builtin_plugins()

        # 加载外部插件
        for plugin_path in self.plugin_config.plugin_paths:
            self._load_external_plugins(plugin_path)

    def _load_builtin_plugins(self):
        """加载内置插件"""
        try:
            from .builtin import get_builtin_plugins
            builtin_plugins = get_builtin_plugins()

            for plugin in builtin_plugins:
                self.register_plugin(plugin)

        except ImportError:
            pass

    def _load_external_plugins(self, plugin_path: str):
        """加载外部插件"""
        if not os.path.exists(plugin_path):
            return

        if os.path.isfile(plugin_path):
            self._load_plugin_from_file(plugin_path)
        elif os.path.isdir(plugin_path):
            self._load_plugins_from_directory(plugin_path)

    def _load_plugin_from_file(self, file_path: str):
        """从文件加载插件"""
        try:
            # 这里可以实现动态加载插件的逻辑
            pass
        except Exception as e:
            self.error_reporter.report_error(
                PluginError(f"无法加载插件文件 {file_path}: {e}")
            )

    def _load_plugins_from_directory(self, dir_path: str):
        """从目录加载插件"""
        plugins_dir = Path(dir_path)

        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue

            try:
                self._load_plugin_from_file(str(plugin_file))
            except Exception as e:
                self.error_reporter.report_error(
                    PluginError(f"无法加载插件 {plugin_file}: {e}")
                )

    def register_plugin(self, plugin: Plugin):
        """注册插件"""
        if plugin.name in self.plugins:
            self.error_reporter.report_warning(
                f"插件 '{plugin.name}' 已被注册，将被覆盖"
            )

        self.plugins[plugin.name] = plugin

        # 如果是转换插件，添加到转换插件列表
        if isinstance(plugin, ConversionPlugin):
            self.conversion_plugins.append(plugin)

        # 如果插件在启用列表中，激活它
        if plugin.name in self.plugin_config.enabled_plugins:
            self.enable_plugin(plugin.name)

    def unregister_plugin(self, plugin_name: str) -> bool:
        """注销插件"""
        if plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]

        # 停用插件
        if plugin.is_activated():
            plugin.deactivate()

        # 从列表中移除
        if plugin in self.conversion_plugins:
            self.conversion_plugins.remove(plugin)

        del self.plugins[plugin_name]
        return True

    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件"""
        if plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]

        if plugin.activate():
            plugin.enabled = True
            return True

        return False

    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件"""
        if plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]

        if plugin.deactivate():
            plugin.enabled = False
            return True

        return False

    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """获取插件"""
        return self.plugins.get(plugin_name)

    def get_all_plugins(self) -> Dict[str, Plugin]:
        """获取所有插件"""
        return self.plugins.copy()

    def get_conversion_plugins(self) -> List[ConversionPlugin]:
        """获取所有转换插件"""
        return [p for p in self.conversion_plugins if p.enabled]

    def list_plugins(self) -> List[Dict[str, str]]:
        """列出所有插件信息"""
        return [plugin.get_info() for plugin in self.plugins.values()]

    def preprocess_code(self, code: str) -> str:
        """预处理代码"""
        for plugin in self.get_conversion_plugins():
            try:
                code = plugin.preprocess(code)
            except Exception as e:
                self.error_reporter.report_error(
                    PluginError(f"插件 {plugin.name} 预处理失败: {e}")
                )

        return code

    def postprocess_code(self, code: str) -> str:
        """后处理代码"""
        for plugin in self.get_conversion_plugins():
            try:
                code = plugin.postprocess(code)
            except Exception as e:
                self.error_reporter.report_error(
                    PluginError(f"插件 {plugin.name} 后处理失败: {e}")
                )

        return code

    def reload_plugins(self):
        """重新加载所有插件"""
        # 清空现有插件
        for plugin in self.plugins.values():
            if plugin.is_activated():
                plugin.deactivate()

        self.plugins.clear()
        self.conversion_plugins.clear()

        # 重新加载
        self._load_plugins()


# 全局插件管理器
_global_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """获取全局插件管理器"""
    global _global_plugin_manager
    if _global_plugin_manager is None:
        _global_plugin_manager = PluginManager()
    return _global_plugin_manager


def register_plugin(plugin: Plugin):
    """注册插件到全局管理器"""
    get_plugin_manager().register_plugin(plugin)


def get_conversion_plugins() -> List[ConversionPlugin]:
    """获取所有启用的转换插件"""
    return get_plugin_manager().get_conversion_plugins()