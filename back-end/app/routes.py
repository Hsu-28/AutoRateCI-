from flask import Blueprint, jsonify
import pyodbc

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/exchange-rates', methods=['GET'])
def get_exchange_rates():
    # 設定連接字串
    server = 'sqlserver'  # 使用服務名稱而不是 IP 地址
    database = 'master'
    username = 'sa'
    password = 'MyP@ssw0rd123!'
    driver = '{ODBC Driver 17 for SQL Server}'

    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # 嘗試執行查詢
        try:
            query = 'SELECT TOP 1 * FROM exchange_rates ORDER BY timestamp DESC;'
            cursor.execute(query)
            row = cursor.fetchone()

            if row:
                data = {
                    'id': row.id,
                    'usd_rate': row.usd_rate,
                    'jpy_rate': row.jpy_rate,
                    'gbp_rate': row.gbp_rate,
                    'aud_rate': row.aud_rate,
                    'timestamp': row.timestamp.isoformat()
                }
                return jsonify(data)
            else:
                return jsonify({'message': 'No data found'}), 404

        except pyodbc.ProgrammingError as pe:
            # 如果表不存在，創建表並插入初始數據
            if '42S02' in str(pe):
                cursor.execute('''
                    CREATE TABLE exchange_rates (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        usd_rate DECIMAL(18, 6) NOT NULL,
                        jpy_rate DECIMAL(18, 6) NOT NULL,
                        gbp_rate DECIMAL(18, 6) NOT NULL,
                        aud_rate DECIMAL(18, 6) NOT NULL,
                        timestamp DATETIME NOT NULL
                    );
                ''')
                cursor.execute('''
                    INSERT INTO exchange_rates (usd_rate, jpy_rate, gbp_rate, aud_rate, timestamp)
                    VALUES (0.031, 4.5, 0.022, 0.048, '2024-08-23T12:56:00');
                ''')
                connection.commit()
                return jsonify({'message': 'Table created and initial data inserted, but no data found'}), 404
            else:
                return jsonify({'error': str(pe)}), 500

        finally:
            cursor.close()
            connection.close()

    except pyodbc.Error as e:
        return jsonify({'error': str(e)}), 500
