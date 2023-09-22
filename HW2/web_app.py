import streamlit as st
import seaborn as sns
import pandas as pd
import plotly as pt
import plotly.express as px
import plotly.figure_factory as ff

iris = sns.load_dataset("iris")

# Setting up the Streamlit app
st.title("Interactive 3D Scatter Plot of Iris Dataset")

# Creating a sidebar
st.sidebar.header("Dataset Description")
st.sidebar.write("This dataset contains information about iris flowers.")
st.sidebar.write("It has attributes such as sepal_length, sepal_width, petal_length, petal_width and species.")
st.sidebar.write("The target variable is 'species' with has three unique values: Setosa, Versicolor and Virginica.")

# Creating a 3d scatter plot
fig = px.scatter_3d(
    iris, x='sepal_length', y='sepal_width', z='petal_length',
    color='species', size='petal_width', opacity=0.7,
    labels={'sepal_length': 'Sepal Length', 'sepal_width': 'Sepal Width', 'petal_length': 'Petal Length'},
    template='plotly_dark'
)

# Updating text and layout
fig.update_traces(text=iris['species'], selector=dict(type='scatter3d'))
fig.update_layout(scene=dict(zaxis_title='Petal Length'), scene_aspectmode='cube')

# Displaying the plot
st.plotly_chart(fig)




