#!/usr/bin/env python3
"""
Pythva命令行接口
提供命令行工具来转换Python代码为Java风格
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

try:
    from .core import convert_python_to_java_style
    from .mapper import convert_with_mapping
except ImportError:
    from core import convert_python_to_java_style
    from mapper import convert_with_mapping


def read_file(file_path: str) -> str:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"错误：无法读取文件 '{file_path}'，请检查文件编码")
        sys.exit(1)


def write_file(file_path: str, content: str) -> None:
    """写入文件内容"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"转换后的代码已保存到: {file_path}")
    except Exception as e:
        print(f"错误：无法写入文件 '{file_path}': {e}")
        sys.exit(1)


def convert_code(
    input_code: str,
    output_file: Optional[str] = None,
    use_enhanced: bool = False,
    show_imports: bool = True
) -> str:
    """转换代码"""
    try:
        if use_enhanced:
            converted_code = convert_with_mapping(input_code)
        else:
            converted_code = convert_python_to_java_style(input_code)

        if output_file:
            write_file(output_file, converted_code)
        else:
            print(converted_code)

        return converted_code

    except Exception as e:
        error_msg = f"转换过程中出错: {e}"
        print(error_msg)
        if not output_file:
            print("\n原始代码:")
            print(input_code)
        sys.exit(1)


def create_example_files():
    """创建示例文件"""
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)

    # Python示例代码
    python_example = '''class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        return a + b

    def multiply(self, x, y):
        return x * y

    def calculate_expression(self, expression):
        # 这是一个计算表达式的示例
        numbers = [1, 2, 3, 4, 5]
        total = sum(numbers)
        return total

# 使用示例
calc = Calculator()
result1 = calc.add(10, 20)
result2 = calc.multiply(5, 6)
result3 = calc.calculate_expression("1+2+3")
'''

    # 写入Python示例文件
    with open(examples_dir / "example.py", "w", encoding='utf-8') as f:
        f.write(python_example)

    print(f"示例文件已创建: {examples_dir / 'example.py'}")
    print("运行以下命令进行转换:")
    print(f"  python -m pythva.cli convert {examples_dir / 'example.py'}")
    print(f"  python -m pythva.cli convert {examples_dir / 'example.py'} -o {examples_dir / 'example.java'}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        prog='pythva',
        description='将Python代码转换为Java风格的语法',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  python -m pythva.cli convert example.py
  python -m pythva.cli convert example.py -o example.java
  python -m pythva.cli convert example.py --enhanced
  python -m pythva.cli create-examples
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # convert命令
    convert_parser = subparsers.add_parser(
        'convert',
        help='转换Python文件为Java风格'
    )
    convert_parser.add_argument(
        'input_file',
        help='输入的Python文件路径'
    )
    convert_parser.add_argument(
        '-o', '--output',
        help='输出文件路径（不指定则输出到控制台）'
    )
    convert_parser.add_argument(
        '-e', '--enhanced',
        action='store_true',
        help='使用增强转换器（包含更多语法映射）'
    )
    convert_parser.add_argument(
        '--no-imports',
        action='store_true',
        help='不显示导入语句'
    )

    # examples命令
    examples_parser = subparsers.add_parser(
        'create-examples',
        help='创建示例文件'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'convert':
        # 读取输入文件
        input_code = read_file(args.input_file)

        # 转换代码
        convert_code(
            input_code=input_code,
            output_file=args.output,
            use_enhanced=args.enhanced,
            show_imports=not args.no_imports
        )

    elif args.command == 'create-examples':
        create_example_files()


if __name__ == "__main__":
    main()