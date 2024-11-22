# Import library
import requests
import pandas as pd
import streamlit as st
import time
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Get API key form the .env
load_dotenv()
API_KEY = os.getenv("API_KEY")


# API URL and headers
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

# Parameters for fetching top 50 cryptocurrencies
PARAMETERS = {
    "start": "1",  # Start at rank 1
    "limit": "50",  # Fetch top 50 cryptocurrencies
    "convert": "USD",  # Convert prices to USD
}

# Function to fetch and process cryptocurrency data
def fetch_crypto_data():
    try:
        response = requests.get(API_URL, headers=HEADERS, params=PARAMETERS)
        response.raise_for_status()
        data = response.json()

        # Process the data
        crypto_data = []
        for item in data["data"]:
            crypto_data.append({
                "Name": item["name"],
                "Symbol": item["symbol"],
                "Price (USD)": round(item["quote"]["USD"]["price"], 2),
                "Market Cap": round(item["quote"]["USD"]["market_cap"], 2),
                "24h Volume": round(item["quote"]["USD"]["volume_24h"], 2),
                "24h Change (%)": round(item["quote"]["USD"]["percent_change_24h"], 2),
            })

        # Convert to a DataFrame
        df = pd.DataFrame(crypto_data)
        return df

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Streamlit App
st.title("Live Cryptocurrency Tracker")
st.sidebar.header("Settings")
refresh_interval = st.sidebar.slider("Auto Refresh Interval (seconds)", 60, 300, 300, 30)

st.markdown(
    """
    **Top 50 Cryptocurrencies**:
    This dashboard shows live cryptocurrency data updated automatically every few minutes.
    """
)


def plot(df):
    # get the top 5
    df = df.head(5)


    # Plot 1: Line plot for Price (USD)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df['Name'], df['Price (USD)'], label="Price (USD)", color='b')
    ax1.set_title("Cryptocurrency Price Comparison (USD)")
    ax1.set_ylabel("Price (USD)")
    ax1.set_xlabel("Cryptocurrency")
    ax1.legend()


    # Plot 2: Pie chart for Market Cap Distribution
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(df['Market Cap'], labels=df['Name'], autopct='%1.1f%%', startangle=90,
            colors=['gold', 'lightblue', 'lightgreen', 'orange', 'pink'])
    ax2.set_title('Market Cap Distribution')


    # Plot 3: Line plot for 24h Change (%)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(df['Name'], df['24h Change (%)'], marker='o', linestyle='-', color='green', label='24h Change (%)')
    ax3.set_title('24h Price Change Comparison (%)')
    ax3.set_xlabel('Cryptocurrency')
    ax3.set_ylabel('24h Change (%)')
    ax3.grid(True)
    ax3.legend()


    # Plot 4: Scatter plot for Price vs Market Cap
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.scatter(df['Price (USD)'], df['Market Cap'], color='blue')
    ax4.set_title('Price vs Market Cap of Cryptocurrencies')
    ax4.set_xlabel('Price (USD)')
    ax4.set_ylabel('Market Cap')
    ax4.set_yscale('log')  # Using logarithmic scale for market cap to visualize more effectively
    ax4.legend(['Market Cap'], loc='upper left')



    # Plot 5: Histogram for 24h Change (%) Distribution
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    ax5.hist(df['24h Change (%)'], bins=10, color='orange', edgecolor='black')
    ax5.set_title('Distribution of 24h Percentage Change')
    ax5.set_xlabel('24h Change (%)')
    ax5.set_ylabel('Frequency')
    ax5.legend(['24h Change (%)'], loc='upper right')


    # Plot 6: Plot a bar graph
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    ax6.bar(df['Name'], df['Price (USD)'], color='lightblue')
    ax6.set_title('Cryptocurrency Price Comparison (USD)')
    ax6.set_xlabel('Cryptocurrency')
    ax6.set_ylabel('Price (USD)')
    ax6.set_xticklabels(df['Name'], rotation=45)


    # Boxplot for get the 24h Change Distribution
    fig7, ax7 = plt.subplots(figsize=(10, 6))
    ax7.boxplot(df['24h Change (%)'], vert=False, patch_artist=True, boxprops=dict(facecolor="skyblue", color="blue"))
    ax7.set_title('24h Change Distribution')
    ax7.set_xlabel('24h Change (%)')

    # Display the plots in the Streamlit app
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)
    st.pyplot(fig5)
    st.pyplot(fig6)
    st.pyplot(fig7)

# Auto-update mechanism
placeholder = st.empty()

while True:
    with placeholder.container():
        df = fetch_crypto_data()

        if not df.empty:
            # Display full data
            st.subheader("Top 50 Cryptocurrency Data")
            st.dataframe(df)

            # Perform basic analysis
            top_5 = df.nlargest(5, "Market Cap")[["Name", "Market Cap"]]
            average_price = df["Price (USD)"].mean()
            highest_change = df["24h Change (%)"].max()
            lowest_change = df["24h Change (%)"].min()

            st.subheader("Analysis")
            st.markdown("### Top 5 Cryptocurrencies by Market Cap")
            st.table(top_5)

            st.markdown(f"**Average Price of Top 50 Cryptocurrencies:** ${average_price:.2f}")
            st.markdown(f"**Highest 24h Percentage Change:** {highest_change:.2f}%")
            st.markdown(f"**Lowest 24h Percentage Change:** {lowest_change:.2f}%")

            # Save the data to an Excel file
            excel_filename = "live_crypto_data.xlsx"
            df.to_excel(excel_filename, index=False)
            st.success(f"Data saved to `{excel_filename}`")

            # Here add a plot function to display the graph
            plot(df)




    # Wait for the refresh interval
    time.sleep(refresh_interval)
