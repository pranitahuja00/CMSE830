import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Car Price Analysis")

data = pd.read_csv('https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/midSem_project/car_price_train.csv', delimiter=",", skiprows=0)

#Balancing the data
data.drop(data[data['Price']>150000].index, axis=0, inplace=True)

if data is not None:
    st.subheader("Attribute Affect On Price")
    selected_column1 = st.selectbox("Select attribute", data.columns)
    if selected_column1:
        chart = alt.Chart(data).mark_circle().encode(x='Price', y=selected_column1).interactive()
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
