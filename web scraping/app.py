import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# โหลดผลลัพธ์และโมเดลจากไฟล์ pickle
@st.cache
def load_data():
    with open('results.pkl', 'rb') as file:
        results = pickle.load(file)
    return results

results = load_data()

if results is not None:
    # แสดงตารางผลลัพธ์
    st.subheader("Sales Forecast Results")
    st.write(results)

    # แสดงกราฟแท่งแนวนอน
    st.subheader("Current vs Forecasted Sales")
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.barh(results['Product_names'], results['Current_Sold_out'], color='blue', label='Current Sales')
    ax.barh(results['Product_names'], results['Forecasted_Sold_out'], color='red', alpha=0.6, label='Forecasted Sales')
    ax.set_xlabel('Sales')
    ax.set_ylabel('Product')
    ax.set_title('Comparison of Current Sales and Forecasted Sales')
    ax.legend()
    ax.grid(axis='x')
    st.pyplot(fig)
else:
    st.write("Please upload the analysis results to proceed.")