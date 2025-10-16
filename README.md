# Pythva - Python到Java风格转换器

Pythva是一个创新的工具，可以将Python代码转换为类似Java风格的语法，同时保持核心仍然是Python。这使得Python代码看起来更像Java，但仍然可以使用Python的运行时环境执行。

## 特性

- 🚀 **语法转换**: 将Python语法转换为Java风格的花括号语法
- 📝 **类型推断**: 自动推断变量类型并添加类型声明
- 🔧 **访问修饰符**: 为类和方法添加public访问修饰符
- 📦 **包结构**: 生成标准的Java包结构
- 🎯 **智能转换**: 智能处理条件语句、循环、函数调用等
- 🧪 **测试覆盖**: 包含完整的测试用例
- 💻 **命令行工具**: 提供便捷的命令行接口
- 🌐 **Web界面**: 基于Flask的在线演示界面
- ⚙️ **配置系统**: YAML/JSON配置文件支持
- 🔌 **插件系统**: 可扩展的插件架构
- ⚡ **性能优化**: 智能缓存和性能监控
- 🐳 **Docker支持**: 容器化部署方案

## 安装

```bash
# 从源码安装
git clone <repository-url>
cd pythva
pip install -e .

# 或者直接使用
python -m pythva.cli --help
```

## 快速开始

### 命令行使用

```bash
# 转换Python文件并输出到控制台
python -m pythva.cli convert example.py

# 转换并保存到文件
python -m pythva.cli convert example.py -o example.java

# 使用增强转换器（包含更多语法映射）
python -m pythva.cli convert example.py --enhanced

# 创建示例文件
python -m pythva.cli create-examples
```

### Python API

```python
from pythva import convert_python_to_java_style, convert_with_mapping

# 基本转换
python_code = '''
class HelloWorld:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")
'''

java_style_code = convert_python_to_java_style(python_code)
print(java_style_code)

# 增强转换（包含导入和高级映射）
enhanced_code = convert_with_mapping(python_code)
print(enhanced_code)
```

## 转换示例

### Python原始代码

```python
class Calculator:
    def __init__(self, initial_value=0):
        self.result = initial_value
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"add({a}, {b}) = {result}")
        return result

    def calculate_expression(self, expression):
        numbers = [1, 2, 3, 4, 5]
        total = sum(numbers)
        return total
```

### 转换后的Java风格代码

```java
package pythva.generated;

public class Calculator {
    public Calculator(int initial_value) {
        this.result = initial_value;
        this.history = new ArrayList<>();
    }

    public int add(int a, int b) {
        int result = (a + b);
        this.history.add(String.format("add(%s, %s) = %s", a, b, result));
        return result;
    }

    public int calculate_expression(String expression) {
        List<Object> numbers = Arrays.asList(1, 2, 3, 4, 5);
        int total = 0;  // sum函数需要手动实现或使用流
        for (Object num : numbers) {
            total += (Integer) num;
        }
        return total;
    }
}
```

## 转换规则

### 类和方法

- Python类定义转换为Java类，使用`public class`
- 方法定义使用`public`修饰符
- `__init__`方法转换为构造函数
- 参数和变量自动推断类型

### 控制结构

- `if`/`elif`/`else` 转换为Java风格的花括号语法
- `for`循环转换为增强for循环（当适用时）
- `while`循环保持相似的结构

### 数据类型

- `int` → `int`
- `str` → `String`
- `float` → `double`
- `bool` → `boolean`
- `list` → `List<Object>` 或 `ArrayList`
- `dict` → `Map<Object, Object>` 或 `HashMap`

### 特殊转换

- `print()` → `System.out.println()`
- `len()` → `.size()` 或 `.length()`
- 字符串格式化使用`String.format()`
- 列表和字典字面量转换为相应的Java集合

## 项目结构

```
pythva/
├── __init__.py          # 包初始化
├── __main__.py          # 主入口点
├── core.py              # 核心转换器
├── mapper.py            # 语法映射器
├── cli.py               # 命令行接口
├── test_converter.py    # 测试用例
├── examples/            # 示例文件
│   ├── basic_example.py
│   └── advanced_example.py
└── README.md           # 项目文档
```

## 测试

运行测试用例：

```bash
# 运行所有测试
python -m pythva.test_converter

# 或者直接运行测试文件
python pythva/test_converter.py
```

## 示例演示

查看和运行示例：

```bash
# 创建示例文件
python -m pythva.cli create-examples

# 转换基本示例
python -m pythva.cli convert pythva/examples/basic_example.py

# 转换高级示例
python -m pythva.cli convert pythva/examples/advanced_example.py --enhanced
```

## 注意事项

1. **不是真正的Java代码**: 转换后的代码仍然是Python代码，只是语法看起来像Java
2. **需要手动调整**: 某些复杂的Python特性可能需要手动调整转换结果
3. **类型推断**: 类型推断基于代码分析，可能需要手动修正
4. **导入语句**: 某些Python模块需要手动转换为相应的Java库

## 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 作者

Pythva项目由 Yaku Makki 开发，旨在探索编程语言语法转换的可能性。

## 联系方式

- 📧 邮箱：yakumakki947@hotmail.com
- 🐙 GitHub：https://github.com/makkichan947/pythva

---

**享受Python和Java双重体验！** 🎉