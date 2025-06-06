import streamlit as st
import pandas as pd

def main():
    st.title("🍽️ Dish Level Costing Report")

    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv("dish.csv")
    
    df = load_data()

    # Sidebar filters
    st.sidebar.header("🔎 Filter Options")
    outlet_list = ["All"] + sorted(df["Outlet"].dropna().unique())
    year_list = ["All"] + sorted(df["Year"].dropna().unique())
    month_list = ["All"] + sorted(df["Month"].dropna().unique())

    selected_outlet = st.sidebar.selectbox("Select Outlet", outlet_list)
    selected_year = st.sidebar.selectbox("Select Year", year_list)
    selected_month = st.sidebar.selectbox("Select Month", month_list)

    # Apply filters
    filtered_df = df.copy()

    if selected_outlet != "All":
        filtered_df = filtered_df[filtered_df["Outlet"] == selected_outlet]

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["Year"] == selected_year]

    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["Month"] == selected_month]

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    # Calculations
    filtered_df["Total Cost"] = filtered_df["Selling Qty"] * filtered_df["Cost Price"]
    filtered_df["Total Revenue"] = filtered_df["Selling Qty"] * filtered_df["Selling Price"]
    filtered_df["% of Cost"] = (filtered_df["Total Cost"] / filtered_df["Total Revenue"]) * 100
    filtered_df["% of Margin"] = 100 - filtered_df["% of Cost"]

    # Summary cards
    total_cost = filtered_df["Total Cost"].sum()
    total_revenue = filtered_df["Total Revenue"].sum()
    food_cost_pct = (total_cost / total_revenue * 100) if total_revenue != 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Cost Value", f"₹{total_cost:,.0f}")
    col2.metric("📈 Total Revenue", f"₹{total_revenue:,.0f}")
    col3.metric("🍲 Food Cost %", f"{food_cost_pct:.2f}%")

    # Table
    st.markdown("### 📋 Item-wise Food Cost Details")

    table_df = filtered_df[[
        "Item Name", "Cost Price", "Selling Qty", "Total Cost", "Total Revenue", "% of Cost", "% of Margin"
    ]].copy()

    # Format percentage columns as strings with exact two decimals (not rounded early)
    table_df["% of Cost"] = table_df["% of Cost"].apply(lambda x: f"{x:.2f}%")
    table_df["% of Margin"] = table_df["% of Margin"].apply(lambda x: f"{x:.2f}%")

    st.dataframe(table_df.sort_values(by="Total Revenue", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
