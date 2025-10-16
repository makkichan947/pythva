#!/usr/bin/env python3
"""
Pythva核心转换器模块
将Python代码转换为Java风格的语法
"""

import ast
import re
from typing import Dict, List, Any, Optional


class JavaStyleConverter(ast.NodeVisitor):
    """Python到Java风格的代码转换器"""

    def __init__(self):
        self.indent_level = 0
        self.lines: List[str] = []
        self.class_stack: List[str] = []
        self.in_method = False

    def convert(self, code: str) -> str:
        """转换Python代码为Java风格"""
        try:
            # 解析Python代码
            tree = ast.parse(code)
            self.visit(tree)

            # 添加包声明（如果需要）
            if self.class_stack:
                package_lines = [f"package pythva.generated;"]
                package_lines.append("")
                return "\n".join(package_lines + self.lines)

            return "\n".join(self.lines)
        except SyntaxError as e:
            return f"// 语法错误: {e}\n{code}"

    def add_line(self, line: str, indent: bool = True):
        """添加一行代码"""
        if indent and line.strip():
            self.lines.append("    " * self.indent_level + line)
        else:
            self.lines.append(line)

    def visit_ClassDef(self, node: ast.ClassDef):
        """访问类定义"""
        # 添加访问修饰符
        class_name = node.name

        # 检查基类
        base_classes = []
        if node.bases:
            for base in node.bases:
                if isinstance(base, ast.Name):
                    base_classes.append(base.id)

        # 类声明
        extends = f" extends {', '.join(base_classes)}" if base_classes else ""

        self.add_line(f"public class {class_name}{extends} {{")
        self.class_stack.append(class_name)
        self.indent_level += 1

        # 访问类体
        for item in node.body:
            self.visit(item)

        self.indent_level -= 1
        self.add_line("}")
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """访问函数定义"""
        # 方法签名
        method_name = node.name
        if method_name == "__init__":
            method_name = self.class_stack[-1] if self.class_stack else "Constructor"

        # 获取返回类型注解
        returns = "Object"
        if node.returns:
            returns = self._get_type_annotation(node.returns)

        # 获取参数类型注解
        params = []
        for arg in node.args.args:
            param_type = "Object"  # 默认类型
            if arg.arg in ['self']:  # 跳过self参数
                continue

            # 特殊参数类型处理
            if method_name == "__init__" and arg.arg == 'name':
                param_type = "String"
            elif arg.arg in ['a', 'b', 'x', 'y']:
                param_type = "int"  # 常见数学参数

            params.append(f"{param_type} {arg.arg}")

        self.add_line(f"public {returns} {method_name}({', '.join(params)}) {{")
        self.in_method = True
        old_indent = self.indent_level
        self.indent_level += 1

        # 访问方法体
        for item in node.body:
            self.visit(item)

        self.indent_level = old_indent
        self.add_line("}")
        self.in_method = False

    def visit_Assign(self, node: ast.Assign):
        """访问赋值语句"""
        targets = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                targets.append(target.id)

        if targets and node.value:
            # 类型推断
            var_type = self._infer_type(node.value)
            var_names = ", ".join(targets)

            if len(targets) == 1:
                self.add_line(f"{var_type} {var_names} = {self._get_value_code(node.value)};")
            else:
                self.add_line(f"{var_type} {var_names};")
                for target in targets:
                    self.add_line(f"{target} = {self._get_value_code(node.value)};")

    def visit_Return(self, node: ast.Return):
        """访问返回语句"""
        if node.value:
            self.add_line(f"return {self._get_value_code(node.value)};")
        else:
            self.add_line("return;")

    def visit_If(self, node: ast.If):
        """访问条件语句"""
        condition = self._get_value_code(node.test)
        self.add_line(f"if ({condition}) {{")
        self.indent_level += 1

        for item in node.body:
            self.visit(item)

        self.indent_level -= 1
        self.add_line("}")

        # 处理else
        if node.orelse:
            self.add_line("else {")
            self.indent_level += 1

            for item in node.orelse:
                self.visit(item)

            self.indent_level -= 1
            self.add_line("}")

    def visit_For(self, node: ast.For):
        """访问for循环"""
        target = self._get_value_code(node.target)
        iter_expr = self._get_value_code(node.iter)

        self.add_line(f"for ({target} : {iter_expr}) {{")
        self.indent_level += 1

        for item in node.body:
            self.visit(item)

        self.indent_level -= 1
        self.add_line("}")

    def visit_While(self, node: ast.While):
        """访问while循环"""
        condition = self._get_value_code(node.test)
        self.add_line(f"while ({condition}) {{")
        self.indent_level += 1

        for item in node.body:
            self.visit(item)

        self.indent_level -= 1
        self.add_line("}")

    def visit_Expr(self, node: ast.Expr):
        """访问表达式语句"""
        if isinstance(node.value, ast.Call):
            # 函数调用
            call_code = self._get_call_code(node.value)
            self.add_line(f"{call_code};")
        elif isinstance(node.value, ast.Constant):
            # 常量表达式
            if isinstance(node.value.value, str):
                self.add_line(f'System.out.println("{node.value.value}");')

    def visit_JoinedStr(self, node: ast.JoinedStr):
        """处理f-string"""
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(f'"{value.value}"')
            elif isinstance(value, ast.FormattedValue):
                parts.append(self._get_value_code(value.value))

        return " + ".join(parts)

    def visit_FormattedValue(self, node: ast.FormattedValue):
        """处理格式化值"""
        return self._get_value_code(node.value)

    def _get_value_code(self, node) -> str:
        """获取值的代码表示"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, ast.List):
            elements = [self._get_value_code(elt) for elt in node.elts]
            return f"Arrays.asList({', '.join(elements)})"
        elif isinstance(node, ast.Dict):
            keys = [self._get_value_code(k) for k in node.keys]
            values = [self._get_value_code(v) for v in node.values]
            items = [f"{k}, {v}" for k, v in zip(keys, values)]
            return f"Map.of({', '.join(items)})"
        elif isinstance(node, ast.BinOp):
            left = self._get_value_code(node.left)
            right = self._get_value_code(node.right)
            op = self._get_binop(node.op)
            return f"({left} {op} {right})"
        elif isinstance(node, ast.Compare):
            left = self._get_value_code(node.left)
            comparators = node.comparators
            if comparators:
                ops = [self._get_cmpop(op) for op in [node.ops[0]]]
                return f"({left} {ops[0]} {self._get_value_code(comparators[0])})"
            return str(node)
        elif isinstance(node, ast.Call):
            return self._get_call_code(node)
        elif isinstance(node, ast.Attribute):
            return f"{self._get_value_code(node.value)}.{node.attr}"
        elif isinstance(node, ast.JoinedStr):
            return self.visit_JoinedStr(node)
        return str(node)

    def _get_call_code(self, node: ast.Call) -> str:
        """获取函数调用代码"""
        func_name = self._get_value_code(node.func)
        args = [self._get_value_code(arg) for arg in node.args]
        return f"{func_name}({', '.join(args)})"

    def _get_binop(self, op) -> str:
        """获取二元运算符"""
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        elif isinstance(op, ast.Mod):
            return "%"
        return str(op)

    def _get_cmpop(self, op) -> str:
        """获取比较运算符"""
        if isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.GtE):
            return ">="
        return str(op)

    def _get_type_annotation(self, node) -> str:
        """获取类型注解"""
        if isinstance(node, ast.Name):
            type_map = {
                'int': 'int',
                'str': 'String',
                'float': 'double',
                'bool': 'boolean',
                'list': 'List',
                'dict': 'Map'
            }
            return type_map.get(node.id, 'Object')
        return 'Object'

    def _infer_type(self, node) -> str:
        """推断变量类型"""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int):
                return "int"
            elif isinstance(node.value, float):
                return "double"
            elif isinstance(node.value, str):
                return "String"
            elif isinstance(node.value, bool):
                return "boolean"
            elif node.value is True:
                return "boolean"
            elif node.value is False:
                return "boolean"
        elif isinstance(node, ast.List):
            return "List<Object>"
        elif isinstance(node, ast.Dict):
            return "Map<Object, Object>"
        return "Object"


def convert_python_to_java_style(code: str) -> str:
    """将Python代码转换为Java风格"""
    converter = JavaStyleConverter()
    return converter.convert(code)


if __name__ == "__main__":
    # 测试代码
    python_code = '''
class HelloWorld:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

    def calculate(self, a, b):
        return a + b

# 使用示例
obj = HelloWorld("World")
result = obj.greet()
sum_result = obj.calculate(10, 20)
'''

    java_style_code = convert_python_to_java_style(python_code)
    print(java_style_code)