import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
data = {
    "Rank": list(range(1, 21)),
    "Company": [
        "AbbVie", "Abbott Laboratories", "Fuji Pharma", "Veru Inc.", "Pulsenmore Ltd.", "Daré Bioscience Inc.",
        "Femasys Inc.", "Aspira Women’s Health", "Palatin Technologies", "Mithra Pharmaceuticals", "The Cooper Companies",
        "Hologic Inc.", "Creative Medical Tech", "Minerva Surgical", "Organon & Co.", "INVO Bioscience",
        "Agile Therapeutics", "Bonzun", "Evofem Biosciences Inc.", "Callitas Therapeutics"
    ],
    "Market Cap (USD)": [
        319840000000, 207080000000, 281900000, 40600000, 17500000, 18500000, 20300000, 24700000, 27500000, 28900000,
        20300000000, 19440000000, 30200000, 35700000, 40100000, 2890000, 2030000, 339000, 128000, 3300
    ],
    "Founded Year": [
        2013, 1888, 1965, 1971, 2014, 2004, 2004, 1993, 1986, 1999,
        1958, 1985, 1998, 2008, 2021, 2007, 1997, 2012, 2007, 2003
    ],
    "Total Employees": [
        50000, 113000, 1600, 190, 50, 40, 40, 100, 20, 500, 15000, 6940,
        10, 240, 9000, 20, 20, 50, 40, "N/A"
    ],
    "Headquarters": [
        "Illinois, USA", "Illinois, USA", "Tokyo, Japan", "Florida, USA", "Omer, Israel", "California, USA",
        "Georgia, USA", "Texas, USA", "New Jersey, USA", "Liège, Belgium", "California, USA", "Massachusetts, USA",
        "Arizona, USA", "California, USA", "New Jersey, USA", "Florida, USA", "New Jersey, USA", "Stockholm, Sweden",
        "California, USA", "British Columbia, Canada"
    ],
    "Stock Exchange": [
        "NYSE", "NYSE", "TYO", "NASDAQ", "TASE", "NASDAQ", "NASDAQ", "NASDAQ", "NYSE", "EBR", "NASDAQ", "NASDAQ",
        "NASDAQ", "NASDAQ", "NYSE", "-", "NASDAQ", "STO", "OTCMKTS", "OTCMKTS"
    ]
}

df = pd.DataFrame(data)

# Streamlit App
st.set_page_config(page_title="Women's Health Market Dashboard", layout="wide")
st.title("Top 20 Women Health-Focused Companies")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_countries = st.sidebar.multiselect("Select Countries", df["Headquarters"].unique(), default=df["Headquarters"].unique())
selected_exchanges = st.sidebar.multiselect("Select Stock Exchanges", df["Stock Exchange"].unique(), default=df["Stock Exchange"].unique())
market_cap_range = st.sidebar.slider("Market Cap Range (USD)", int(df["Market Cap (USD)"].min()), int(df["Market Cap (USD)"].max()), (int(df["Market Cap (USD)"].min()), int(df["Market Cap (USD)"].max())))

# Apply Filters
filtered_df = df[(df["Headquarters"].isin(selected_countries)) &
                 (df["Stock Exchange"].isin(selected_exchanges)) &
                 (df["Market Cap (USD)"].between(market_cap_range[0], market_cap_range[1]))]

# Overview Metrics
st.subheader("Dashboard Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Market Cap", f"${filtered_df['Market Cap (USD)'].sum():,.0f}")
col2.metric("Average Market Cap", f"${filtered_df['Market Cap (USD)'].mean():,.0f}")
col3.metric("Median Founded Year", f"{int(filtered_df['Founded Year'].median())}")
col4.metric("Number of Companies", f"{len(filtered_df)}")
st.download_button("Download Filtered Data as CSV", filtered_df.to_csv(index=False), "filtered_companies.csv", "text/csv")

# Data Table
st.subheader("Companies Data")
st.dataframe(filtered_df)

# Interactive Visualization
st.subheader("Market Cap Distribution")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(y=filtered_df["Company"], x=filtered_df["Market Cap (USD)"], palette="coolwarm", ax=ax)
ax.set_xlabel("Market Cap (USD)")
ax.set_ylabel("Company")
ax.set_title("Market Capitalization of Companies")
st.pyplot(fig)

st.subheader("Founded Year vs. Market Cap")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=filtered_df, x="Founded Year", y="Market Cap (USD)", hue="Company", size="Market Cap (USD)", sizes=(20, 200), ax=ax2)
ax2.set_xlabel("Founded Year")
ax2.set_ylabel("Market Cap (USD)")
ax2.set_title("Founded Year vs. Market Cap")
st.pyplot(fig2)

# Additional Visualization: Employees vs. Market Cap
st.subheader("Total Employees vs. Market Cap")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=filtered_df, x="Total Employees", y="Market Cap (USD)", hue="Company", size="Market Cap (USD)", sizes=(20, 200), ax=ax3)
ax3.set_xlabel("Total Employees")
ax3.set_ylabel("Market Cap (USD)")
ax3.set_title("Total Employees vs. Market Cap")
st.pyplot(fig3)
