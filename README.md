# Cryptocurrency Tracker

A live cryptocurrency tracker dashboard built using Streamlit, Python, and CoinMarketCap API. This application fetches real-time cryptocurrency data, visualizes key metrics such as price, market cap, 24h change, and more. The dashboard auto-refreshes the data and generates insightful visualizations like line plots, scatter plots, pie charts, and histograms.

## Features

- **Live Cryptocurrency Data**: Fetches the top 50 cryptocurrencies and displays real-time data such as price, market cap, volume, and percentage change.
- **Auto-refresh**: The dashboard updates every few minutes to keep the data current.
- **Data Visualization**: Includes a variety of visualizations such as line plots, pie charts, scatter plots, histograms, and bar charts to help analyze the data.
- **Export to Excel**: The live cryptocurrency data can be downloaded in an Excel file.
  
## Technologies Used

- **Streamlit**: For building the interactive dashboard.
- **Python**: For scripting and data processing.
- **Requests**: For API interaction.
- **Matplotlib**: For plotting graphs.
- **CoinMarketCap API**: For fetching live cryptocurrency data.
- **.env**: To securely store the API key.
  
## Requirements

Before running the application, ensure you have Python installed. You will also need to install the required dependencies.

### Step 1: Clone the repository

```bash
git clone https://github.com/09-prince/crypto-tracker.git
cd crypto-tracker
