import streamlit as st
import importlib

# Must be the first Streamlit command
st.set_page_config(page_title="Navtara Performance Dashboard", layout="wide")

st.title("📈 Navtara Performance Dashboard")

# Main section selection
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
            module = importlib.import_module("web_sales")  # No .py extension
            module.main()
        except ModuleNotFoundError:
            st.error("❌ 'Web sales' module not found.")
        except AttributeError:
            st.error("❌ 'main' function not found in 'Web sales' module.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

    elif sub_option == "Reconciliations":
     st.subheader("🔄 Reconciliations")

    platform_option = st.radio("Choose Platform", ["Swiggy", "Zomato"])

    if platform_option == "Swiggy":
        swiggy_report = st.radio(
            "Select Swiggy Report",
            ["Sales Reconciliation", "Order Level Reconciliation"]
        )

        st.subheader(f"🧾 Swiggy – {swiggy_report}")
        st.info(f"{swiggy_report} – Coming Soon!")

    elif platform_option == "Zomato":
        zomato_report = st.radio(
            "Select Zomato Report",
            ["Sales Reconciliation", "Order Level Reconciliation"]
        )

        st.subheader(f"🧾 Zomato – {zomato_report}")
        st.info(f"{zomato_report} – Coming Soon!")



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

    st.subheader(food_option)
    st.info(f"{food_option} – Coming Soon!")

# === FINANCIAL REPORTING ===
elif main_section == "Financial Reporting":
    st.header("📑 Financial Reporting")

    finance_option = st.sidebar.radio(
        "Select a Report",
        ["P&L Report", "Cash Flow Statement"]
    )

    st.subheader(finance_option)
    st.info(f"{finance_option} – Coming Soon!")
