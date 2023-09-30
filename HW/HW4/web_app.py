import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Bank Dataset Analysis")

data = pd.read_csv("https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/HW/HW4/bank/bank.csv", delimiter=";", skiprows=0)

if data is not None:
    st.subheader("Data Preview")
    st.write(data.head())
    st.subheader("Data Exploration")
    fig, ax = plt.subplots(figsize=(8, 6))
    selected_columns = st.multiselect("Select columns for summary statistics:", data.columns)
    if selected_columns:
        st.write(data[selected_columns].describe())

    st.subheader("Data Visualization")
    chart_type = st.selectbox("Select chart type:", ["Histogram", "Line Chart"])
    if chart_type == "Histogram":
        selected_column = st.selectbox("Select a numeric column:", data.select_dtypes(include=[np.number]).columns)
        if selected_column:
            sns.histplot(data[selected_column], bins=20, kde=True, ax=ax)
    elif chart_type == "Line Chart":
        x_column = st.selectbox("Select X-axis (numeric):", data.select_dtypes(include=[np.number]).columns)
        y_column = st.selectbox("Select Y-axis (numeric):", data.select_dtypes(include=[np.number]).columns)
        if x_column and y_column:
            sns.lineplot(data=data, x=data[x_column], y=data[y_column])
    st.pyplot(fig)
