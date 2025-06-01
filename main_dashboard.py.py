import streamlit as st
import importlib

# This line must be first before anything else
st.set_page_config(page_title="Sales Performance Analysis", layout="wide")

st.title("📊 Sales Performance Analysis")

st.sidebar.title("Menu")
option = st.sidebar.radio(
    "Select a Report",
    ["Sales Growth", "Reconciliations", "Cash Variance"]
)

if option == "Sales Growth":
    module = importlib.import_module("Web sales")  # Do not add .py extension
    module.main()  # Call your function

elif option == "Reconciliations":
    st.subheader("🔄 Reconciliations")
    st.info("Reconciliation report will be added here.")

elif option == "Cash Variance":
    st.subheader("💰 Cash Variance")
    st.info("Cash Variance report will be added here.")
