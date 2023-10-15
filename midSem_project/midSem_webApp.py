import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

st.title("Car Price Analysis")

data = pd.read_csv('https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/midSem_project/car_price_train.csv', delimiter=",", skiprows=0)
data_test = pd.read_csv('https://raw.githubusercontent.com/pranitahuja00/CMSE830/main/midSem_project/car_price_test.csv', delimiter=",", skiprows=0)

all_data = pd.concat([data,data_test], axis=0)
all_data.reset_index(drop=True, inplace=True)

#Converting certain attributes to numeric and cleaning others
all_data['Mileage'] = all_data['Mileage'].str.replace("km", "")
all_data['Mileage'] = all_data['Mileage'].astype(int)

all_data['Levy'] = all_data['Levy'].map(lambda x:0 if x== '-' else x)
all_data['Levy'] = all_data['Levy'].astype(float)

all_data['Doors']=all_data['Doors'].str.replace('04-May','4')
all_data['Doors']=all_data['Doors'].str.replace('02-May','2')
all_data['Doors']=all_data['Doors'].str.replace('02-Mar','2')
all_data['Doors']=all_data['Doors'].str.replace('>5','5')
all_data['Doors'] = all_data['Doors'].astype(float)

all_data['Turbo']=all_data['Engine volume'].str.contains('Turbo')
all_data['Engine volume']=all_data['Engine volume'].str.replace('Turbo','')
all_data['Engine volume']= all_data['Engine volume'].astype('float')

all_data['Leather interior']=all_data['Leather interior'].map(lambda x:True if x== 'Yes' else False)

all_data = all_data.drop_duplicates(subset=[a for a in all_data.columns if a not in ['ID']])

#Balancing the data
all_data.drop(all_data[all_data['Price']>200000].index, axis=0, inplace=True)
all_data.drop(all_data[all_data['Price']<1500].index, axis=0, inplace=True)
all_data.drop(all_data[all_data['Mileage']>550000].index, axis=0, inplace=True)
all_data.reset_index(drop=True, inplace=True)

st.subheader("Check the effect of each attribute on the final price:")
selected_column1 = st.selectbox("Select attribute", [c for c in all_data.columns if c not in ['ID', 'Price', 'Model', 'Prod. year']])
if selected_column1:
    chart = alt.Chart(all_data).mark_circle().encode(x='Price', y=selected_column1).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.subheader("Check car attributes according to manufacturer and model:")
car_make = None
car_model = None
car_make = st.selectbox("Select manufacturer", [m for m in all_data['Manufacturer'].unique()])
car_model = st.selectbox("Select model", [m for m in all_data['Model'][all_data['Manufacturer']==car_make].unique()])
multiple_attr = st.multiselect('Select attributes to view: ', options=all_data.columns)

if(car_model != None and car_make != None):
    make_model_price = all_data[multiple_attr][all_data['Model']==car_model][all_data['Manufacturer']==car_make].reset_index(drop=True)
    st.write(make_model_price)