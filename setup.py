#!/usr/bin/env python3
"""
Pythva安装脚本
用于打包和分发Pythva项目
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# 读取版本信息
version_file = (this_directory / "__init__.py").read_text(encoding='utf-8')
version_line = [line for line in version_file.split('\n') if '__version__' in line]
if version_line:
    __version__ = version_line[0].split('=')[1].strip().strip('"\'')
else:
    __version__ = "1.0.0"

setup(
    name="pythva",
    version=__version__,
    author="Yaku Makki",
    author_email="yakumakki947@hotmail.com",
    description="Python到Java风格代码转换器 - 让Python代码看起来像Java",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makkichan947/pythva",
    project_urls={
        "Bug Tracker": "https://github.com/makkichan947/pythva/issues",
        "Documentation": "https://pythva.readthedocs.io/",
        "Source Code": "https://github.com/makkichan947/pythva",
    },
    packages=find_packages(include=["pythva", "pythva.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
        ],
        "web": [
            "Flask>=2.0.0",
            "Jinja2>=3.1.0",
        ],
        "all": [
            "PyYAML>=6.0",
            "Flask>=2.0.0",
            "pytest>=7.0.0",
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pythva=pythva.cli:main",
            "pythva-web=pythva.web_demo:run_web_demo",
        ],
    },
    package_data={
        "pythva": [
            "README.md",
            "examples/*",
            "templates/*",
        ],
    },
    include_package_data=True,
    keywords=[
        "python",
        "java",
        "code-generator",
        "transpiler",
        "syntax",
        "converter",
        "pythva"
    ],
    license="MIT",
    platforms=["any"],
    zip_safe=False,
)