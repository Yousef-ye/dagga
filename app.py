import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Shoe Store System", layout="wide")
st.title("👞 Shoe Store Management System")

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data(ws):
    return conn.read(worksheet=ws)

page = st.sidebar.radio("Menu:", ["📊 Dashboard", "📦 Inventory", "🛒 Sales", "💸 Expenses"])

if page == "📊 Dashboard":
    st.header("Financial Report")
    try:
        df_sales = get_data("Sales_Log")
        df_exp = get_data("Expenses_Log")
        total_profit = df_sales['Profit'].sum() if not df_sales.empty else 0
        total_exp = df_exp['Amount'].sum() if not df_exp.empty else 0
        st.metric("Net Profit", f"{total_profit - total_exp:,} EGP")
        st.dataframe(get_data("Inventory"))
    except Exception as e:
        st.error(f"Error loading data: {e}")

elif page == "📦 Inventory":
    st.header("Add New Item")
    with st.form("add_item"):
        cat = st.text_input("Category")
        name = st.text_input("Product")
        size = st.text_input("Size")
        cost = st.number_input("Cost")
        price = st.number_input("Price")
        qty = st.number_input("Quantity")
        if st.form_submit_button("Save"):
            new_data = pd.DataFrame([[cat, name, size, cost, price, qty]], columns=['Category', 'Product', 'Size', 'Cost', 'Price', 'Quantity'])
            df = pd.concat([get_data("Inventory"), new_data], ignore_index=True)
            conn.update(worksheet="Inventory", data=df)
            st.success("Added successfully!")

elif page == "🛒 Sales":
    st.header("Record Sale")
    with st.form("sell_item"):
        prod = st.text_input("Product Name")
        qty_sold = st.number_input("Quantity")
        if st.form_submit_button("Confirm Sale"):
            new_sale = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), prod, qty_sold, 0]], columns=['Date', 'Product', 'Quantity_Sold', 'Profit'])
            df = pd.concat([get_data("Sales_Log"), new_sale], ignore_index=True)
            conn.update(worksheet="Sales_Log", data=df)
            st.success("Sale recorded!")

elif page == "💸 Expenses":
    st.header("Record Expense")
    with st.form("exp_item"):
        etype = st.text_input("Expense Type")
        val = st.number_input("Amount")
        if st.form_submit_button("Save Expense"):
            new_exp = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), etype, val, ""]], columns=['Date', 'Type', 'Amount', 'Notes'])
            df = pd.concat([get_data("Expenses_Log"), new_exp], ignore_index=True)
            conn.update(worksheet="Expenses_Log", data=df)
            st.success("Expense recorded!")
