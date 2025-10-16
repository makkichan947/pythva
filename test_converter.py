#!/usr/bin/env python3
"""
Pythva转换器测试
"""

import unittest
from core import convert_python_to_java_style
from mapper import convert_with_mapping


class TestPythvaConverter(unittest.TestCase):
    """测试转换器功能"""

    def test_basic_class_conversion(self):
        """测试基本类转换"""
        python_code = '''
class HelloWorld:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")
'''
        expected_java = '''package pythva.generated;

public class HelloWorld {
    public HelloWorld(String name) {
        this.name = name;
    }

    public void greet() {
        System.out.println(String.format("Hello, %s!", this.name));
    }
}'''

        result = convert_python_to_java_style(python_code)
        self.assertIn("public class HelloWorld", result)
        self.assertIn("public HelloWorld(String name)", result)
        self.assertIn("public void greet()", result)

    def test_method_with_return(self):
        """测试带返回值的函数"""
        python_code = '''
def calculate(a, b):
    return a + b
'''
        result = convert_python_to_java_style(python_code)
        self.assertIn("public Object calculate", result)
        self.assertIn("return (a + b)", result)

    def test_conditional_statement(self):
        """测试条件语句"""
        python_code = '''
def check_value(x):
    if x > 0:
        return "positive"
    else:
        return "negative"
'''
        result = convert_python_to_java_style(python_code)
        self.assertIn("if (x > 0)", result)
        self.assertIn("return \"positive\"", result)
        self.assertIn("else", result)

    def test_loop_conversion(self):
        """测试循环转换"""
        python_code = '''
def sum_list(items):
    total = 0
    for item in items:
        total += item
    return total
'''
        result = convert_python_to_java_style(python_code)
        self.assertIn("for (item : items)", result)

    def test_variable_assignment(self):
        """测试变量赋值"""
        python_code = '''
def test_assignment():
    x = 10
    y = "hello"
    z = True
    return x, y, z
'''
        result = convert_python_to_java_style(python_code)
        self.assertIn("int x = 10", result)
        self.assertIn("String y = \"hello\"", result)
        self.assertIn("boolean z = true", result)

    def test_enhanced_converter_imports(self):
        """测试增强转换器的导入功能"""
        python_code = '''
from typing import List

def process_list(data: List[int]):
    return sum(data)
'''
        result = convert_with_mapping(python_code)
        self.assertIn("import java.util.List", result)
        self.assertIn("import java.util.ArrayList", result)

    def test_list_and_dict_literals(self):
        """测试列表和字典字面量"""
        python_code = '''
def test_literals():
    my_list = [1, 2, 3]
    my_dict = {"a": 1, "b": 2}
    return my_list, my_dict
'''
        result = convert_with_mapping(python_code)
        self.assertIn("Arrays.asList", result)
        self.assertIn("Map.of", result)


def run_tests():
    """运行测试"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()