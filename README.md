# AutoRateCI-
Vue/ Flask / MSSQL / Docker / CI/CD 


## 技術堆疊
- **Vue.js**: 前端框架
- **Flask**: 後端 API
- **MSSQL**: 資料庫應用
- **Docker**: 容器化應用
- **CI/CD**: 自動化測試和部署

## 功能
- 查詢最新匯率
- 支援多種貨幣
- 直觀的匯率視覺化展示


## 安裝和運行

### 後端
1. 確保已安裝 Docker 和 Docker Compose。
2. 進入後端目錄：cd back-end
3. 配置環境變數和資料庫連接。
4. 建立並啟動 Docker 容器：docker-compose up

### 前端
1. 確保已安裝 Node.js 和 npm。
2. 進入前端目錄: cd front-end
3. 啟動開發伺服器：npm run dev
4. 構建前端資源並準備部署：
   使用官方的 Nginx 基礎映像構建 Docker 容器。
   將前端檔案複製到 Nginx 的靜態文件目錄中。
   暴露 Nginx 的預設端口 80 並啟動 Nginx 服務。

## 使用說明
1. 打開瀏覽器並訪問 http://127.0.0.1:80 查看匯率資訊。
2. 需要等待一分鐘容器完全建立完成，python會使用提供的 API 進行匯率查詢並寫入資料庫。

## CI/CD
使用 GitLab CI/CD 自動化測試和部署到。

