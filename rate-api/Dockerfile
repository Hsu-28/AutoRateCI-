# 使用官方 Python 3.8 的基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖和 ODBC 驱动
RUN apt-get update && \
    apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg2 \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# 添加 Microsoft 的包签名密钥和包存储库
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# # 更新包列表并安装 Microsoft ODBC Driver for SQL Server
# RUN apt-get update && \
#     ACCEPT_EULA=Y apt-get install -y msodbcsql17

# 复制 requirements.txt 并安装 Python 依赖项
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码到容器中的 /app 目录
COPY . /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动 getRate.py 脚本
CMD ["python", "/app/getRate.py"]
