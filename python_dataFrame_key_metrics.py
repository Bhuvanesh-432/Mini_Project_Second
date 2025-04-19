import mysql.connector
import pandas as pd

def fetch_stock_data():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'stock_data'
    }

    conn = mysql.connector.connect(**config)

    # Read the full stock table
    query = "SELECT symbol, date, close, volume FROM stocks;"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Convert to datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['symbol', 'date'], inplace=True)
    return df

def analyze_market(df):
    # Calculate yearly return: (last_close - first_close) / first_close
    returns = (
        df.groupby('symbol')
        .agg(first_close=('close', 'first'), last_close=('close', 'last'), avg_volume=('volume', 'mean'))
        .reset_index()
    )
    returns['yearly_return'] = (returns['last_close'] - returns['first_close']) / returns['first_close'] * 100

    # Top 10 green & loss stocks
    top_10_green = returns.sort_values(by='yearly_return', ascending=False).head(10)
    top_10_loss = returns.sort_values(by='yearly_return').head(10)

    # Market summary
    green_count = (returns['yearly_return'] > 0).sum()
    red_count = (returns['yearly_return'] <= 0).sum()
    avg_price = df['close'].mean()
    avg_volume = df['volume'].mean()

    market_summary = {
        'green_stocks': green_count,
        'red_stocks': red_count,
        'avg_price': round(avg_price, 2),
        'avg_volume': int(avg_volume)
    }

    return top_10_green, top_10_loss, market_summary

# Run everything
df = fetch_stock_data()
top_10_green, top_10_loss, market_summary = analyze_market(df)

print("📈 Top 10 Green Stocks:")
print(top_10_green[['symbol', 'yearly_return']])

print("\n📉 Top 10 Loss Stocks:")
print(top_10_loss[['symbol', 'yearly_return']])

print("\n🧾 Market Summary:")
for k, v in market_summary.items():
    print(f"{k}: {v}")
