#!/usr/bin/env python3
"""
Pythva Web演示界面
提供基于Flask的Web界面来演示转换功能
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from .core import convert_python_to_java_style
from .mapper import convert_with_mapping
from .config import get_conversion_config
from .errors import get_error_reporter, reset_error_reporter


# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'pythva-demo-secret-key'


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """转换代码"""
    try:
        data = request.get_json()
        python_code = data.get('code', '')
        use_enhanced = data.get('enhanced', False)

        if not python_code.strip():
            return jsonify({
                'success': False,
                'error': '请输入Python代码'
            })

        # 重置错误报告器
        reset_error_reporter()

        # 执行转换
        if use_enhanced:
            converted_code = convert_with_mapping(python_code)
        else:
            converted_code = convert_python_to_java_style(python_code)

        # 获取错误报告
        error_reporter = get_error_reporter()

        return jsonify({
            'success': True,
            'converted_code': converted_code,
            'errors': len(error_reporter.errors),
            'warnings': len(error_reporter.warnings)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'转换失败: {str(e)}'
        })


@app.route('/examples')
def get_examples():
    """获取示例代码"""
    examples = {
        'basic_class': '''class Calculator:
    def __init__(self, initial_value=0):
        self.result = initial_value

    def add(self, a, b):
        return a + b

    def calculate(self):
        return self.result * 2''',

        'data_processor': '''from typing import List

class DataProcessor:
    def __init__(self, name: str):
        self.name = name
        self.data: List[int] = []

    def process_data(self) -> int:
        return sum(self.data)

    def add_item(self, item: int):
        self.data.append(item)''',

        'advanced': '''class AdvancedCalculator:
    def __init__(self):
        self.history = []

    def power(self, base, exponent):
        result = base ** exponent
        self.history.append(f"{base}^{exponent} = {result}")
        return result

    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b'''
    }

    return jsonify(examples)


@app.route('/config')
def get_config():
    """获取当前配置"""
    config = get_conversion_config()
    return jsonify({
        'output_style': config.output_style,
        'add_package_declaration': config.add_package_declaration,
        'package_name': config.package_name,
        'default_type': config.default_type,
        'indent_size': config.indent_size,
        'debug_mode': config.debug_mode
    })


def create_templates():
    """创建HTML模板"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)

    index_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pythva - Python到Java风格转换器演示</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .converter {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        .converter-tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }

        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
        }

        .tab:hover {
            background: #e9ecef;
        }

        .tab.active {
            background: white;
            border-bottom-color: #007bff;
            color: #007bff;
        }

        .editor-container {
            display: flex;
            height: 500px;
        }

        .editor-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .editor-header {
            padding: 10px 15px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            font-weight: bold;
        }

        .editor {
            flex: 1;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
            outline: none;
            resize: none;
            border: none;
            background: #2d3748;
            color: #e2e8f0;
        }

        .python-editor {
            border-right: 1px solid #4a5568;
        }

        .toolbar {
            padding: 15px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background: #007bff;
            color: white;
        }

        .btn-primary:hover {
            background: #0056b3;
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #545b62;
        }

        .checkbox {
            margin-left: 10px;
        }

        .status {
            margin-left: auto;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
        }

        .status.success {
            background: #d4edda;
            color: #155724;
        }

        .status.error {
            background: #f8d7da;
            color: #721c24;
        }

        .loading {
            display: none;
            margin-left: 10px;
        }

        .examples {
            max-height: 300px;
            overflow-y: auto;
            margin-top: 20px;
        }

        .example-item {
            background: white;
            margin-bottom: 10px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .example-header {
            padding: 10px 15px;
            background: #f8f9fa;
            cursor: pointer;
            font-weight: bold;
        }

        .example-code {
            padding: 15px;
            background: #2d3748;
            color: #e2e8f0;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            display: none;
        }

        @media (max-width: 768px) {
            .editor-container {
                flex-direction: column;
                height: auto;
            }

            .python-editor {
                border-right: none;
                border-bottom: 1px solid #4a5568;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Pythva</h1>
            <p>Python到Java风格转换器 - 体验双语编程魅力</p>
        </div>

        <div class="converter">
            <div class="converter-tabs">
                <div class="tab active" onclick="switchTab('converter')">在线转换</div>
                <div class="tab" onclick="switchTab('examples')">示例代码</div>
            </div>

            <div id="converter-tab" class="tab-content">
                <div class="editor-container">
                    <div class="editor-panel">
                        <div class="editor-header">Python代码</div>
                        <textarea class="editor python-editor" id="python-code" placeholder="请输入Python代码..."></textarea>
                    </div>
                    <div class="editor-panel">
                        <div class="editor-header">Java风格代码</div>
                        <textarea class="editor" id="java-code" placeholder="转换结果将在这里显示..." readonly></textarea>
                    </div>
                </div>

                <div class="toolbar">
                    <button class="btn btn-primary" onclick="convertCode()">转换代码</button>
                    <button class="btn btn-secondary" onclick="clearAll()">清空</button>
                    <label class="checkbox">
                        <input type="checkbox" id="enhanced-mode"> 增强模式
                    </label>
                    <div class="status" id="status"></div>
                    <div class="loading" id="loading">转换中...</div>
                </div>
            </div>

            <div id="examples-tab" class="tab-content" style="display: none;">
                <div class="examples" id="examples-container">
                    <!-- 示例代码将在这里动态加载 -->
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentTab = 'converter';

        function switchTab(tabName) {
            currentTab = tabName;

            // 更新标签状态
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');

            // 更新内容显示
            document.getElementById('converter-tab').style.display =
                tabName === 'converter' ? 'block' : 'none';
            document.getElementById('examples-tab').style.display =
                tabName === 'examples' ? 'block' : 'none';

            if (tabName === 'examples') {
                loadExamples();
            }
        }

        async function convertCode() {
            const pythonCode = document.getElementById('python-code').value;
            const enhancedMode = document.getElementById('enhanced-mode').checked;

            if (!pythonCode.trim()) {
                showStatus('请输入Python代码', 'error');
                return;
            }

            showStatus('转换中...', 'loading');

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: pythonCode,
                        enhanced: enhancedMode
                    })
                });

                const result = await response.json();

                if (result.success) {
                    document.getElementById('java-code').value = result.converted_code;
                    showStatus(`转换完成 (${result.errors}错误, ${result.warnings}警告)`, 'success');
                } else {
                    showStatus(result.error, 'error');
                }
            } catch (error) {
                showStatus('网络错误，请稍后重试', 'error');
            }
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            const loading = document.getElementById('loading');

            status.textContent = message;
            loading.style.display = type === 'loading' ? 'block' : 'none';

            status.className = 'status ' + type;
        }

        function clearAll() {
            document.getElementById('python-code').value = '';
            document.getElementById('java-code').value = '';
            showStatus('');
        }

        async function loadExamples() {
            try {
                const response = await fetch('/examples');
                const examples = await response.json();

                const container = document.getElementById('examples-container');

                for (const [key, code] of Object.entries(examples)) {
                    const exampleDiv = document.createElement('div');
                    exampleDiv.className = 'example-item';

                    exampleDiv.innerHTML = `
                        <div class="example-header" onclick="toggleExample('${key}')">
                            ${key.replace('_', ' ').toUpperCase()}
                        </div>
                        <div class="example-code" id="example-${key}">
                            <pre>${escapeHtml(code)}</pre>
                            <button onclick="useExample('${key}')">使用此示例</button>
                        </div>
                    `;

                    container.appendChild(exampleDiv);
                }
            } catch (error) {
                console.error('加载示例失败:', error);
            }
        }

        function toggleExample(exampleId) {
            const codeDiv = document.getElementById(`example-${exampleId}`);
            codeDiv.style.display = codeDiv.style.display === 'none' ? 'block' : 'none';
        }

        function useExample(exampleId) {
            // 这里需要从服务器获取示例代码
            fetch('/examples')
                .then(response => response.json())
                .then(examples => {
                    document.getElementById('python-code').value = examples[exampleId];
                    switchTab('converter');
                });
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // 快捷键支持
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                convertCode();
            }
        });

        // 初始化
        document.addEventListener('DOMContentLoaded', function() {
            // 添加一些示例代码
            document.getElementById('python-code').value = `class HelloWorld:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

# 使用示例
obj = HelloWorld("World")
print(obj.greet())`;
        });
    </script>
</body>
</html>'''

    with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)


def run_web_demo(host='127.0.0.1', port=5000, debug=False):
    """运行Web演示"""
    # 创建模板
    create_templates()

    print(f"🚀 Pythva Web演示启动中...")
    print(f"📍 访问地址: http://{host}:{port}")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    print("-" * 50)

    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Pythva Web演示')
    parser.add_argument('--host', default='127.0.0.1', help='监听主机')
    parser.add_argument('--port', type=int, default=5000, help='监听端口')
    parser.add_argument('--debug', action='store_true', help='开启调试模式')

    args = parser.parse_args()

    run_web_demo(host=args.host, port=args.port, debug=args.debug)