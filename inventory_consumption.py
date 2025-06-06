import streamlit as st
import pandas as pd


def main():
   
    file_path = r"inventory_loss.csv"

    try:
        df = pd.read_csv(file_path)
        df['Month'] = df['Month'].astype(str)

        # --- Sidebar Filters ---
        years = sorted(df['Year'].dropna().unique())
        selected_year = st.sidebar.selectbox("Select Year", ['All'] + years)

        if selected_year == 'All':
            month_options = sorted(df['Month'].dropna().unique())
            filtered_df = df.copy()
        else:
            month_options = sorted(df[df['Year'] == selected_year]['Month'].dropna().unique())
            filtered_df = df[df['Year'] == selected_year]

        selected_month = st.sidebar.selectbox("Select Month", ['All'] + month_options)

        if selected_year == 'All':
            location_options = sorted(df['Location'].dropna().unique())
        else:
            location_options = sorted(df[df['Year'] == selected_year]['Location'].dropna().unique())

        selected_location = st.sidebar.selectbox("Select Location", ['All'] + location_options)

        if selected_month != 'All':
            filtered_df = filtered_df[filtered_df['Month'] == selected_month]

        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['Location'] == selected_location]

        # --- Table Calculation ---
        table_df = filtered_df.groupby(['Item', 'UOM']).agg({
            'Price': 'mean',
            'Opening Stock (Qty)': 'sum',
            'Purchases (Qty)': 'sum',
            'Ideal Closing Stock': 'sum',
            'Consumption (Qty)': 'sum'
        }).reset_index()

        table_df['Consumption (Value)'] = table_df['Consumption (Qty)'] * table_df['Price']

        # Rename Ideal Closing Stock as Closing Stock
        table_df.rename(columns={'Ideal Closing Stock': 'Closing Stock'}, inplace=True)

        # Rearranged Columns
        table_df = table_df[
            ['Item', 'UOM', 'Price', 'Opening Stock (Qty)', 'Purchases (Qty)',
             'Closing Stock', 'Consumption (Qty)', 'Consumption (Value)']
        ]

        # --- Totals Row ---
        totals = {
            'Item': 'Total',
            'UOM': '',
            'Price': table_df['Price'].mean(),
            'Opening Stock (Qty)': table_df['Opening Stock (Qty)'].sum(),
            'Purchases (Qty)': table_df['Purchases (Qty)'].sum(),
            'Closing Stock': table_df['Closing Stock'].sum(),
            'Consumption (Qty)': table_df['Consumption (Qty)'].sum(),
            'Consumption (Value)': table_df['Consumption (Value)'].sum()
        }

        table_df = pd.concat([table_df, pd.DataFrame([totals])], ignore_index=True)

        # --- Display Table with Formatting ---
        st.subheader("📋 Inventory Consumption Details")
        st.dataframe(
            table_df.style.format({
                'Price': '₹ {:,.2f}',
                'Opening Stock (Qty)': '{:,.0f}',
                'Purchases (Qty)': '{:,.0f}',
                'Closing Stock': '{:,.0f}',
                'Consumption (Qty)': '{:,.0f}',
                'Consumption (Value)': '₹ {:,.2f}'
            }),
            use_container_width=True
        )

    except FileNotFoundError:
        st.error("❌ Inventory loss file not found.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
