# Mini_Project_Second
Data-Driven Stock Analysis
Project Title:
Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends

Domain:
Finance / Data Analytics

Skills Gained:
Pandas, Python, Power BI, Streamlit, SQL, Statistics, Data Organizing, Cleaning, and Visualizing

Problem Statement:
The Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of Nifty 50 stocks' performance over the past year. The project analyzes daily stock data, including open, close, high, low, and volume values. It involves cleaning and processing the data, generating key performance insights, and visualizing top-performing and worst-performing stocks in terms of price changes. Interactive dashboards using Streamlit and Power BI enable investors, analysts, and enthusiasts to make informed decisions based on performance trends.

Business Use Cases:

Stock Performance Ranking: Identify the top 10 best-performing (green) and worst-performing (red) stocks.

Market Overview: Summarize the market with average performance and green/red stock ratios.

Investment Insights: Highlight consistent gainers and significant decliners.

Decision Support: Provide insights on average prices, volatility, and stock behavior.

Approach:
1. Data Extraction and Transformation:

Extract data from YAML files organized by month and date.

Convert to CSV format, organized by stock symbol.

Result: 50 cleaned CSV files (one per symbol).

2. Data Analysis and Visualization:

Top 10 Green and Red Stocks:

Sort by yearly return and select top/bottom 10.

Market Summary:

Count green vs red stocks.

Calculate average price and volume.

3. Volatility Analysis:

Calculate daily returns: (Close - Prev Close) / Prev Close.

Compute standard deviation for each stock.

Visualize top 10 most volatile stocks using bar chart.

4. Cumulative Return Over Time:

Compute cumulative return for each stock.

Visualize top 5 stocks using a line chart.

5. Sector-Wise Performance:

Map each stock to its sector (via CSV).

Calculate average yearly return per sector.

Visualize using bar chart.

6. Stock Price Correlation:

Calculate correlation matrix for closing prices.

Visualize relationships with a heatmap.

7. Monthly Gainers and Losers:

Calculate monthly return for each stock.

Identify top 5 gainers and losers per month.

Display 12 bar charts (one for each month).

Dataset:
Extracted from YAML files and organized as CSV by symbol.

Results:

Fully functional dashboard showing annual stock performance.

Insightful market overview with performance trends.

Interactive Power BI and Streamlit dashboards for user-friendly analysis.

Technical Tags:
Languages: PythonDatabase: MySQL/PostgreSQLVisualization Tools: Streamlit, Power BILibraries: Pandas, Matplotlib, SQLAlchemy

Project Deliverables:

SQL Database: Contains cleaned and structured stock data.

Python Scripts: For data extraction, transformation, and analysis.

Power BI Dashboard: For visualization of key insights.

Streamlit Application: For interactive, real-time analysis.

Project Documentation & Presentation: For reporting and stakeholder review.
