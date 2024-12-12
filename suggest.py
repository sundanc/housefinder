import pandas as pd
import numpy as np
import streamlit as st

data = pd.read_csv("Housing.csv")
data['sqft_living_grade'] = data['sqft_living'] * data['grade']
data['age'] = 2024 - data['yr_built']
data['renovation_status'] = np.where(data['yr_renovated'] > 0, 1, 0)
data = data.drop(columns=['id', 'date', 'zipcode'])

st.title("Find Your Best House")
st.write("### Input your preferences to get the best match")

min_sqft_living = st.number_input("Minimum living area (sqft):", min_value=0, step=1)
max_sqft_living = st.number_input("Maximum living area (sqft):", min_value=0, step=1)
bedrooms = st.number_input("Minimum number of bedrooms:", min_value=0, step=1)
bathrooms = st.number_input("Minimum number of bathrooms:", min_value=0.0, step=0.5)
floors = st.number_input("Minimum number of floors:", min_value=1, step=1)
grade = st.slider("Minimum house grade (1-13):", min_value=1, max_value=13, value=7)
view = st.slider("Minimum view rating (0-4):", min_value=0, max_value=4, value=0)
max_age = st.number_input("Maximum house age:", min_value=0, step=1, value=100)
renovation_status = st.selectbox("Renovation status:", options=["Doesn't matter", "Renovated", "Not renovated"])

filtered_data = data[
    (data['sqft_living'] >= min_sqft_living) &
    ((data['sqft_living'] <= max_sqft_living) if max_sqft_living > 0 else True) &
    (data['bedrooms'] >= bedrooms) &
    (data['bathrooms'] >= bathrooms) &
    (data['floors'] >= floors) &
    (data['grade'] >= grade) &
    (data['view'] >= view) &
    (data['age'] <= max_age)
]

if renovation_status == "Renovated":
    filtered_data = filtered_data[filtered_data['renovation_status'] == 1]
elif renovation_status == "Not renovated":
    filtered_data = filtered_data[filtered_data['renovation_status'] == 0]

best_house = filtered_data.sort_values(by=['grade', 'view', 'sqft_living'], ascending=[False, False, False]).head(1)

if not best_house.empty:
    st.write("### Best Matching House")
    st.table(best_house.drop(columns=['lat', 'long']).rename(columns=lambda x: x.replace('_', ' ').title()))
else:
    st.write("No houses match your criteria. Try adjusting your preferences.")
