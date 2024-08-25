# 使用官方 Python 3.8.3 的基础镜像
FROM python:3.8.3-buster

# 设置工作目录
WORKDIR /app

# 更新包列表并安装必要的系统依赖和 ODBC 驱动
RUN apt-get update && \
    apt-get install -y \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    gnupg2 \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# 添加 Microsoft 的包签名密钥和包存储库
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# 更新包列表并安装 Microsoft ODBC Driver for SQL Server
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# 确认 ODBC 驱动安装成功
RUN echo "[ODBC Driver 17 for SQL Server]" > /etc/odbcinst.ini && \
    echo "Description = Microsoft ODBC Driver 17 for SQL Server" >> /etc/odbcinst.ini && \
    echo "Driver = /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.6.1" >> /etc/odbcinst.ini

# 复制 requirements.txt 并安装 Python 依赖项，包括 pyodbc
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 确认 pyodbc 是否成功安装
RUN python -c "import pyodbc; print('pyodbc installed successfully')"

# 复制应用程序代码到容器中的 /app 目录
COPY . /app

# 设置环境变量
ENV FLASK_APP=/app/app/app.py
ENV FLASK_ENV=production

# 暴露 Flask 默认端口
EXPOSE 5000

# 启动脚本，首先运行 getRate.py，然后启动 Flask
CMD ["bash", "-c", "python /app/app/getRate.py > /app/getRate.log 2>&1 && flask run --host=0.0.0.0"]
