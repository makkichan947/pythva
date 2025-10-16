#!/usr/bin/env python3
"""
Pythva语法映射器模块
提供Python到Java风格的详细语法映射规则
"""

import ast
import re
from typing import Dict, List, Tuple, Any, Optional


class SyntaxMapper:
    """语法映射器"""

    # Python内置类型到Java类型的映射
    TYPE_MAPPING = {
        'int': 'int',
        'float': 'double',
        'str': 'String',
        'bool': 'boolean',
        'list': 'List',
        'dict': 'Map',
        'tuple': 'List',  # 元组映射为只读列表
        'set': 'Set',
        'None': 'null',
        'True': 'true',
        'False': 'false'
    }

    # 常用Python函数到Java静态方法的映射
    FUNCTION_MAPPING = {
        'print': 'System.out.println',
        'len': 'Collection.size',  # 需要上下文判断
        'range': 'IntStream.range',
        'enumerate': 'List.of',  # 简化处理
        'zip': 'List.of',  # 简化处理
        'sum': 'Collection.sum',  # 需要上下文判断
        'max': 'Collections.max',
        'min': 'Collections.min',
        'abs': 'Math.abs',
        'round': 'Math.round'
    }

    # Python魔法方法到Java方法的映射
    MAGIC_METHODS = {
        '__init__': 'constructor',
        '__str__': 'toString',
        '__repr__': 'toString',
        '__len__': 'size',
        '__getitem__': 'get',
        '__setitem__': 'set',
        '__iter__': 'iterator',
        '__next__': 'next',
        '__eq__': 'equals',
        '__lt__': 'compareTo',
        '__le__': 'compareTo',
        '__gt__': 'compareTo',
        '__ge__': 'compareTo',
        '__add__': 'plus',
        '__sub__': 'minus',
        '__mul__': 'multiply',
        '__truediv__': 'divide'
    }

    @classmethod
    def map_type(cls, python_type: str) -> str:
        """映射Python类型到Java类型"""
        return cls.TYPE_MAPPING.get(python_type, 'Object')

    @classmethod
    def map_function(cls, func_name: str, context: str = "") -> str:
        """映射Python函数到Java方法"""
        if func_name in cls.FUNCTION_MAPPING:
            return cls.FUNCTION_MAPPING[func_name]
        return func_name

    @classmethod
    def map_magic_method(cls, magic_method: str) -> str:
        """映射Python魔法方法到Java方法"""
        return cls.MAGIC_METHODS.get(magic_method, magic_method)

    @classmethod
    def needs_import(cls, java_type: str) -> bool:
        """判断是否需要导入"""
        import_required_types = {
            'List', 'Map', 'Set', 'ArrayList', 'HashMap', 'HashSet',
            'Arrays', 'Collections', 'IntStream'
        }
        return java_type in import_required_types

    @classmethod
    def get_required_imports(cls, code: str) -> List[str]:
        """获取需要的导入语句"""
        imports = set()

        # 分析代码中的类型使用
        for type_name in ['List', 'Map', 'Set', 'Arrays', 'Collections']:
            if type_name in code:
                if type_name == 'List':
                    imports.add('import java.util.List;')
                    imports.add('import java.util.ArrayList;')
                elif type_name == 'Map':
                    imports.add('import java.util.Map;')
                    imports.add('import java.util.HashMap;')
                elif type_name == 'Set':
                    imports.add('import java.util.Set;')
                    imports.add('import java.util.HashSet;')
                elif type_name == 'Arrays':
                    imports.add('import java.util.Arrays;')
                elif type_name == 'Collections':
                    imports.add('import java.util.Collections;')

        return sorted(list(imports))


