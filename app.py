import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="نظام إدارة الأحذية", layout="wide")
st.title("👞 نظام إدارة محل الأحذية - يوسف")

# إنشاء الاتصال بـ Google Sheets
# تأكد أنك لا تضع رابط الملف هنا، بل في إعدادات Secrets في Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)


def get_data(ws):
    return conn.read(worksheet=ws)


page = st.sidebar.radio("القائمة:", ["📊 لوحة التحكم", "📦 إضافة بضاعة", "🛒 تسجيل بيع", "💸 تسجيل مصاريف"])

# --- لوحة التحكم ---
if page == "📊 لوحة التحكم":
    st.header("التقرير المالي")
    try:
        df_inv = get_data("Inventory")
        df_sales = get_data("Sales_Log")
        df_exp = get_data("Expenses_Log")

        st.metric("صافي الربح الحقيقي", f"{df_sales['الربح'].sum() - df_exp['القيمة'].sum():,} ج")
        st.dataframe(df_inv)
    except:
        st.error("تأكد من تسمية الصفحات في Google Sheets بـ Inventory, Sales_Log, Expenses_Log")

# --- إضافة بضاعة (داخل form) ---
elif page == "📦 إضافة بضاعة":
    st.header("إضافة بضاعة")
    with st.form("add_item"):
        name = st.text_input("اسم الصنف")
        price = st.number_input("سعر البيع")
        qty = st.number_input("الكمية")
        submit = st.form_submit_button("إضافة للمخزن")
        if submit:
            st.success("تم!")

# --- تسجيل بيع (داخل form) ---
elif page == "🛒 تسجيل بيع":
    st.header("تسجيل عملية بيع")
    with st.form("sell_item"):
        # يجب وضع المدخلات والزر داخل الـ form
        prod = st.text_input("اسم المنتج")
        qty_sold = st.number_input("الكمية")
        submit_sale = st.form_submit_button("إتمام البيع")
        if submit_sale:
            st.success("تم تسجيل البيع!")