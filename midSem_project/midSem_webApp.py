import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Car Price Analysis")

data = pd.read_csv('https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/midSem_project/car_price_train.csv', delimiter=",", skiprows=0)

#Converting certain attributes to numeric and cleaning others
data['Mileage'] = data['Mileage'].str.replace("km", "")
data['Mileage'] = data['Mileage'].astype(int)

data['Levy'] = data['Levy'].replace('-',np.nan)
data['Levy'] = data['Levy'].astype(float)
data.dropna(axis=0, inplace=True)

data['Doors']=data['Doors'].str.replace('04-May','4')
data['Doors']=data['Doors'].str.replace('02-May','2')

#Balancing the data
data.drop(data[data['Price']>120000].index, axis=0, inplace=True)
data.drop(data[data['Mileage']>550000].index, axis=0, inplace=True)
data.drop(data[data['Levy']>5000].index, axis=0, inplace=True)

if data is not None:
    st.subheader("Attribute Affect On Price")
    selected_column1 = st.selectbox("Select attribute", [c for c in data.columns if c not in ['ID', 'Price', 'Model', 'Prod. year']])
    if selected_column1:
        chart = alt.Chart(data).mark_circle().encode(x='Price', y=selected_column1).interactive()
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
