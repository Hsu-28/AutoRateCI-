from flask import Blueprint, jsonify
import pyodbc

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/exchange-rates', methods=['GET'])
def get_exchange_rates():
    # 設定連接字串
    server = '192.168.1.110,1433'
    database = 'my_database'
    username = 'sa'
    password = 'MyP@ssw0rd123!'
    driver = '{ODBC Driver 17 for SQL Server}'

    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = 'SELECT TOP 1 * FROM exchange_rates ORDER BY timestamp DESC;'
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

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

    except pyodbc.Error as e:
        return jsonify({'error': str(e)}), 500
