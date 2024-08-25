# AutoRateCI-
Vue/ Flask / Docker /Kubernetes / CI/CD 


## 技術堆疊
- **Vue.js**: 前端框架
- **Flask**: 後端 API
- **Docker**: 容器化應用
- **Kubernetes**: 容器編排
- **CI/CD**: 自動化測試和部署

## 功能
- 查詢最新匯率
- 支援多種貨幣
- 直觀的匯率視覺化展示

## 安裝和運行

### 後端
1. 確保已安裝 Docker 和 Docker Compose。
2. 克隆專案：git clone <repository-url>
3. 進入後端目錄：cd back-end
4. 配置環境變數和資料庫連接。
5. 建立並啟動 Docker 容器：docker-compose up

### 前端
1. 確保已安裝 Node.js 和 npm。
2. 進入前端目錄：cd frontend
3. 安裝依賴：npm install
4. 啟動開發伺服器：npm run dev

## 使用說明
1. 打開瀏覽器並訪問 http://127.0.0.1:5000 查看匯率資訊。
2. 使用提供的 API 進行查詢。

## CI/CD
使用 GitLab CI/CD 自動化測試和部署到 Kubernetes 集群。

