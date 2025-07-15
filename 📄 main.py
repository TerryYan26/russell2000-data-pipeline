# main.py

import psycopg2
import requests
import time

# ====================
# PostgreSQL 配置
# ====================
db_params = {
    'dbname': 'your_db_name',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}

# ====================
# IEX Cloud Token
# ====================
IEX_TOKEN = 'YOUR_IEX_CLOUD_API_TOKEN'
IEX_BASE_URL = 'https://cloud.iexapis.com/stable'

# ====================
# 初始化表
# ====================
def init_db():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS realtime_prices (
            id SERIAL PRIMARY KEY,
            ticker TEXT,
            price REAL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical_prices (
            id SERIAL PRIMARY KEY,
            ticker TEXT,
            date DATE,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume BIGINT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 数据库表已创建")

# ====================
# 获取数据
# ====================
def fetch_realtime_price(ticker):
    url = f"{IEX_BASE_URL}/stock/{ticker}/quote?token={IEX_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("latestPrice")
    else:
        print(f"⚠️ 获取实时价格失败: {ticker} - {response.text}")
        return None

def fetch_historical_data(ticker, range_period="1m"):
    url = f"{IEX_BASE_URL}/stock/{ticker}/chart/{range_period}?token={IEX_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ 获取历史数据失败: {ticker} - {response.text}")
        return []

# ====================
# 保存数据
# ====================
def save_realtime_price_pg(ticker, price):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO realtime_prices (ticker, price) VALUES (%s, %s)",
        (ticker, price)
    )
    conn.commit()
    cursor.close()
    conn.close()

def save_historical_data_pg(ticker, hist_data):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    for day in hist_data:
        cursor.execute(
            '''
            INSERT INTO historical_prices (ticker, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                ticker,
                day['date'],
                day['open'],
                day['high'],
                day['low'],
                day['close'],
                day['volume']
            )
        )
    conn.commit()
    cursor.close()
    conn.close()

# ====================
# 主流程
# ====================
def main():
    init_db()
    tickers = ["AAPL", "MSFT", "TSLA"]
    for ticker in tickers:
        print(f"🔎 处理: {ticker}")

        price = fetch_realtime_price(ticker)
        if price:
            save_realtime_price_pg(ticker, price)
            print(f"✅ 实时价格已保存: {price}")

        hist_data = fetch_historical_data(ticker)
        if hist_data:
            save_historical_data_pg(ticker, hist_data)
            print(f"✅ 历史数据已保存")

        time.sleep(1)
    print("🎉 完成")

if __name__ == "__main__":
    main()
