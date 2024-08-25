# 使用官方 Nginx 基礎映像
FROM nginx:alpine

# 複製前端文件到 Nginx 預設的靜態文件目錄
COPY . /usr/share/nginx/html

# 暴露 Nginx 默認端口
EXPOSE 80

# 啟動 Nginx
CMD ["nginx", "-g", "daemon off;"]
