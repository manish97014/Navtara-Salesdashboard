import streamlit as st
import pandas as pd

def main():
    st.title("📊 Ideal vs Actual Food Cost Analysis")

    file_path = r"foodcost_category.csv"

    try:
        df = pd.read_csv(file_path)
        df['Month'] = df['Month'].astype(str)  # Ensure Month is string

        # Sidebar Filters
        years = sorted(df['Year'].dropna().unique())
        selected_year = st.sidebar.selectbox("Select Year", years)

        months = sorted(df[df['Year'] == selected_year]['Month'].dropna().unique())
        selected_month = st.sidebar.selectbox("Select Month (optional)", ['All'] + months)

        locations = sorted(df[df['Year'] == selected_year]['Location'].dropna().unique())
        selected_location = st.sidebar.selectbox("Select Location (optional)", ['All'] + locations)

        # Filtered Data
        filtered_df = df[df['Year'] == selected_year]
        if selected_month != 'All':
            filtered_df = filtered_df[filtered_df['Month'] == selected_month]
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['Location'] == selected_location]

        # Card Calculations
        if selected_month == 'All' and selected_location == 'All':
            total_ideal = df[df['Year'] == selected_year]['Ideal Cost'].sum()
            total_actual = df[df['Year'] == selected_year]['Actual Cost'].sum()
            total_variance = df[df['Year'] == selected_year]['Variance'].sum()

            month_count = df[df['Year'] == selected_year]['Month'].nunique()
            location_count = df[df['Year'] == selected_year]['Location'].nunique()

            ideal_cost = total_ideal / (month_count * location_count)
            actual_cost = total_actual / (month_count * location_count)
            variance = total_variance / (month_count * location_count)

        elif selected_month != 'All' and selected_location == 'All':
            total_ideal = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]['Ideal Cost'].sum()
            total_actual = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]['Actual Cost'].sum()
            total_variance = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]['Variance'].sum()

            location_count = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]['Location'].nunique()

            ideal_cost = total_ideal / location_count
            actual_cost = total_actual / location_count
            variance = total_variance / location_count

        else:
            ideal_cost = filtered_df['Ideal Cost'].sum()
            actual_cost = filtered_df['Actual Cost'].sum()
            variance = filtered_df['Variance'].sum()

        # Display Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Ideal Food Cost", f"₹ {ideal_cost:,.2f}")
        col2.metric("Actual Food Cost", f"₹ {actual_cost:,.2f}")
        col3.metric("Variance", f"₹ {variance:,.2f}")

        # Location-wise Table
        st.subheader("📍 Location-wise Food Cost")
        if selected_month == 'All' and selected_location == 'All':
            month_count = df[df['Year'] == selected_year]['Month'].nunique()
            loc_table = df[df['Year'] == selected_year].groupby('Location').agg({
                'Ideal Cost': 'sum', 'Actual Cost': 'sum', 'Variance': 'sum'
            }).reset_index()
            loc_table['Ideal Cost'] = loc_table['Ideal Cost'] / month_count
            loc_table['Actual Cost'] = loc_table['Actual Cost'] / month_count
            loc_table['Variance'] = loc_table['Variance'] / month_count
        elif selected_month != 'All' and selected_location == 'All':
            loc_table = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)].groupby('Location').agg({
                'Ideal Cost': 'sum', 'Actual Cost': 'sum', 'Variance': 'sum'
            }).reset_index()
        else:
            loc_table = filtered_df.groupby('Location').agg({
                'Ideal Cost': 'sum', 'Actual Cost': 'sum', 'Variance': 'sum'
            }).reset_index()
        st.dataframe(loc_table)

        # Category-wise Table
        st.subheader("🍽️ Category-wise Food Cost")
        if selected_month == 'All' and selected_location == 'All':
            month_count = df[df['Year'] == selected_year]['Month'].nunique()
            location_count = df[df['Year'] == selected_year]['Location'].nunique()
            cat_table = df[df['Year'] == selected_year].groupby('Category').agg({
                'Ideal Cost': 'sum', 'Actual Cost': 'sum', 'Variance': 'sum'
            }).reset_index()
            cat_table['Ideal Cost'] = cat_table['Ideal Cost'] / (month_count * location_count)
            cat_table['Actual Cost'] = cat_table['Actual Cost'] / (month_count * location_count)
            cat_table['Variance'] = cat_table['Variance'] / (month_count * location_count)
        elif selected_month != 'All' and selected_location == 'All':
            cat_table = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)].groupby('Category').agg({
                'Ideal Cost': 'sum', 'Actual Cost': 'sum', 'Variance': 'sum'
            }).reset_index()

            # Divide by number of locations for Year + Month
            location_count = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]['Location'].nunique()
            cat_table['Ideal Cost'] = cat_table['Ideal Cost'] / location_count
            cat_table['Actual Cost'] = cat_table['Actual Cost'] / location_count
            cat_table['Variance'] = cat_table['Variance'] / location_count
        else:
            cat_table = filtered_df.groupby('Category').agg({
                'Ideal Cost': 'sum', 'Actual Cost': 'sum', 'Variance': 'sum'
            }).reset_index()
        st.dataframe(cat_table)

        # Download Buttons (Only CSV)
        def download_buttons(name, df_table):
            csv = df_table.to_csv(index=False).encode('utf-8')
            st.download_button(f"Download {name} CSV", csv, f"{name.lower().replace(' ', '_')}.csv", "text/csv")

        download_buttons("Location-wise Food Cost", loc_table)
        download_buttons("Category-wise Food Cost", cat_table)

    except FileNotFoundError:
        st.error("❌ File not found.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
