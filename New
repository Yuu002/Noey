import streamlit as st
import pickle
import matplotlib.pyplot as plt

st.title("Product Sales Prediction")

# โหลดผลลัพธ์และโมเดลจากไฟล์ pickle
@st.cache
def load_data():
    with open('results.pkl', 'rb') as file:
        results = pickle.load(file)
    return results

results = load_data()

if results is not None:
    # แสดงตารางยอดขายปัจจุบัน
    st.subheader("Current Sales")
    st.write(results[['Product_names', 'Current_Sold_out']])  # แสดงเฉพาะยอดขายปัจจุบัน

    # สร้าง selectbox ให้ผู้ใช้เลือกผลิตภัณฑ์
    selected_products = st.multiselect("Select Products:", results['Product_names'].tolist(), default=results['Product_names'].tolist())

    # กรองข้อมูลตามผลิตภัณฑ์ที่เลือก
    filtered_results = results[results['Product_names'].isin(selected_products)]

    # แสดงกราฟแท่งแนวนอนของยอดขายปัจจุบัน
    st.subheader("Current Sales")
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.barh(filtered_results['Product_names'], filtered_results['Current_Sold_out'], color='blue', label='Current Sales')
    ax.set_xlabel('Sales')
    ax.set_ylabel('Product')
    ax.set_title('Current Sales')
    ax.legend()
    ax.grid(axis='x')
    st.pyplot(fig)

    # เพิ่มปุ่ม Predict
    if st.button("Predict"):
        # แสดงตารางและกราฟของยอดขายที่ทำนายได้
        st.subheader("Sales Forecast Results")
        st.write(results[['Product_names', 'Current_Sold_out', 'Forecasted_Sold_out']])  # แสดงทั้งยอดขายปัจจุบันและยอดขายที่ทำนายได้

        # แสดงกราฟเปรียบเทียบยอดขายปัจจุบันและยอดขายที่ทำนายได้
        st.subheader("Current vs Forecasted Sales")
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.barh(filtered_results['Product_names'], filtered_results['Current_Sold_out'], color='blue', label='Current Sales')
        ax.barh(filtered_results['Product_names'], filtered_results['Forecasted_Sold_out'], color='red', alpha=0.6, label='Forecasted Sales')
        ax.set_xlabel('Sales')
        ax.set_ylabel('Product')
        ax.set_title('Comparison of Current and Forecasted Sales')
        ax.legend()
        ax.grid(axis='x')
        st.pyplot(fig)
else:
    st.write("Please upload the analysis results to proceed.")
