from flask import Flask, jsonify
from flask_restful import Api, Resource
import pyodbc
from flask_cors import CORS  # 導入 CORS

app = Flask(__name__)
api = Api(app)

# 配置 CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # 允許所有來源

# 配置 SQL Server 連接
def get_db_connection():
    server = '192.168.1.110,1433'  # IP 地址和端口
    database = 'master'  # 資料庫名稱
    username = 'sa'
    password = 'MyP@ssw0rd123!'
    driver = '{ODBC Driver 17 for SQL Server}'

    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    return pyodbc.connect(connection_string)

class ExchangeRateResource(Resource):
    def get(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # 執行查詢
            query = '''
            SELECT TOP 1 *
            FROM exchange_rates
            ORDER BY timestamp DESC;
            '''
            cursor.execute(query)
            
            # 取得結果
            row = cursor.fetchone()
            
            if row:
                result = {
                    "id": row.id,
                    "usd_rate": str(row.usd_rate),  # Decimal 轉為字串
                    "jpy_rate": str(row.jpy_rate),  # Decimal 轉為字串
                    "gbp_rate": str(row.gbp_rate),  # Decimal 轉為字串
                    "aud_rate": str(row.aud_rate),  # Decimal 轉為字串
                    "timestamp": row.timestamp.isoformat()  # Datetime 轉為 ISO 格式字串
                }
                return jsonify(result)
            else:
                return jsonify({"message": "No data found."})
        
        except pyodbc.Error as e:
            return jsonify({"error": str(e)})
        
        finally:
            cursor.close()
            connection.close()

# 註冊 API 路由
api.add_resource(ExchangeRateResource, '/latest-exchange-rate')

if __name__ == '__main__':
    app.run(debug=True)
