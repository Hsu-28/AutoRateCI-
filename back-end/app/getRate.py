import time
import requests
import pyodbc
from datetime import datetime

# 設置 API 端點 URL
url = 'https://v6.exchangerate-api.com/v6/97603bbe0aa603ea1362d19a/latest/TWD'

# 設置 SQL Server 連接字符串
server = '192.168.1.110,1433'
database = 'master'  # 假設在 master 資料庫中創建表格，但你可以根據需要修改
username = 'sa'
password = 'MyP@ssw0rd123!'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def create_table_if_not_exists():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='exchange_rates' AND xtype='U')
        BEGIN
            CREATE TABLE exchange_rates (
                id INT IDENTITY(1,1) PRIMARY KEY,
                usd_rate DECIMAL(18, 6) NOT NULL,
                jpy_rate DECIMAL(18, 6) NOT NULL,
                gbp_rate DECIMAL(18, 6) NOT NULL,
                aud_rate DECIMAL(18, 6) NOT NULL,
                timestamp DATETIME NOT NULL
            );
        END
        ''')
        conn.commit()
        print("表格檢查和創建成功。")
    except pyodbc.Error as e:
        print(f"創建表格時發生錯誤: {e}")
    finally:
        cursor.close()
        conn.close()

def fetch_exchange_rates():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        time_last_update_utc = data.get('time_last_update_utc', 'N/A')
        conversion_rates = data.get('conversion_rates', {})

        # 獲取台幣（TWD）的匯率
        twd_rate = conversion_rates.get('TWD', None)
        if not twd_rate:
            print("台幣（TWD）匯率未找到")
            return None

        # 計算其他貨幣的匯率（以每單位台幣為基準）
        exchange_rates = {
            '美元': round(conversion_rates.get('USD', 0) / twd_rate, 6) if conversion_rates.get('USD') else None,
            '日元': round(conversion_rates.get('JPY', 0) / twd_rate, 6) if conversion_rates.get('JPY') else None,
            '英鎊': round(conversion_rates.get('GBP', 0) / twd_rate, 6) if conversion_rates.get('GBP') else None,
            '澳幣': round(conversion_rates.get('AUD', 0) / twd_rate, 6) if conversion_rates.get('AUD') else None
        }

        timestamp = datetime.strptime(time_last_update_utc, '%a, %d %b %Y %H:%M:%S %z')
        
        return {
            'usd_rate': exchange_rates['美元'],
            'jpy_rate': exchange_rates['日元'],
            'gbp_rate': exchange_rates['英鎊'],
            'aud_rate': exchange_rates['澳幣'],
            'timestamp': timestamp
        }

    except requests.exceptions.RequestException as e:
        print(f"獲取數據時發生錯誤: {e}")
        return None

def insert_data_to_db(data):
    if data:
        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            query = '''
            INSERT INTO exchange_rates (usd_rate, jpy_rate, gbp_rate, aud_rate, timestamp)
            VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (data['usd_rate'], data['jpy_rate'], data['gbp_rate'], data['aud_rate'], data['timestamp']))
            conn.commit()
            print("數據插入成功。")

        except pyodbc.Error as e:
            print(f"插入數據時發生錯誤: {e}")

        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    # 初次立即執行
    create_table_if_not_exists()
    data = fetch_exchange_rates()
    insert_data_to_db(data)
    
    # 每12小時執行一次
    while True:
        time.sleep(43200)
        data = fetch_exchange_rates()
        insert_data_to_db(data)
