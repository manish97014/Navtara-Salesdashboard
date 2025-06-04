import streamlit as st
import importlib
import sys
import os

# Must be the first Streamlit command
st.set_page_config(page_title="Navtara Performance Dashboard", layout="wide")

st.title("📈 Navtara Performance Dashboard")

# === Main section selection ===
main_section = st.sidebar.radio(
    "Select Section",
    ["Sales Performance Analysis", "Food Cost Analysis", "Financial Reporting"]
)

# === SALES PERFORMANCE ANALYSIS ===
if main_section == "Sales Performance Analysis":
    st.header("📊 Sales Performance Analysis")

    sub_option = st.sidebar.radio(
        "Select a Report",
        ["Sales Growth", "Reconciliations", "Cash Variance"]
    )

    if sub_option == "Sales Growth":
        try:
            import web_sales
            web_sales.main()
        except Exception as e:
            st.error(f"❌ Error loading Sales Growth Report: {e}")

    elif sub_option == "Reconciliations":
        st.subheader("🔄 Reconciliations")
        platform_option = st.radio("Choose Platform", ["Swiggy", "Zomato"])

        if platform_option == "Swiggy":
            swiggy_report = st.radio(
                "Select Swiggy Report",
                ["Sales Reconciliation", "Order Level Reconciliation"]
            )
            if swiggy_report == "Sales Reconciliation":
                try:
                    sys.path.append(os.path.join(os.getcwd(), "Reconciliations", "Swiggy"))
                    import swiggy_reconciliation
                    swiggy_reconciliation.main()
                except Exception as e:
                    st.error(f"❌ Error loading Swiggy Sales Reconciliation: {e}")
            else:
                st.info("Order Level Reconciliation – Coming Soon!")

        elif platform_option == "Zomato":
            st.info("Zomato Reports – Coming Soon!")

    elif sub_option == "Cash Variance":
        st.subheader("💰 Cash Variance")
        st.info("Cash Variance report will be added here.")

# === FOOD COST ANALYSIS ===
elif main_section == "Food Cost Analysis":
    st.header("🍽️ Food Cost Analysis")

    food_option = st.sidebar.radio(
        "Select a Report",
        [
            "Ideal Vs Actual Food Cost",
            "Inventory Consumption Report",
            "Inventory Loss Report",
            "Dish Level Costing Report"
        ]
    )

    if food_option == "Ideal Vs Actual Food Cost":
        try:
            sys.path.append(os.path.join(os.getcwd(), "food_cost_analysis", "ideal_vs_actual"))
            import ideal_vs_actual
            ideal_vs_actual.main()
        except Exception as e:
            st.error(f"❌ Error loading Ideal Vs Actual Food Cost: {e}")

    elif food_option == "Inventory Consumption Report":
        try:
            sys.path.append(os.path.join(os.getcwd(), "food_cost_analysis", "inventory_consumption"))
            import inventory_consumption
            inventory_consumption.main()
        except Exception as e:
            st.error(f"❌ Error loading Inventory Consumption Report: {e}")

    elif food_option == "Inventory Loss Report":
        try:
            sys.path.append(os.path.join(os.getcwd(), "food_cost_analysis", "inventory_loss"))
            import inventory_loss
            inventory_loss.main()
        except Exception as e:
            st.error(f"❌ Error loading Inventory Loss Report: {e}")

    elif food_option == "Dish Level Costing Report":
        st.info("Dish Level Costing Report – Coming Soon!")

# === FINANCIAL REPORTING ===
elif main_section == "Financial Reporting":
    st.header("📑 Financial Reporting")

    finance_option = st.sidebar.radio(
        "Select a Report",
        ["P&L Report", "Cash Flow Statement"]
    )

    st.subheader(finance_option)
    st.info(f"{finance_option} – Coming Soon!")
