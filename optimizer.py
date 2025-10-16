#!/usr/bin/env python3
"""
Pythva性能优化和缓存模块
提供代码优化、缓存管理和性能监控功能
"""

import hashlib
import json
import time
import pickle
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass
import ast


@dataclass
class CacheEntry:
    """缓存条目"""
    code_hash: str
    converted_code: str
    timestamp: float
    access_count: int = 0
    last_accessed: float = 0.0


@dataclass
class PerformanceMetrics:
    """性能指标"""
    conversion_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    total_conversions: int = 0
    average_conversion_time: float = 0.0


class ConversionCache:
    """转换缓存管理器"""

    def __init__(self, max_size: int = 1000, cache_file: Optional[str] = None):
        """初始化缓存管理器"""
        self.max_size = max_size
        self.cache_file = cache_file
        self.cache: Dict[str, CacheEntry] = {}
        self._load_cache()

    def _get_code_hash(self, code: str) -> str:
        """计算代码哈希值"""
        return hashlib.md5(code.encode('utf-8')).hexdigest()

    def get(self, code: str) -> Optional[str]:
        """从缓存获取转换结果"""
        code_hash = self._get_code_hash(code)

        if code_hash in self.cache:
            entry = self.cache[code_hash]
            entry.access_count += 1
            entry.last_accessed = time.time()
            return entry.converted_code

        return None

    def put(self, code: str, converted_code: str):
        """将转换结果存入缓存"""
        code_hash = self._get_code_hash(code)

        # 检查缓存大小
        if len(self.cache) >= self.max_size and code_hash not in self.cache:
            self._evict_oldest()

        entry = CacheEntry(
            code_hash=code_hash,
            converted_code=converted_code,
            timestamp=time.time()
        )

        self.cache[code_hash] = entry

    def _evict_oldest(self):
        """驱逐最老的缓存条目"""
        if not self.cache:
            return

        # 基于最后访问时间和访问次数的综合评分
        oldest_entry = min(
            self.cache.values(),
            key=lambda e: (e.last_accessed, -e.access_count)
        )

        del self.cache[oldest_entry.code_hash]

    def _load_cache(self):
        """从文件加载缓存"""
        if not self.cache_file or not Path(self.cache_file).exists():
            return

        try:
            with open(self.cache_file, 'rb') as f:
                data = pickle.load(f)

            for entry_data in data:
                entry = CacheEntry(**entry_data)
                self.cache[entry.code_hash] = entry

        except Exception:
            # 缓存文件损坏，重置缓存
            self.cache = {}

    def save_cache(self):
        """保存缓存到文件"""
        if not self.cache_file:
            return

        try:
            cache_data = []
            for entry in self.cache.values():
                cache_data.append({
                    'code_hash': entry.code_hash,
                    'converted_code': entry.converted_code,
                    'timestamp': entry.timestamp,
                    'access_count': entry.access_count,
                    'last_accessed': entry.last_accessed
                })

            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)

        except Exception:
            pass  # 保存失败时静默处理

    def clear(self):
        """清空缓存"""
        self.cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_accesses = sum(entry.access_count for entry in self.cache.values())
        hit_rate = 0.0

        if total_accesses > 0:
            hit_rate = (total_accesses / (total_accesses + sum(1 for _ in self.cache.values()))) * 100

        return {
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'total_accesses': total_accesses,
            'hit_rate_percent': hit_rate,
            'oldest_entry': min((e.timestamp for e in self.cache.values()), default=0),
            'newest_entry': max((e.timestamp for e in self.cache.values()), default=0)
        }


