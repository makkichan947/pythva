# Pythva Docker镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHVA_CONFIG=/app/config/pythva.yaml

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY setup.py README.md ./
COPY pythva/ ./pythva/

# 安装Python依赖
RUN pip install --no-cache-dir -e .

# 创建配置目录
RUN mkdir -p /app/config /app/examples /app/cache

# 复制默认配置文件
RUN python -c "from pythva.config import ConfigManager; ConfigManager().create_default_config('/app/config/pythva.yaml')"

# 创建非root用户
RUN useradd --create-home --shell /bin/bash pythva && \
    chown -R pythva:pythva /app
USER pythva

# 暴露端口（用于Web界面）
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from pythva.core import convert_python_to_java_style; print('Pythva is working!')" || exit 1

# 默认启动命令
CMD ["python", "-m", "pythva.cli", "--help"]