import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Mix Tool", layout="wide")
st.title("Sales Mix Analyzer")

# --- Upload ---
uploaded_file = st.file_uploader("Upload your SalesMixByPrice.csv", type="csv")

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file, header=3)
    df = df_raw.rename(columns={df_raw.columns[0]: 'Item'}).copy()

    # --- Clean ---
    df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', '', regex=False), errors='coerce')
    df['Items Sold'] = pd.to_numeric(df['Items Sold'], errors='coerce')
    df = df.dropna(subset=['Items Sold', 'Price'])
    df['Item'] = df['Item'].astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.title()

    # --- Mappings ---
    item_to_category = {
        "Bud Light Bottle": ["Dom Bottle"],
        "Michelob Ultra Bottle": ["Dom Bottle"],
        "Can Twisted Tea": ["Cans / Prem Bottle"],
        "Can White Claw Mango": ["Hard Seltzer"],
        "Can White Claw Black Cherry": ["Hard Seltzer"],
        "Modelo Especial 16Oz": ["Prem Pint"],
        "Modelo Especial 32Oz": ["Prem 32oz"],
        "Jameson": ["Jameson"],
        "Jameson (Fs)": ["Jameson"],
        "Titos": ["Tito'S"],
        "Titos (Fs)": ["Tito'S"],
        "Zipparita": ["Zipparita"],
        "House Cab Gl": ["House Wines"],
        "House Merlot Gl": ["House Wines"],
        "La Marca Prosecco Gl": ["Prem Wines"],
        "Mimosa": ["Mimosa"],
    }

    key_to_sheet_label = {
        "Dom Bottle $5": "Dom Bottle $5",
        "Cans / Prem Bottle $5": "Cans / Prem Bottle $5",
        "Hard Seltzer $5": "Hard Seltzer $5",
        "Prem Pint $5": "Prem Pint $5",
        "Prem 32oz $7": "Prem 32oz $7",
        "Jameson $5": "Jameson $5",
        "Tito'S $5.50": "Tito'S $5.50",
        "Zipparita $5": "Zipparita $5",
        "House Wines $5": "House Wines $5",
        "Prem Wines $7": "Prem Wines $7",
        "Mimosa $5": "Mimosa $5",
    }

    # --- Group ---
    summary = (
        df.groupby(["Item", "Price"])
        .agg({"Items Sold": "sum"})
        .reset_index()
    )

    summary["CategoryList"] = summary["Item"].map(item_to_category)
    summary = summary.dropna(subset=["CategoryList"])
    summary = summary.explode("CategoryList")
    summary["CategoryList_str"] = summary["CategoryList"].astype(str)
    summary["Key"] = summary["CategoryList_str"] + " $" + summary["Price"].astype(str)
    summary["Key"] = summary["Key"].str.replace(r"\.0$", "", regex=True)
    summary["Key"] = summary["Key"].apply(lambda x: x if "$" not in x else (x + "0" if "." in x and len(x.split('$')[-1].split('.')[-1]) == 1 else x))
    summary["DiscountSheetLabel"] = summary["Key"].map(key_to_sheet_label)
    summary = summary.dropna(subset=["DiscountSheetLabel"])

    final = (
        summary.groupby("DiscountSheetLabel")["Items Sold"]
        .sum()
        .reset_index()
        .sort_values("DiscountSheetLabel")
    )

    # --- Display + Download ---
    st.subheader("Results")
    st.dataframe(final, use_container_width=True)

    csv = final.to_csv(index=False).encode("utf-8")
    st.download_button("Download Categorized CSV", data=csv, file_name="sales_mix_summary.csv", mime="text/csv")