class EnhancedConverter(ast.NodeVisitor):
    """增强的转换器，包含更多语法映射"""

    def __init__(self):
        self.mapper = SyntaxMapper()
        self.imports: List[str] = []
        self.lines: List[str] = []
        self.indent_level = 0
        self.in_class = False
        self.variables: Dict[str, str] = {}  # 变量类型追踪

    def convert(self, code: str) -> str:
        """转换代码并添加必要的导入"""
        tree = ast.parse(code)

        # 第一遍：收集类型信息和导入需求
        self._collect_info(tree)

        # 第二遍：生成Java风格代码
        self.visit(tree)

        # 组合导入和代码
        all_lines = self.imports + [''] + self.lines if self.imports else self.lines
        return '\n'.join(all_lines)

    def _collect_info(self, tree: ast.AST):
        """收集类型信息和导入需求"""
        for node in ast.walk(tree):
            if isinstance(node, ast.List):
                self.imports.append('import java.util.List;')
                self.imports.append('import java.util.ArrayList;')
            elif isinstance(node, ast.Dict):
                self.imports.append('import java.util.Map;')
                self.imports.append('import java.util.HashMap;')
            elif isinstance(node, ast.Name):
                if node.id in ['print', 'len', 'range', 'sum', 'max', 'min']:
                    # 这些函数需要特殊处理
                    pass

    def add_line(self, line: str, indent: bool = True):
        """添加一行代码"""
        if indent and line.strip():
            self.lines.append("    " * self.indent_level + line)
        else:
            self.lines.append(line)

    def visit_Import(self, node: ast.Import):
        """处理import语句"""
        for alias in node.names:
            module_name = alias.name
            # 将Python模块导入转换为Java导入
            if module_name.startswith('pythva'):
                self.add_line(f"import {module_name}.*;")
            else:
                # 对于其他模块，保持原样或转换为相应的Java库
                self.add_line(f"// import {module_name} (需要手动转换)")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """处理from import语句"""
        if node.module:
            for alias in node.names:
                if node.module == 'typing' and alias.name == 'List':
                    self.imports.append('import java.util.List;')
                elif node.module == 'typing' and alias.name == 'Dict':
                    self.imports.append('import java.util.Map;')
                else:
                    self.add_line(f"// from {node.module} import {alias.name} (需要手动转换)")

    def visit_List(self, node: ast.List):
        """处理列表字面量"""
        if node.elts:
            elements = []
            for elt in node.elts:
                elements.append(self._get_value_code(elt))
            return f"Arrays.asList({', '.join(elements)})"
        return "new ArrayList<>()"

    def visit_Dict(self, node: ast.Dict):
        """处理字典字面量"""
        if node.keys and node.values:
            items = []
            for key, value in zip(node.keys, node.values):
                key_code = self._get_value_code(key)
                value_code = self._get_value_code(value)
                items.append(f"{key_code}, {value_code}")
            return f"Map.of({', '.join(items)})"
        return "new HashMap<>()"

    def visit_Call(self, node: ast.Call):
        """处理函数调用"""
        func_name = self._get_value_code(node.func)

        # 特殊函数映射
        if func_name == 'print':
            args = [self._get_value_code(arg) for arg in node.args]
            return f"System.out.println({', '.join(args)})"
        elif func_name == 'len':
            if node.args:
                arg = self._get_value_code(node.args[0])
                return f"{arg}.size()"
        elif func_name == 'range':
            if node.args:
                if len(node.args) == 1:
                    return f"IntStream.range(0, {self._get_value_code(node.args[0])})"
                elif len(node.args) == 2:
                    start, end = self._get_value_code(node.args[0]), self._get_value_code(node.args[1])
                    return f"IntStream.range({start}, {end})"

        # 默认处理
        args = [self._get_value_code(arg) for arg in node.args]
        return f"{func_name}({', '.join(args)})"

    def _get_value_code(self, node) -> str:
        """获取值的代码表示（简化版）"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, ast.List):
            return self.visit_List(node)
        elif isinstance(node, ast.Dict):
            return self.visit_Dict(node)
        elif isinstance(node, ast.Call):
            return self.visit_Call(node)
        elif isinstance(node, ast.BinOp):
            left = self._get_value_code(node.left)
            right = self._get_value_code(node.right)
            op = self._get_binop(node.op)
            return f"({left} {op} {right})"
        return str(node)

    def _get_binop(self, op) -> str:
        """获取二元运算符"""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%',
            ast.Pow: '**',
            ast.LShift: '<<',
            ast.RShift: '>>',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.BitAnd: '&',
            ast.FloorDiv: '//'
        }
        return op_map.get(type(op), str(op))


def convert_with_mapping(code: str) -> str:
    """使用语法映射进行转换"""
    converter = EnhancedConverter()
    return converter.convert(code)


if __name__ == "__main__":
    # 测试语法映射
    test_code = '''
from typing import List, Dict

def process_data(data: List[int]) -> int:
    result = sum(data)
    return result

class DataProcessor:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_length(self):
        return len(self.items)
'''

    converted = convert_with_mapping(test_code)
    print(converted)