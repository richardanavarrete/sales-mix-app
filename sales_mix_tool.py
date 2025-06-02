import streamlit as st
import pandas as pd

st.title("Sales Mix Analyzer")

uploaded_file = st.file_uploader("Upload your SalesMixByPrice.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, header=3)
    df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', '', regex=False), errors='coerce')
    df['Items Sold'] = pd.to_numeric(df['Items Sold'], errors='coerce')
    df = df.dropna(subset=['Items Sold', 'Price'])
    df['Item'] = df['Item'].astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.title()

    st.write("Cleaned Data Preview:")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Cleaned CSV", csv, "cleaned_sales_mix.csv", "text/csv")
