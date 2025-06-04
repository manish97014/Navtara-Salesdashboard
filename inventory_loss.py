import streamlit as st
import pandas as pd

def main():
    st.title("📦 Inventory Loss Analysis")

    file_path = r"C:\Users\Navtara- Surya\OneDrive - Meal Metrix\Navtara\Python- Sales Performance analysis\Food cost analysis\foodcost_inputs\inventory_loss.csv"

    try:
        df = pd.read_csv(file_path)
        df['Month'] = df['Month'].astype(str)

        # Year filter with 'All'
        years = sorted(df['Year'].dropna().unique())
        selected_year = st.sidebar.selectbox("Select Year", ['All'] + years)

        # Month filter
        if selected_year == 'All':
            month_options = sorted(df['Month'].dropna().unique())
            filtered_df = df.copy()
        else:
            month_options = sorted(df[df['Year'] == selected_year]['Month'].dropna().unique())
            filtered_df = df[df['Year'] == selected_year]

        selected_month = st.sidebar.selectbox("Select Month", ['All'] + month_options)

        # Location filter
        if selected_year == 'All':
            location_options = sorted(df['Location'].dropna().unique())
        else:
            location_options = sorted(df[df['Year'] == selected_year]['Location'].dropna().unique())

        selected_location = st.sidebar.selectbox("Select Location", ['All'] + location_options)

        # Apply Month filter
        if selected_month != 'All':
            filtered_df = filtered_df[filtered_df['Month'] == selected_month]

        # Apply Location filter
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['Location'] == selected_location]

        # Card Calculations
        ideal_value = filtered_df['Ideal Closing stock Value'].sum()
        actual_value = filtered_df['Actual Closing stock Value'].sum()
        variance = filtered_df['Variance'].sum()

        # Display Custom Metric Cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
                <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;text-align:center;border:1px solid #ddd;">
                    <h5 style="font-size:16px;">Ideal Closing Stock Value</h5>
                    <h3 style="font-size:22px; color: #0a5;">₹ {ideal_value:,.2f}</h3>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;text-align:center;border:1px solid #ddd;">
                    <h5 style="font-size:16px;">Actual Closing Stock Value</h5>
                    <h3 style="font-size:22px; color: #08c;">₹ {actual_value:,.2f}</h3>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;text-align:center;border:1px solid #ddd;">
                    <h5 style="font-size:16px;">Variance</h5>
                    <h3 style="font-size:22px; color: #c00;">₹ {variance:,.2f}</h3>
                </div>
            """, unsafe_allow_html=True)

        # Table: Item, Avg Price, Ideal Closing Stock, Actual Closing Stock, Variance
        st.subheader("📋 Inventory Details by Item")
        item_table = filtered_df.groupby(['Item', 'UOM']).agg({
            'Price': 'mean',
            'Ideal Closing Stock': 'sum',
            'Actual Closing Stock': 'sum',
            'Variance': 'sum'
        }).reset_index()

        item_table.rename(columns={
            'Price': 'Avg Price',
            'Ideal Closing Stock': 'Ideal Closing Stock (Qty)',
            'Actual Closing Stock': 'Actual Closing Stock (Qty)',
            'Variance': 'Variance (Qty)'
        }, inplace=True)

        st.dataframe(item_table)

    except FileNotFoundError:
        st.error("❌ Inventory loss file not found.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
