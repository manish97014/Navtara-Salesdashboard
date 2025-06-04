import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# === FILE PATHS ===
input_path = r"output files"
pos_file = f"{input_path}\\swiggy_pos.xlsx"
mapping_file = f"{input_path}\\swiggy_mapping_table.xlsx"

@st.cache_data
def load_data():
    pos_df = pd.read_excel(pos_file, usecols=['Deployment', 'Order Id', 'Bill Date', 'Gross Bill Amount', 'Source'], parse_dates=['Bill Date'])
    map_df = pd.read_excel(mapping_file, usecols=['Restaurant ID', 'Deployment'])

    pos_df['Deployment'] = pos_df['Deployment'].astype(str).str.strip()
    map_df['Deployment'] = map_df['Deployment'].astype(str).str.strip()
    map_df['Restaurant ID'] = map_df['Restaurant ID'].astype(str).str.strip()

    merged_df = pos_df.merge(
        map_df[['Restaurant ID', 'Deployment']],
        how='left',
        on='Deployment'
    )
    merged_df.rename(columns={'Deployment': 'Location'}, inplace=True)

    merged_df['Year'] = merged_df['Bill Date'].dt.year
    merged_df['Month'] = merged_df['Bill Date'].dt.month
    merged_df['MonthName'] = merged_df['Bill Date'].dt.strftime('%B')

    return merged_df

def generate_weeks(year, month):
    start_date = datetime(year, month, 1)
    end_date = pd.Timestamp(start_date) + pd.offsets.MonthEnd(0)
    weeks = []

    first_day_weekday = start_date.weekday()
    if first_day_weekday == 5:
        first_week_end = start_date
    elif first_day_weekday < 5:
        days_to_saturday = 5 - first_day_weekday
        first_week_end = start_date + timedelta(days=days_to_saturday)
    else:
        first_week_end = start_date + timedelta(days=6)

    if first_week_end > end_date:
        first_week_end = end_date

    weeks.append((start_date, first_week_end))
    current_start = first_week_end + timedelta(days=1)

    while current_start <= end_date:
        week_end = current_start + timedelta(days=6)
        if week_end > end_date:
            week_end = end_date
        weeks.append((current_start, week_end))
        current_start = week_end + timedelta(days=1)

    return weeks

def assign_week_label(df):
    week_starts = []
    week_ends = []
    for date in df['Bill Date']:
        year = date.year
        month = date.month
        weeks = generate_weeks(year, month)
        label_start = None
        label_end = None
        for start, end in weeks:
            if start <= date <= end:
                label_start = start
                label_end = end
                break
        week_starts.append(label_start)
        week_ends.append(label_end)

    df['SwiggyWeekStart'] = pd.to_datetime(week_starts)
    df['SwiggyWeekEnd'] = pd.to_datetime(week_ends)
    df['WeekLabel'] = df['SwiggyWeekStart'].dt.strftime('%Y-%m-%d') + ' - ' + df['SwiggyWeekEnd'].dt.strftime('%Y-%m-%d')
    return df

# === MAIN FUNCTION ===
def main():
    df = load_data()
    df = assign_week_label(df)

    st.title("Swiggy POS Sales Dashboard")

    with st.sidebar:
        year_options = sorted(df['Year'].dropna().unique())
        selected_year = st.selectbox("Select Year (optional)", options=[None] + year_options, index=0)

        if selected_year:
            month_options = sorted(
                df[df['Year'] == selected_year]['MonthName'].dropna().unique(),
                key=lambda x: datetime.strptime(x, '%B').month
            )
        else:
            month_options = sorted(df['MonthName'].dropna().unique(), key=lambda x: datetime.strptime(x, '%B').month)
        selected_month = st.selectbox("Select Month (optional)", options=[None] + month_options, index=0)

        if selected_year and selected_month:
            week_options = sorted(
                df[(df['Year'] == selected_year) & (df['MonthName'] == selected_month)]['WeekLabel'].dropna().unique()
            )
        else:
            week_options = sorted(df['WeekLabel'].dropna().unique())
        selected_week = st.selectbox("Select Week (optional)", options=[None] + week_options, index=0)

        location_options = sorted(df['Location'].dropna().unique())
        selected_locations = st.multiselect("Select Location(s)", options=location_options, default=location_options)

    # Apply filters
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_month:
        filtered_df = filtered_df[filtered_df['MonthName'] == selected_month]
    if selected_week:
        filtered_df = filtered_df[filtered_df['WeekLabel'] == selected_week]
    if selected_locations:
        filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]

    total_sales = filtered_df['Gross Bill Amount'].sum()

    st.header("Sales as per POS (Swiggy)")
    st.metric("Gross Bill Amount (₹)", f"{total_sales:,.0f}")
