import streamlit as st
import importlib

# Must be the first Streamlit command
st.set_page_config(page_title="Sales Performance Analysis", layout="wide")

st.title("📊 Sales Performance Analysis")

st.sidebar.title("Menu")
option = st.sidebar.radio(
    "Select a Report",
    ["Sales Growth", "Reconciliations", "Cash Variance"]
)

if option == "Sales Growth":
    try:
        module = importlib.import_module("web_sales")  # no .py extension
        module.main()  # call main function of the module
    except ModuleNotFoundError:
        st.error("Error: 'Web sales' module not found.")
    except AttributeError:
        st.error("Error: 'main' function not found in 'Web sales' module.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

elif option == "Reconciliations":
    st.subheader("🔄 Reconciliations")
    st.info("Reconciliation report will be added here.")

elif option == "Cash Variance":
    st.subheader("💰 Cash Variance")
    st.info("Cash Variance report will be added here.")
