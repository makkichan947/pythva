#!/usr/bin/env python3
"""
Pythva配置文件管理
提供配置加载、验证和管理的功能
"""

import json
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class ConversionConfig:
    """转换配置类"""

    # 输出设置
    output_style: str = "java"  # java, compact, verbose
    add_package_declaration: bool = True
    package_name: str = "pythva.generated"

    # 类型映射
    default_type: str = "Object"
    string_type: str = "String"
    int_type: str = "int"
    float_type: str = "double"
    bool_type: str = "boolean"
    list_type: str = "List"
    dict_type: str = "Map"

    # 代码风格
    indent_size: int = 4
    use_tabs: bool = False
    add_access_modifiers: bool = True
    add_final_modifiers: bool = False

    # 函数映射
    print_function: str = "System.out.println"
    len_function: str = ".size()"
    range_function: str = "IntStream.range"

    # 高级选项
    enable_type_inference: bool = True
    enable_string_interpolation: bool = True
    enable_collection_literals: bool = True
    preserve_comments: bool = True

    # 性能选项
    cache_enabled: bool = True
    max_cache_size: int = 1000

    # 调试选项
    debug_mode: bool = False
    verbose_output: bool = False


@dataclass
class PluginConfig:
    """插件配置类"""

    enabled_plugins: List[str] = field(default_factory=list)
    plugin_paths: List[str] = field(default_factory=list)
    plugin_settings: Dict[str, Any] = field(default_factory=dict)


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: Optional[str] = None):
        """初始化配置管理器"""
        self.config_file = config_file or self._find_config_file()
        self.config = ConversionConfig()
        self.plugin_config = PluginConfig()
        self._load_config()

    def _find_config_file(self) -> Optional[str]:
        """查找配置文件"""
        search_paths = [
            "pythva.yaml",
            "pythva.yml",
            "pythva.json",
            ".pythva.yaml",
            ".pythva.yml",
            ".pythva.json",
            os.path.expanduser("~/.pythva.yaml"),
            os.path.expanduser("~/.pythva.yml"),
            os.path.expanduser("~/.pythva.json")
        ]

        for path in search_paths:
            if os.path.exists(path):
                return path

        return None

    def _load_config(self):
        """加载配置文件"""
        if not self.config_file:
            return

        try:
            if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                self._load_yaml_config()
            elif self.config_file.endswith('.json'):
                self._load_json_config()
        except Exception as e:
            print(f"警告：无法加载配置文件 {self.config_file}: {e}")

    def _load_yaml_config(self):
        """加载YAML配置文件"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data:
            self._apply_config_data(data)

    def _load_json_config(self):
        """加载JSON配置文件"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data:
            self._apply_config_data(data)

    def _apply_config_data(self, data: Dict[str, Any]):
        """应用配置数据"""
        # 转换配置
        if 'conversion' in data:
            conv_data = data['conversion']
            for key, value in conv_data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)

        # 插件配置
        if 'plugins' in data:
            plugin_data = data['plugins']
            if 'enabled' in plugin_data:
                self.plugin_config.enabled_plugins = plugin_data['enabled']
            if 'paths' in plugin_data:
                self.plugin_config.plugin_paths = plugin_data['paths']
            if 'settings' in plugin_data:
                self.plugin_config.plugin_settings = plugin_data['settings']

    def save_config(self, file_path: Optional[str] = None) -> str:
        """保存配置到文件"""
        save_path = file_path or self.config_file or "pythva.yaml"

        config_data = {
            'conversion': {
                'output_style': self.config.output_style,
                'add_package_declaration': self.config.add_package_declaration,
                'package_name': self.config.package_name,
                'default_type': self.config.default_type,
                'string_type': self.config.string_type,
                'int_type': self.config.int_type,
                'float_type': self.config.float_type,
                'bool_type': self.config.bool_type,
                'list_type': self.config.list_type,
                'dict_type': self.config.dict_type,
                'indent_size': self.config.indent_size,
                'use_tabs': self.config.use_tabs,
                'add_access_modifiers': self.config.add_access_modifiers,
                'add_final_modifiers': self.config.add_final_modifiers,
                'print_function': self.config.print_function,
                'len_function': self.config.len_function,
                'range_function': self.config.range_function,
                'enable_type_inference': self.config.enable_type_inference,
                'enable_string_interpolation': self.config.enable_string_interpolation,
                'enable_collection_literals': self.config.enable_collection_literals,
                'preserve_comments': self.config.preserve_comments,
                'cache_enabled': self.config.cache_enabled,
                'max_cache_size': self.config.max_cache_size,
                'debug_mode': self.config.debug_mode,
                'verbose_output': self.config.verbose_output
            },
            'plugins': {
                'enabled': self.plugin_config.enabled_plugins,
                'paths': self.plugin_config.plugin_paths,
                'settings': self.plugin_config.plugin_settings
            }
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)

        return save_path

    def create_default_config(self, file_path: str = "pythva.yaml") -> str:
        """创建默认配置文件"""
        return self.save_config(file_path)

    def get_conversion_config(self) -> ConversionConfig:
        """获取转换配置"""
        return self.config

    def get_plugin_config(self) -> PluginConfig:
        """获取插件配置"""
        return self.plugin_config

    def update_conversion_config(self, **kwargs):
        """更新转换配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

    def enable_plugin(self, plugin_name: str):
        """启用插件"""
        if plugin_name not in self.plugin_config.enabled_plugins:
            self.plugin_config.enabled_plugins.append(plugin_name)

    def disable_plugin(self, plugin_name: str):
        """禁用插件"""
        if plugin_name in self.plugin_config.enabled_plugins:
            self.plugin_config.enabled_plugins.remove(plugin_name)


# 全局配置实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """获取全局配置管理器"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_conversion_config() -> ConversionConfig:
    """获取转换配置"""
    return get_config_manager().get_conversion_config()


def reload_config():
    """重新加载配置"""
    global _config_manager
    _config_manager = ConfigManager()


if __name__ == "__main__":
    # 测试配置管理器
    config_manager = ConfigManager()

    print("当前配置:")
    print(f"输出样式: {config_manager.config.output_style}")
    print(f"缩进大小: {config_manager.config.indent_size}")
    print(f"调试模式: {config_manager.config.debug_mode}")

    # 创建默认配置文件
    config_file = config_manager.create_default_config()
    print(f"默认配置文件已创建: {config_file}")