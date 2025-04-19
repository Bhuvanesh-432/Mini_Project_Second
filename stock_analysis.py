import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# ---- 1. Load the data FIRST ----
@st.cache_data

def load_data():
    df = pd.read_csv("cleaned_stock_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['symbol', 'date'], inplace=True)

    try:
        sector_df = pd.read_csv("sector_mapping.csv")

        if 'sector' in df.columns:
            df = df.drop(columns=['sector'])

        df = pd.merge(df, sector_df, on='symbol', how='left')

        if 'sector' not in df.columns or df['sector'].isnull().all():
            df['sector'] = "Unknown"

    except FileNotFoundError:
        st.warning("⚠️ sector_mapping.csv not found. Proceeding without sector filter.")
        df['sector'] = "Unknown"

    return df

# ✅ Load the dataframe BEFORE using it
df = load_data()

# ---- 2. Sidebar filters ----
st.sidebar.title("📊 Stock Analysis Dashboard")
selected_symbols = st.sidebar.multiselect(
    "Select Stocks",
    sorted(df['symbol'].unique()),
    default=sorted(df['symbol'].unique())
)

selected_sectors = st.sidebar.multiselect(
    "Select Sectors",
    sorted(df['sector'].dropna().unique()),
    default=sorted(df['sector'].dropna().unique())
)

# ---- 3. Filter the main DataFrame ----
df = df[df['symbol'].isin(selected_symbols) & df['sector'].isin(selected_sectors)]

# ---- 1. Volatility Analysis ----
st.header("1. Volatility Analysis")
df['daily_return'] = df.groupby('symbol')['close'].pct_change()
volatility = df.groupby('symbol')['daily_return'].std().reset_index().rename(columns={'daily_return': 'volatility'})
top_volatility = volatility.sort_values(by='volatility', ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_volatility, x='symbol', y='volatility', ax=ax1, palette='Reds_r')
ax1.set_title('Top 10 Most Volatile Stocks')
st.pyplot(fig1)

# ---- 2. Cumulative Return Over Time ----
st.header("2. Cumulative Return Over Time")
df['cum_return'] = (1 + df['daily_return']).groupby(df['symbol']).cumprod()
cum_last = df.groupby('symbol')['cum_return'].last().sort_values(ascending=False)
top_5_cum = cum_last.head(5).index.tolist()

fig2, ax2 = plt.subplots(figsize=(12, 5))
for symbol in top_5_cum:
    symbol_df = df[df['symbol'] == symbol]
    ax2.plot(symbol_df['date'], symbol_df['cum_return'], label=symbol)
ax2.legend()
ax2.set_title("Top 5 Cumulative Return Performers")
st.pyplot(fig2)

# ---- 3. Sector-wise Performance ----
st.header("3. Sector-wise Performance")
yearly_return = df.groupby('symbol').agg(first=('close', 'first'), last=('close', 'last')).reset_index()
yearly_return['yearly_return'] = (yearly_return['last'] - yearly_return['first']) / yearly_return['first'] * 100
sector_map = df[['symbol', 'sector']].drop_duplicates()
yearly_sector = pd.merge(yearly_return, sector_map, on='symbol')
sector_avg = yearly_sector.groupby('sector')['yearly_return'].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(12, 5))
sns.barplot(data=sector_avg, x='sector', y='yearly_return', ax=ax3, palette='viridis')
ax3.set_title("Average Yearly Return by Sector")
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
st.pyplot(fig3)

# ---- 4. Stock Price Correlation ----
st.header("4. Stock Price Correlation")
close_pivot = df.pivot(index='date', columns='symbol', values='close')
returns = close_pivot.pct_change().dropna()
corr_matrix = returns.corr()

fig4, ax4 = plt.subplots(figsize=(16, 12))
sns.heatmap(corr_matrix, cmap='coolwarm', ax=ax4)
ax4.set_title("Stock Price Correlation Heatmap")
st.pyplot(fig4)

# ---- 5. Monthly Top Gainers and Losers ----
st.header("5. Monthly Gainers and Losers")
df['month'] = df['date'].dt.to_period('M')
monthly = df.groupby(['symbol', 'month']).agg(first=('close', 'first'), last=('close', 'last')).reset_index()
monthly['return_pct'] = (monthly['last'] - monthly['first']) / monthly['first'] * 100

months = monthly['month'].unique()
selected_month = st.selectbox("Select Month", sorted(months.astype(str)))
month_data = monthly[monthly['month'].astype(str) == selected_month]
top_5 = month_data.sort_values(by='return_pct', ascending=False).head(5)
bottom_5 = month_data.sort_values(by='return_pct').head(5)

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Top 5 Gainers in {selected_month}")
    fig5a, ax5a = plt.subplots()
    sns.barplot(data=top_5, x='symbol', y='return_pct', ax=ax5a, palette='Greens_r')
    ax5a.set_title("Top 5 Gainers")
    st.pyplot(fig5a)

with col2:
    st.subheader(f"Top 5 Losers in {selected_month}")
    fig5b, ax5b = plt.subplots()
    sns.barplot(data=bottom_5, x='symbol', y='return_pct', ax=ax5b, palette='Reds_r')
    ax5b.set_title("Top 5 Losers")
    st.pyplot(fig5b)