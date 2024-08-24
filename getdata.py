import pyodbc

# 設定連接字串
server = '192.168.1.110,1433'  # IP 地址和端口
database = 'master'  # 或者你的具體資料庫名稱
username = 'sa'
password = 'MyP@ssw0rd123!'
driver = '{ODBC Driver 17 for SQL Server}'

# 連接到 SQL Server
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    connection = pyodbc.connect(connection_string)
    print("Connection successful!")
    
    # 創建游標
    cursor = connection.cursor()

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
        print(f"ID: {row.id}")
        print(f"USD Rate: {row.usd_rate}")
        print(f"JPY Rate: {row.jpy_rate}")
        print(f"GBP Rate: {row.gbp_rate}")
        print(f"AUD Rate: {row.aud_rate}")
        print(f"Timestamp: {row.timestamp}")
    else:
        print("No data found.")

    # 關閉連接
    cursor.close()
    connection.close()
except pyodbc.Error as e:
    print(f"Error: {e}")