class CodeOptimizer:
    """代码优化器"""

    def __init__(self):
        """初始化优化器"""
        self.optimization_rules = {
            'remove_redundant_parentheses': self._remove_redundant_parentheses,
            'simplify_expressions': self._simplify_expressions,
            'optimize_string_concatenation': self._optimize_string_concatenation,
            'remove_unused_imports': self._remove_unused_imports,
        }

    def optimize(self, code: str, enabled_rules: Optional[List[str]] = None) -> str:
        """优化代码"""
        if not enabled_rules:
            enabled_rules = list(self.optimization_rules.keys())

        optimized_code = code

        for rule_name in enabled_rules:
            if rule_name in self.optimization_rules:
                try:
                    optimized_code = self.optimization_rules[rule_name](optimized_code)
                except Exception:
                    # 优化失败时跳过该规则
                    continue

        return optimized_code

    def _remove_redundant_parentheses(self, code: str) -> str:
        """移除多余的括号"""
        # 简单的括号简化逻辑
        import re

        # 移除多余的嵌套括号
        patterns = [
            (r'\(\(([^()]+)\)\)', r'(\1)'),  # ((expr)) -> (expr)
            (r'\(\(([^()]*)\)\)', r'(\1)'),   # ((expr)) -> (expr)
        ]

        for pattern, replacement in patterns:
            code = re.sub(pattern, replacement, code)

        return code

    def _simplify_expressions(self, code: str) -> str:
        """简化表达式"""
        # 这里可以添加更多的表达式简化逻辑
        return code

    def _optimize_string_concatenation(self, code: str) -> str:
        """优化字符串连接"""
        # 将多个字符串连接优化为StringBuilder模式（如果适用）
        return code

    def _remove_unused_imports(self, code: str) -> str:
        """移除未使用的导入"""
        # 分析代码中的导入使用情况
        return code


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        """初始化性能监控器"""
        self.metrics = PerformanceMetrics()
        self.start_time = 0.0

    def start_conversion(self):
        """开始转换计时"""
        self.start_time = time.time()

    def end_conversion(self):
        """结束转换计时"""
        if self.start_time > 0:
            conversion_time = time.time() - self.start_time
            self.metrics.conversion_time = conversion_time
            self.metrics.total_conversions += 1

            # 更新平均时间
            total_time = self.metrics.average_conversion_time * (self.metrics.total_conversions - 1)
            self.metrics.average_conversion_time = (total_time + conversion_time) / self.metrics.total_conversions

            self.start_time = 0.0

    def record_cache_hit(self):
        """记录缓存命中"""
        self.metrics.cache_hits += 1

    def record_cache_miss(self):
        """记录缓存未命中"""
        self.metrics.cache_misses += 1

    def get_metrics(self) -> PerformanceMetrics:
        """获取性能指标"""
        return self.metrics

    def get_detailed_report(self) -> str:
        """获取详细性能报告"""
        metrics = self.metrics
        cache_efficiency = 0.0

        if (metrics.cache_hits + metrics.cache_misses) > 0:
            cache_efficiency = (metrics.cache_hits / (metrics.cache_hits + metrics.cache_misses)) * 100

        return f"""
性能监控报告:
- 总转换次数: {metrics.total_conversions}
- 平均转换时间: {metrics.average_conversion_time:.4f}秒
- 最后转换时间: {metrics.conversion_time:.4f}秒
- 缓存命中: {metrics.cache_hits}
- 缓存未命中: {metrics.cache_misses}
- 缓存效率: {cache_efficiency:.2f}%
        """.strip()

    def reset(self):
        """重置性能指标"""
        self.metrics = PerformanceMetrics()


class OptimizedConverter:
    """优化的转换器，集成缓存和性能监控"""

    def __init__(self, cache_enabled: bool = True, max_cache_size: int = 1000,
                 debug_mode: bool = False):
        """初始化优化转换器"""
        self.cache = ConversionCache(max_cache_size) if cache_enabled else None
        self.monitor = PerformanceMonitor()
        self.debug_mode = debug_mode
        self.optimizer = CodeOptimizer()

        # 导入核心转换器
        from .core import convert_python_to_java_style
        from .mapper import convert_with_mapping
        self.basic_converter = convert_python_to_java_style
        self.enhanced_converter = convert_with_mapping

    def convert(self, code: str, use_enhanced: bool = False,
                optimize: bool = True) -> str:
        """转换代码（带缓存和优化）"""
        self.monitor.start_conversion()

        # 尝试从缓存获取
        if self.cache:
            cached_result = self.cache.get(code)
            if cached_result:
                self.monitor.record_cache_hit()
                self.monitor.end_conversion()
                return cached_result

        self.monitor.record_cache_miss()

        # 执行转换
        try:
            if use_enhanced:
                converted_code = self.enhanced_converter(code)
            else:
                converted_code = self.basic_converter(code)

            # 应用优化
            if optimize:
                converted_code = self.optimizer.optimize(converted_code)

            # 存入缓存
            if self.cache:
                self.cache.put(code, converted_code)

        except Exception as e:
            self.monitor.end_conversion()
            raise e

        self.monitor.end_conversion()
        return converted_code

    def get_performance_report(self) -> str:
        """获取性能报告"""
        return self.monitor.get_detailed_report()

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        if self.cache:
            return self.cache.get_stats()
        return {}

    def clear_cache(self):
        """清空缓存"""
        if self.cache:
            self.cache.clear()

    def save_cache(self):
        """保存缓存"""
        if self.cache:
            self.cache.save_cache()


# 全局优化转换器实例
_global_optimizer: Optional[OptimizedConverter] = None


def get_optimized_converter() -> OptimizedConverter:
    """获取全局优化转换器"""
    global _global_optimizer
    if _global_optimizer is None:
        _global_optimizer = OptimizedConverter()
    return _global_optimizer


def convert_with_optimization(code: str, use_enhanced: bool = False) -> str:
    """使用优化的方式进行转换"""
    converter = get_optimized_converter()
    return converter.convert(code, use_enhanced)


if __name__ == "__main__":
    # 测试优化器
    cache = ConversionCache(max_size=100)

    # 测试缓存
    test_code = "print('hello')"
    result1 = "System.out.println('hello');"

    cache.put(test_code, result1)
    retrieved = cache.get(test_code)

    print(f"缓存测试: {retrieved == result1}")
    print(f"缓存统计: {cache.get_stats()}")

    # 测试优化器
    optimizer = CodeOptimizer()
    optimized = optimizer.optimize("((test))")
    print(f"优化测试: '{optimized}'")