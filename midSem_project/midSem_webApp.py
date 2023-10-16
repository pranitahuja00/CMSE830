import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

st.title("Car Price Analysis")

data = pd.read_csv('https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/midSem_project/car_price_train.csv', delimiter=",", skiprows=0)
data_test = pd.read_csv('https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/midSem_project/car_price_test.csv', delimiter=",", skiprows=0)

#Converting certain attributes to numeric and cleaning others
data.rename(columns={'Prod. year': 'Production year'}, inplace=True)
data['Mileage'] = data['Mileage'].str.replace("km", "")
data['Mileage'] = data['Mileage'].astype(int)

data['Levy'] = data['Levy'].map(lambda x:0 if x== '-' else x)
data['Levy'] = data['Levy'].astype(float)

data['Doors']=data['Doors'].str.replace('04-May','4')
data['Doors']=data['Doors'].str.replace('02-May','2')
data['Doors']=data['Doors'].str.replace('02-Mar','2')
data['Doors']=data['Doors'].str.replace('>5','5')
data['Doors'] = data['Doors'].astype(float)

data['Turbo']=data['Engine volume'].str.contains('Turbo')
data['Engine volume']=data['Engine volume'].str.replace('Turbo','')
data['Engine volume']= data['Engine volume'].astype('float')

data['Leather interior']=data['Leather interior'].map(lambda x:True if x== 'Yes' else False)

data = data.drop_duplicates(subset=[a for a in data.columns if a not in ['ID']])

#Balancing the data
data.drop(data[data['Price']>200000].index, axis=0, inplace=True)
data.drop(data[data['Price']<1500].index, axis=0, inplace=True)
data.drop(data[data['Mileage']>550000].index, axis=0, inplace=True)
data.drop(data[data['Levy']>8000].index, axis=0, inplace=True)
data.reset_index(drop=True, inplace=True)

#Doing the same for test data
data_test.rename(columns={'Prod. year': 'Production year'}, inplace=True)
data_test['Mileage'] = data_test['Mileage'].str.replace("km", "")
data_test['Mileage'] = data_test['Mileage'].astype(int)

data_test['Levy'] = data_test['Levy'].map(lambda x:0 if x== '-' else x)
data_test['Levy'] = data_test['Levy'].astype(float)

data_test['Doors']=data_test['Doors'].str.replace('04-May','4')
data_test['Doors']=data_test['Doors'].str.replace('02-May','2')
data_test['Doors']=data_test['Doors'].str.replace('02-Mar','2')
data_test['Doors']=data_test['Doors'].str.replace('>5','5')
data_test['Doors'] = data_test['Doors'].astype(float)

data_test['Turbo']=data_test['Engine volume'].str.contains('Turbo')
data_test['Engine volume']=data_test['Engine volume'].str.replace('Turbo','')
data_test['Engine volume']= data_test['Engine volume'].astype('float')

data_test['Leather interior']=data_test['Leather interior'].map(lambda x:True if x== 'Yes' else False)

data_test = data_test.drop_duplicates(subset=[a for a in data_test.columns if a not in ['ID']])

#Balancing the data
data_test.drop(data_test[data_test['Price']>200000].index, axis=0, inplace=True)
data_test.drop(data_test[data_test['Price']<1500].index, axis=0, inplace=True)
data_test.drop(data_test[data_test['Mileage']>550000].index, axis=0, inplace=True)
data_test.reset_index(drop=True, inplace=True)

st.subheader("Check the relationship between attributes and the final price:")
selected_column1 = st.selectbox("Select attribute", [c for c in data.columns if c not in ['ID', 'Price', 'Production year', 'Model']])
price_hue = st.selectbox("Select Hue", [c for c in data.columns if c not in ['ID', 'Price', 'Model', 'Prod. year', 'Mileage', 'Levy']])
chart_line_check = st.checkbox("Show Regression Line", key=1)
if selected_column1:
    chart = alt.Chart(data).mark_circle().encode(x='Price', y=selected_column1, color=price_hue).interactive()
    chart_line = chart.transform_regression('Price', selected_column1).mark_line()
    st.altair_chart(chart+chart_line if chart_line_check else chart, theme="streamlit", use_container_width=True)

st.subheader("Check price and attributes according to manufacturer and model:")
car_make = None
car_model = None
car_make = st.selectbox("Select manufacturer", [m for m in data['Manufacturer'].unique()], placeholder='Select Manufacturer')
car_model = st.selectbox("Select model", [m for m in data['Model'][data['Manufacturer']==car_make].unique()], placeholder='Select Model')
multiple_attr = st.multiselect('Select attributes to view: ', options=data.columns, default=['Price', 'Mileage'])

if(car_model != None and car_make != None):
    make_model_price = data[multiple_attr][data['Model']==car_model][data['Manufacturer']==car_make].reset_index(drop=True)
    st.write(make_model_price)
    st.write('Price according to mileage for ', car_make, ' ', car_model, ':')
    make_model_price_chart_line_check = st.checkbox("Show Regression Line", key=2)
    make_model_price_chart = alt.Chart(data[data['Model']==car_model][data['Manufacturer']==car_make]).mark_circle().encode(x='Price', y='Mileage').interactive()
    make_model_price_chart_line = make_model_price_chart.transform_regression('Price', 'Mileage').mark_line()
    st.altair_chart(make_model_price_chart+make_model_price_chart_line if make_model_price_chart_line_check else make_model_price_chart, theme="streamlit", use_container_width=True)

