import pickle
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(layout = 'centered')

# load orginal DataFrame
df = pd.read_csv('datasets/datasets in project/gurgaon_properties.csv', on_bad_lines= 'skip')

# Custom CSS for styling
st.markdown("""
    <style>
        div.block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Add the title with custom styling
st.markdown("<h1 style='text-align: center; font-family: Arial, sans-serif;'> Enter your Inputs</h1>",unsafe_allow_html=True )

# Input from gituser

property_type = st.selectbox(label='Property Type',options = ['house','flat'], placeholder = 'Choose an option', index = None)
sector = st.selectbox(label = 'Sector', options = sorted(df['sector'].unique().tolist(), key = len), placeholder = 'Choose an option', index= None)
built_up_area = st.number_input(label = 'Built-Up Area', placeholder = 'Enter the area that you want', value = 0)
property_age = st.selectbox(label = 'Property Age', options = sorted(df['agepossession'].unique().tolist()), placeholder = 'Choose an option', index = None)

bedroom = st.selectbox(label = 'Number of Bedroom', options = sorted(df['bedroom'].unique().tolist()), placeholder = 'Choose an option', index = None)
bathroom = st.selectbox(label = 'Number of Bathroom', options = sorted(df['bathroom'].unique().tolist()), placeholder = 'Choose an option', index = None )
study_room = st.selectbox(label = 'Number of Study Room', options = sorted(df['study room'].unique().tolist()), placeholder = 'Choose an option', index = None )
servant_room = st.selectbox(label = 'Number of Servant Room', options = sorted(df['servant room'].unique().tolist()), placeholder = 'Choose an option', index = None )
store_room = st.selectbox(label = 'Number of Store Room', options = sorted(df['store room'].unique().tolist()), placeholder = 'Choose an option', index = None )
balcony = st.selectbox(label = 'Number of Balcony', options = sorted(df['balcony'].unique().tolist()), placeholder = 'Choose an option', index = None )

furnishing_type = st.selectbox(label = 'Furnishing Type', options = sorted(df['furnishing_type'].unique().tolist()), placeholder = 'Choose an option', index = None )
luxury_category = st.selectbox(label = 'Luxury Category', options = sorted(df['luxury_category'].unique().tolist()), placeholder = 'Choose an option', index = None )
floor_category = st.selectbox(label = 'Floor Category', options = sorted(df['floor_category'].unique().tolist()), placeholder = 'Choose an option', index = None )

A = False
if(property_type != None and sector != None and built_up_area != None and property_age !=None and bedroom != None and bathroom != None and study_room != None):
    A = True

B = False
if(servant_room != None and store_room != None and balcony != None and furnishing_type != None and luxury_category!=None and floor_category != None):
    B = True

# loading model

try:
  pipeline = pickle.load(open('ml models/final_model2.pkl','rb'))

except FileNotFoundError:
    st.error("Model file not found")

try:
  scaler = pickle.load(open('ml models/power_trf.pkl','rb'))

except FileNotFoundError:
    st.error('Power Transfomer file not found')


button = st.button(label = 'Predict', key = 'btn1')

if button:
    if A == True and B == True:

      built_up_area = int(built_up_area)
      bedroom = int(bedroom)
      bathroom = int(bathroom)
      study_room = int(study_room)
      servant_room = int(servant_room)
      store_room = int(store_room)

      # Forming DataFrame from User input
      data = [[property_type, sector, built_up_area, property_age, bedroom, bathroom, study_room, servant_room, store_room, balcony, furnishing_type, luxury_category, floor_category]]
      cols = df.columns[:-1].tolist()

      test_df = pd.DataFrame(data, columns = cols)

      # st.dataframe(test_df)
      price = np.round(scaler.inverse_transform(pipeline.predict(test_df).reshape(-1, 1))[0][0], 2)

      lower_value =  price - 0.2164
      higher_value = price + 0.2164

      text = 'The price of this {} is between {} to {}'.format(property_type, u'\u20B9 {}cr'.format(np.round(lower_value, 2)), u'\u20B9 {}cr'.format(np.round(higher_value, 2)))

      st.success(text)


    else:
       st.error('Please! Fill all the features')


## Contack Links

# Custom CSS for footer
footer_style = """
    <style>
        .footer {
            position: fixed;
            bottom: 10px;
            right: 10px;
            text-align: right;
            text-decoration: none;
            color: #000000;
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000; /* Ensures it stays above other elements */
        }
        .footer p {
            margin: 0;
            font-size: 14px;
        }
        .footer a {
            display: flex;
            align-items: center;
            text-decoration: none;
            color: #000000;
            margin-top: 5px;
        }
        .footer a img {
            margin-right: 5px;
            width: 24px;
            height: 24px;
        }
    </style>
"""

# Footer content
footer_content = """
    <div class="footer">
        <p>Made with ❤️ by Rajeev Nayan Tripathi</p>
        <a href="https://www.linkedin.com/in/rajeev-nayan-tripathi-1499581b7/" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/linkedin.png" alt="LinkedIn Icon"/>LinkedIn
        </a>
        <a href="mailto:rajeevnayantripathi36@gmail.com" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/gmail--v1.png" alt="Gmail Icon"/>Email
        </a>
    </div>
"""

# Display the footer
st.markdown(footer_style, unsafe_allow_html=True)
st.markdown(footer_content, unsafe_allow_html=True)
