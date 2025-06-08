import streamlit as st
import pandas as pd

def card(title, amount, color="#4CAF50"):
    card_html = f"""
    <div style="
        background-color:#f5f5f5;
        border-radius:15px;
        padding:25px 20px;
        margin:0 10px;  
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        width: 280px;
        text-align: center;
        ">
        <div style="font-size:18px; font-weight:bold; color:#333;">{title}</div>
        <div style="font-size:30px; font-weight:bold; color:{color}; margin-top:15px; white-space: nowrap; overflow-x: auto;">
            {amount}
        </div>
    </div>
    """
    return card_html

def main():
    st.title("💵 Cash Variance Report")

    file_path = "CVR.csv"

    try:
        df = pd.read_csv(file_path)

        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y %H:%M", errors='coerce')
        df = df.dropna(subset=["Date"])

        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.strftime('%B')

        df["Variance"] = df["Actual Cash Sales"] - df["Expected Cash Sales"]

        years = sorted(df["Year"].dropna().unique())
        selected_year = st.sidebar.selectbox("Select Year", ['All'] + years, index=0)

        months = sorted(df["Month"].dropna().unique())
        selected_month = st.sidebar.selectbox("Select Month", ['All'] + months, index=0)

        locations = sorted(df["Location"].dropna().unique())
        selected_location = st.sidebar.selectbox("Select Location", ['All'] + locations, index=0)

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_range"
        )

        filtered_df = df.copy()

        if selected_year != 'All':
            filtered_df = filtered_df[filtered_df["Year"] == selected_year]
        if selected_month != 'All':
            filtered_df = filtered_df[filtered_df["Month"] == selected_month]
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df["Location"] == selected_location]
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df["Date"].dt.date >= start_date) & 
                (filtered_df["Date"].dt.date <= end_date)
            ]

        # Final values - round and remove commas/₹
        expected_total = int(round(filtered_df["Expected Cash Sales"].sum()))
        actual_total = int(round(filtered_df["Actual Cash Sales"].sum()))
        variance_total = int(round(filtered_df["Variance"].sum()))
        color = "#E53935" if variance_total < 0 else "#4CAF50"

        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.markdown(card("🧾 Expected Cash Sales", str(expected_total)), unsafe_allow_html=True)
        with col2:
            st.markdown(card("💰 Actual Cash Sales", str(actual_total)), unsafe_allow_html=True)
        with col3:
            st.markdown(card("🔀 Variance", str(variance_total), color=color), unsafe_allow_html=True)

        # Format date for display
        filtered_df["Date"] = filtered_df["Date"].dt.strftime('%d-%m-%Y')

        st.subheader("📋 Cash Variance Details")
        display_cols = [
            "Date", "Location", "Total Sales", "Swiggy", "Zomato", "Card Sales",
            "UPI", "Dineout", "Zomato Pro", "Expenses",
            "Expected Cash Sales", "Actual Cash Sales", "Variance"
        ]
        st.dataframe(filtered_df[display_cols].sort_values("Date"), use_container_width=True)

        # Download button
        csv = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Report as CSV", csv, "cash_variance_report.csv", "text/csv")

    except FileNotFoundError:
        st.error("❌ CVR.csv file not found.")
    except Exception as e:
        st.error(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    main()
