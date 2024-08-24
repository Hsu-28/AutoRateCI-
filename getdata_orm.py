from sqlalchemy import create_engine, Column, Integer, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 設定資料庫連接
server = '192.168.1.110,1433'
database = 'master'
username = 'sa'
password = 'MyP@ssw0rd123!'
driver = 'ODBC Driver 17 for SQL Server'

# 連接字串
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

# 建立引擎
engine = create_engine(connection_string)

# 創建一個 Base 類來定義 ORM 類
Base = declarative_base()

# 定義一個與 exchange_rates 表對應的 ORM 類
class ExchangeRate(Base):
    __tablename__ = 'exchange_rates'

    id = Column(Integer, primary_key=True)
    usd_rate = Column(Numeric(18, 6), nullable=False)
    jpy_rate = Column(Numeric(18, 6), nullable=False)
    gbp_rate = Column(Numeric(18, 6), nullable=False)
    aud_rate = Column(Numeric(18, 6), nullable=False)
    timestamp = Column(DateTime, nullable=False)

# 創建 Session 類別
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 查詢最新一條數據
    latest_rate = session.query(ExchangeRate).order_by(ExchangeRate.timestamp.desc()).first()

    # 輸出結果
    if latest_rate:
        print(f"ID: {latest_rate.id}")
        print(f"USD Rate: {latest_rate.usd_rate}")
        print(f"JPY Rate: {latest_rate.jpy_rate}")
        print(f"GBP Rate: {latest_rate.gbp_rate}")
        print(f"AUD Rate: {latest_rate.aud_rate}")
        print(f"Timestamp: {latest_rate.timestamp}")
    else:
        print("No data found.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # 關閉 Session
    session.close()
