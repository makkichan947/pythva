# Pythva快速开始指南

## 🎯 什么是Pythva？

Pythva是一个创新的代码转换工具，可以将Python代码转换为类似Java风格的语法，同时保持核心仍然是Python。这让你可以用Python的简洁性编写代码，却拥有Java般的代码结构。

## 🚀 快速开始

### 安装

```bash
# 从PyPI安装（推荐）
pip install pythva

# 或者从源码安装
git clone https://github.com/pythva/pythva.git
cd pythva
pip install -e .
```

### 基本使用

#### 命令行转换

```bash
# 转换单个文件
pythva convert example.py

# 转换并保存到文件
pythva convert example.py -o example.java

# 使用增强转换器
pythva convert example.py --enhanced

# 创建示例文件
pythva create-examples
```

#### Python API

```python
from pythva import convert_python_to_java_style, convert_with_mapping

# 基本转换
python_code = '''
class HelloWorld:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"
'''

# 转换为Java风格
java_style_code = convert_python_to_java_style(python_code)
print(java_style_code)

# 使用增强转换器（包含更多特性）
enhanced_code = convert_with_mapping(python_code)
print(enhanced_code)
```

## 📋 转换示例

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
        int total = 0;
        for (Object num : numbers) {
            total += (Integer) num;
        }
        return total;
    }
}
```

## ⚙️ 高级功能

### 配置文件

创建 `pythva.yaml` 配置文件来自定义转换行为：

```yaml
conversion:
  output_style: "java"
  add_package_declaration: true
  package_name: "myproject.generated"
  indent_size: 4
  add_access_modifiers: true
  enable_type_inference: true
  debug_mode: false

plugins:
  enabled:
    - comment_preserver
    - type_annotation
  paths: []
```

### 性能优化

```python
from pythva import convert_with_optimization

# 使用缓存和优化的转换
optimized_result = convert_with_optimization(python_code, use_enhanced=True)
```

### 插件系统

```python
from pythva import get_plugin_manager

# 获取插件管理器
plugin_manager = get_plugin_manager()

# 列出可用插件
plugins = plugin_manager.list_plugins()
for plugin in plugins:
    print(f"{plugin['name']}: {plugin['description']}")
```

### Web界面

```bash
# 启动Web演示界面
pythva-web --host 127.0.0.1 --port 5000

# 然后访问 http://127.0.0.1:5000
```

## 🐳 Docker使用

```bash
# 构建镜像
docker build -t pythva .

# 运行命令行版本
docker run --rm -v $(pwd)/examples:/app/examples pythva convert /app/examples/basic_example.py

# 运行Web版本
docker-compose up
```

## 🔧 开发和调试

### 运行测试

```bash
# 运行所有测试
python -m pytest pythva/test_converter.py -v

# 运行单个测试
python -m pytest pythva/test_converter.py::TestPythvaConverter::test_basic_class_conversion -v
```

### 调试模式

```python
from pythva import get_error_reporter

# 启用调试模式
reporter = get_error_reporter()
# 现在会输出详细的调试信息
```

## 📚 示例文件

项目包含多个示例文件：

- `examples/basic_example.py` - 基础类和方法演示
- `examples/advanced_example.py` - 高级特性和类型注解
- `examples/oop_example.py` - 面向对象编程演示
- `examples/data_structures_example.py` - 数据结构和算法
- `examples/async_decorator_example.py` - 异步编程和装饰器

## 🌍 多语言支持

```python
from pythva.i18n import get_translator, set_global_language

# 设置语言
set_global_language('zh_CN')  # 中文
set_global_language('en')     # 英文
set_global_language('es')     # 西班牙语

# 获取翻译器
translator = get_translator('fr')  # 法语
message = translator.translate('conversion_completed')
```

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 📄 许可证

MIT License - 详见[LICENSE](LICENSE)文件

## 🆘 获取帮助

- 📖 完整文档：https://pythva.readthedocs.io/
- 🐛 报告问题：https://github.com/pythva/pythva/issues
- 💬 讨论交流：https://github.com/pythva/pythva/discussions
- 📧 联系我们：contact@pythva.org

---

**享受Python和Java双重体验！** 🎉