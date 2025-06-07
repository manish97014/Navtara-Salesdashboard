import streamlit as st
import pandas as pd
import os

FILE_PATH = r"PnL.csv"

def main():

    st.title("📈 Profit & Loss Summary")

    # File check
    if not os.path.exists(FILE_PATH):
        st.error(f"❌ File not found at: {FILE_PATH}")
        st.stop()

    df = pd.read_csv(FILE_PATH)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    # Sidebar Filters
    years = sorted(df['Year'].dropna().unique())
    months = sorted(df['Month'].dropna().unique())
    locations = sorted(df['Location'].dropna().unique())

    st.sidebar.markdown("### 🔍 Filter Data")

    year = st.sidebar.multiselect("Select Year", ["Select All"] + years, default=None)
    if "Select All" in year or not year:
        year = years

    month = st.sidebar.multiselect("Select Month", ["Select All"] + months, default=None)
    if "Select All" in month or not month:
        month = months

    location = st.sidebar.multiselect("Select Location", ["Select All"] + locations, default=None)
    if "Select All" in location or not location:
        location = locations

    # Filter data based on sidebar
    df_filtered = df[
        (df['Year'].isin(year)) &
        (df['Month'].isin(month)) &
        (df['Location'].isin(location))
    ]

    # Summary values for cards
    def get_total_by_category(cat):
        return df_filtered.loc[df_filtered['Category'] == cat, 'Amount'].sum()

    revenue = get_total_by_category('Revenue')
    food_cost = get_total_by_category('Food Cost')
    operating_cost = get_total_by_category('Operating Cost')
    expense = food_cost + operating_cost
    gross_profit = revenue - food_cost
    net_profit = revenue - food_cost - operating_cost

    def format_currency(amount):
        return f"₹ {amount:,.0f}"

    pct = lambda x: f"{(x / revenue * 100):.2f}%" if revenue else "0.00%"

    # CSS (cards style)
    st.markdown("""
    <style>
    .card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 5px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #ccc;
        text-align: center;
    }
    .card p {
        font-size: 20px;
        margin: 0;
        font-weight: bold;
        color: #000000;
    }
    .card span {
        font-size: 14px;
        color: #000000;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    def render_card(title, amount, percent, color):
        st.markdown(f"""
        <div class='card'>
            <h3 style='color: {color}; font-weight: bold;'>{title}</h3>
            <p>{amount}</p>
            <span>{percent}</span>
        </div>
        """, unsafe_allow_html=True)

    # Cards layout with updated colors
    col1, col2, col3 = st.columns(3)
    with col1: render_card("Revenue", format_currency(revenue), pct(revenue), "#008000")  # Green
    with col2: render_card("Expenses", format_currency(expense), pct(expense), "#FF0000")  # Red
    with col3: render_card("Food Cost", format_currency(food_cost), pct(food_cost), "#FF0000")  # Red

    col4, col5, col6 = st.columns(3)
    with col4: render_card("Operating Cost", format_currency(operating_cost), pct(operating_cost), "#FF0000")  # Red
    with col5: render_card("Gross Profit", format_currency(gross_profit), pct(gross_profit), "#008000")  # Green
    with col6: render_card("Net Profit", format_currency(net_profit), pct(net_profit), "#008000")  # Green

    # === Bottom Table ===
    st.markdown("---")
    st.subheader("📋 P&L Report")

    # Define Particulars
    particulars_list = [
        'Non AC', 'AC', 'Swiggy', 'Zomato', 'Takeaway',
        'Bakery', 'Beverages', 'Fruits', 'Groceries',
        'Milk products', 'Ready to eat', 'Spices', 'Vegetables'
    ]

    def get_amount(item_name, df_input):
        mask = (
            (df_input['Category'] == item_name) |
            (df_input['Sub-Category'] == item_name) |
            (df_input['Super-Sub-Category'] == item_name)
        )
        return df_input.loc[mask, 'Amount'].sum()

    # Function to get previous period dataframe filtered
    def get_previous_period_df():
        prev_year = None
        prev_month = None
        # Only single year and single month selected for previous period logic to work
        if len(year) == 1 and len(month) == 1:
            selected_year = year[0]
            selected_month = month[0]

            # If only year selected (month=all), previous year data
            if ("Select All" in month) or (selected_month == '') or (selected_month not in months):
                # previous year filter
                prev_year = selected_year - 1
                prev_month = None
            else:
                # Year + Month selected, so previous month in same year
                prev_year = selected_year
                # Calculate previous month as int
                try:
                    selected_month_int = int(selected_month)
                    prev_month_int = selected_month_int - 1
                    if prev_month_int == 0:
                        # If previous month < 1, go to Dec previous year
                        prev_month_int = 12
                        prev_year = selected_year - 1
                    prev_month = str(prev_month_int)
                except:
                    prev_month = None
        elif len(year) == 1 and (("Select All" in month) or len(month) == len(months)):
            # Only year selected with all months, so previous year data
            prev_year = year[0] - 1
            prev_month = None
        else:
            # Multiple years or months selected - skip previous period
            prev_year = None
            prev_month = None

        # Filter dataframe based on previous period
        if prev_year is not None:
            if prev_month:
                df_prev = df[
                    (df['Year'] == prev_year) &
                    (df['Month'] == prev_month) &
                    (df['Location'].isin(location))
                ]
            else:
                df_prev = df[
                    (df['Year'] == prev_year) &
                    (df['Location'].isin(location))
                ]
            return df_prev
        else:
            return pd.DataFrame()  # empty df if no previous period

    df_prev = get_previous_period_df()

    # Calculate revenue for previous period for % calculation
    prev_revenue = df_prev.loc[df_prev['Category'] == 'Revenue', 'Amount'].sum() if not df_prev.empty else 0

    # Calculate previous period Gross Profit and Net Profit properly
    if not df_prev.empty:
        prev_revenue = df_prev.loc[df_prev['Category'] == 'Revenue', 'Amount'].sum()
        prev_food_cost = df_prev.loc[df_prev['Category'] == 'Food Cost', 'Amount'].sum()
        prev_operating_cost = df_prev.loc[df_prev['Category'] == 'Operating Cost', 'Amount'].sum()
        gross_profit_prev = prev_revenue - prev_food_cost
        net_profit_prev = prev_revenue - prev_food_cost - prev_operating_cost
    else:
        gross_profit_prev = 0
        net_profit_prev = 0

    # Build data
    rows = []
    rows.append({'Particulars': 'Revenue', 'Amount': '', 'Percentage': '', 'Previous Period': '', '% (Prev)': ''})

    for name in particulars_list:
        amt = get_amount(name, df_filtered)
        # previous period amount
        prev_amt = get_amount(name, df_prev) if not df_prev.empty else 0

        percent = f"{(amt / revenue * 100):.2f}%" if revenue and amt else ""
        prev_percent = f"{(prev_amt / prev_revenue * 100):.2f}%" if prev_revenue and prev_amt else ""

        rows.append({
            'Particulars': name,
            'Amount': amt,
            'Percentage': percent,
            'Previous Period': prev_amt,
            '% (Prev)': prev_percent
        })

    # Insert Total Sales after Takeaway
    sales_items = ['Non AC', 'AC', 'Swiggy', 'Zomato', 'Takeaway']
    total_sales = sum([row['Amount'] for row in rows if row['Particulars'] in sales_items])
    total_sales_prev = sum([row['Previous Period'] for row in rows if row['Particulars'] in sales_items])
    sales_percent = f"{(total_sales / revenue * 100):.2f}%" if revenue else ""
    sales_prev_percent = f"{(total_sales_prev / prev_revenue * 100):.2f}%" if prev_revenue else ""
    rows.insert(6, {'Particulars': 'Total Sales', 'Amount': total_sales, 'Percentage': sales_percent,
                   'Previous Period': total_sales_prev, '% (Prev)': sales_prev_percent})

    # Total Food Cost after Vegetables
    food_items = [
        'Bakery', 'Beverages', 'Fruits', 'Groceries',
        'Milk products', 'Ready to eat', 'Spices', 'Vegetables'
    ]
    total_food_cost = sum([row['Amount'] for row in rows if row['Particulars'] in food_items])
    total_food_cost_prev = sum([row['Previous Period'] for row in rows if row['Particulars'] in food_items])
    food_cost_percent = f"{(total_food_cost / revenue * 100):.2f}%" if revenue else ""
    food_cost_prev_percent = f"{(total_food_cost_prev / prev_revenue * 100):.2f}%" if prev_revenue else ""
    rows.append({'Particulars': 'Total Food Cost', 'Amount': total_food_cost, 'Percentage': food_cost_percent,
                 'Previous Period': total_food_cost_prev, '% (Prev)': food_cost_prev_percent})

    # Gross Profit
    gross_profit_percent = f"{(gross_profit / revenue * 100):.2f}%" if revenue else ""
    gross_profit_prev_percent = f"{(gross_profit_prev / prev_revenue * 100):.2f}%" if prev_revenue else ""
    rows.append({'Particulars': 'Gross Profit', 'Amount': gross_profit, 'Percentage': gross_profit_percent,
                 'Previous Period': gross_profit_prev, '% (Prev)': gross_profit_prev_percent})

    # Expense Categories
    expense_items = [
        'Salaries', 'Rent', 'Water', 'Electricity', 'Staff room rent',
        'Staff electricity', 'Commission', 'Admin expenses',
        'Repairs and maintenance', 'Advertisement'
    ]
    for item in expense_items:
        amt = get_amount(item, df_filtered)
        prev_amt = get_amount(item, df_prev) if not df_prev.empty else 0
        percent = f"{(amt / revenue * 100):.2f}%" if revenue and amt else ""
        prev_percent = f"{(prev_amt / prev_revenue * 100):.2f}%" if prev_revenue and prev_amt else ""
        rows.append({
            'Particulars': item,
            'Amount': amt,
            'Percentage': percent,
            'Previous Period': prev_amt,
            '% (Prev)': prev_percent
        })

    # Operating Cost = sum of all the above expense_items
    operating_cost_total = sum([row['Amount'] for row in rows if row['Particulars'] in expense_items])
    operating_cost_prev_total = sum([row['Previous Period'] for row in rows if row['Particulars'] in expense_items])
    operating_cost_percent = f"{(operating_cost_total / revenue * 100):.2f}%" if revenue else ""
    operating_cost_prev_percent = f"{(operating_cost_prev_total / prev_revenue * 100):.2f}%" if prev_revenue else ""
    rows.append({'Particulars': 'Operating Cost', 'Amount': operating_cost_total, 'Percentage': operating_cost_percent,
                 'Previous Period': operating_cost_prev_total, '% (Prev)': operating_cost_prev_percent})

    # Net Profit
    net_profit_percent = f"{(net_profit / revenue * 100):.2f}%" if revenue else ""
    net_profit_prev_percent = f"{(net_profit_prev / prev_revenue * 100):.2f}%" if prev_revenue else ""
    rows.append({'Particulars': 'Net Profit', 'Amount': net_profit, 'Percentage': net_profit_percent,
                 'Previous Period': net_profit_prev, '% (Prev)': net_profit_prev_percent})

    # === Render as HTML table ===
    table_html = """
    <style>
    table.custom {
        width: 100%;
        border-collapse: collapse;
        font-size: 18px;
    }
    table.custom th, table.custom td {
        border: 1px solid #ccc;
        padding: 10px;
        text-align: left;
    }
    table.custom th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    .bold-row {
        font-weight: bold;
    }
    </style>
    <table class="custom">
        <tr>
            <th>Particulars</th>
            <th>Amount</th>
            <th>%</th>
            <th>Previous Period</th>
            <th>% (Prev)</th>
        </tr>
    """

    for row in rows:
        bold_class = "bold-row" if row['Particulars'] in [
            'Revenue', 'Total Sales', 'Total Food Cost', 'Gross Profit', 'Operating Cost', 'Net Profit'
        ] else ""
        amt_display = f"₹ {row['Amount']:,.0f}" if isinstance(row['Amount'], (int, float)) else ""
        prev_display = f"₹ {row['Previous Period']:,.0f}" if isinstance(row['Previous Period'], (int, float)) else ""
        perc_display = row.get('Percentage', '')
        prev_perc_display = row.get('% (Prev)', '')

        table_html += f"<tr class='{bold_class}'>" \
                      f"<td>{row['Particulars']}</td>" \
                      f"<td>{amt_display}</td>" \
                      f"<td>{perc_display}</td>" \
                      f"<td>{prev_display}</td>" \
                      f"<td>{prev_perc_display}</td>" \
                      f"</tr>"

    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

    # === Add CSV Download Button ===
    st.markdown("---")
    st.markdown("### 📥 Download P&L Report as CSV")

    # Convert rows to DataFrame for download
    download_df = pd.DataFrame(rows)

    # Format numeric columns for download (remove currency symbol for csv)
    download_df['Amount'] = download_df['Amount'].apply(lambda x: round(x,0) if isinstance(x, (int,float)) else "")
    download_df['Previous Period'] = download_df['Previous Period'].apply(lambda x: round(x,0) if isinstance(x, (int,float)) else "")

    csv = download_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name='PnL_Report.csv',
        mime='text/csv'
    )


if __name__ == "__main__":
    main()
