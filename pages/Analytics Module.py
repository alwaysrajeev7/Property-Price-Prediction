import ast
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from wordcloud import WordCloud, STOPWORDS

st.set_page_config(layout = 'wide')

# Custom CSS for styling
st.markdown("""
    <style>
        div.block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Add the title with custom styling
# st.markdown("<h1 style='text-align: center; font-family: Arial, sans-serif;'> Analysis for Understanding Gurgaon RealEstate</h1>", unsafe_allow_html=True )

st.write(" ")

# Loading Datasets
df1 = pd.read_csv('datasets/datasets in project/gurgaon_with_corrdinates.csv', on_bad_lines = 'skip')
df2 = pd.read_csv('datasets/datasets in project/gurgaon_properties.csv', on_bad_lines = 'skip')
word_cloud_df = pd.read_csv('datasets/datasets in project/gurgaon_houses_and_flats_combined.csv', on_bad_lines ='skip')
df3 = pd.read_csv('datasets/datasets in project/gurgaon_missing_values_removed.csv', on_bad_lines = 'skip')

# ----------------------------------------------------------------
st.subheader('Geo Map : Gurgaon Real Estate Price/Sqft by Sector')

group_df = df1.groupby('sector').mean(numeric_only= True)[['price_in_cr',	'price_per_sqft', 'built_up_area', 'latitude', 'longitude']]

group_df.rename(columns = {'price_in_cr':'Average Price(In Crores)', 'price_per_sqft':'Average Price/Sqft', 'built_up_area':'Average Built-Up Area', 'latitude':'Latitude', 'longitude':'Longitude' }, inplace = True)

group_df['Average Price(In Crores)'] = group_df['Average Price(In Crores)'].round(2)

group_df = group_df.astype({'Average Price/Sqft':int, 'Average Built-Up Area':int}).reset_index().rename(columns = {'sector':'Sector'})


# Plotting city map

btn_map = st.button(label = 'Show', key = 'geomap')

if btn_map:
         fig = px.scatter_mapbox(group_df, lat='Latitude', lon='Longitude', color='Average Price/Sqft', size='Average Built-Up Area', size_max=20, zoom=11,
                                 color_continuous_scale='jet', mapbox_style='open-street-map', hover_name='Sector',
                                 hover_data={'Average Price(In Crores)': True, 'Average Price/Sqft': True,'Average Built-Up Area': True})
         fig.update_layout(height = 700, width = 1500)
         st.plotly_chart(fig, use_container_width = False)

st.divider()

# -----------------------------------------------------------------
st.subheader('WordCloud: Amenities in Sector Properties')

sector_name = st.selectbox(label='Locality', options = sorted(word_cloud_df['sector'].unique().tolist(), key = len) , placeholder='Choose an option', index = None) # Sector selection

btn1 = st.button(label = 'Show', key = 'word_cloud')

if btn1 and sector_name:
    data = word_cloud_df[word_cloud_df['sector'] == sector_name]['features'].dropna().values   # Filter data for the selected sector

    # Safely parse features and create a flattened list
    try:
        unique_list = [item for sublist in data for item in ast.literal_eval(sublist)]

    except:
        unique_list = []

    # Create feature text for WordCloud
    feature_text = ' '.join(unique_list)
    stopwords = set(STOPWORDS)

    if len(unique_list) != 0:

       # Generate the WordCloud

       wordcloud = WordCloud(width = 1200, height = 500, background_color ='black', stopwords = stopwords, min_font_size = 10).generate(feature_text)

       # Plot the WordCloud
       fig, ax = plt.subplots()
       ax.imshow(wordcloud)
       ax.axis("off")  # Turn off axis
       st.pyplot(fig)

    else:
        # Handle empty WordCloud scenario
        st.warning("No valid features found for the selected sector")

st.divider()


# -----------------------------------------------------------------
st.subheader('Tree Map: Properties Average Price by Sector')

l1 = df2['property_type'].unique().tolist()
l1.insert(0,'Overall')

property_type = st.selectbox(label = 'Property Type', options = l1, placeholder = 'Choose an option', index=None, key = 1)

btn2 = st.button(label = 'Show', key = 'avg_price')

if property_type == 'Overall' and btn2:

    temp = df2.groupby('sector')['price_in_cr'].mean().round(2).reset_index().rename(columns={'sector': 'Sector', 'price_in_cr': 'Average Price(In Crores)'})

    fig = px.treemap(temp, path=[px.Constant('Gurgaon'), 'Sector'], values='Average Price(In Crores)', color='Average Price(In Crores)', hover_name='Sector', color_continuous_scale='jet')
    fig.update_layout(height = 550, width = 1500)
    st.plotly_chart(fig, use_container_width=False)
    st.divider()

elif( (property_type == 'flat' or property_type == 'house') and btn2):

    temp = df2[(df2['property_type'] == property_type)].groupby('sector')['price_in_cr'].mean().round(2).reset_index().rename(columns = {'sector':'Sector','price_in_cr':'Average Price(In Crores)'})

    if property_type == 'flat':
       fig = px.treemap(temp, path = [px.Constant('Gurgaon'), 'Sector'], values = 'Average Price(In Crores)', color = 'Average Price(In Crores)', hover_name = 'Sector',color_continuous_scale = 'plasma')
       fig.update_layout(height = 550, width = 1500)
       st.plotly_chart(fig, use_container_width = True)
       st.divider()
    elif property_type == 'house':
        fig = px.treemap(temp, path=[px.Constant('Gurgaon'), 'Sector'], values='Average Price(In Crores)', color = 'Average Price(In Crores)', hover_name='Sector', color_continuous_scale = 'viridis')
        fig.update_layout(height = 550, width = 1500)
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

elif btn2:
    st.error('Please Select an Option')


# -----------------------------------------------------------------
st.subheader('Price by Built Up Area')

property_type = st.selectbox(label = 'Property Type', options = df2['property_type'].unique().tolist(), placeholder = 'Choose an option', index=None, key = 2)

btn3 = st.button(label = 'Show', key = 'price_by_built_up_area')

if btn3 and property_type is not None:

   temp = df2[df2['property_type'] == property_type]

   fig = px.scatter(temp, x='built_up_area', y='price_in_cr', color='bedroom', color_continuous_scale = 'plasma')
   fig.update_layout(xaxis_title='Built Up Area', yaxis_title='Price (In Crores)')
   st.plotly_chart(fig, use_container_width=True)

elif btn3:
    st.error('Please Select an Option')

st.divider()


# -----------------------------------------------------------------
st.subheader('Bedroom Distribution of Properties in Selected Locality')

sectors_list = sorted(df2['sector'].unique().tolist(), key = len)

sectors_list.insert(0,'Overall')

sector_name = st.selectbox(label = 'Locality', options = sectors_list, placeholder = 'Choose an option', index = None, key= 'bedroom_sector')

if sector_name == 'Overall':
    temp = df2['bedroom'] .value_counts().reset_index()
else:
    temp = df2[df2['sector'] == sector_name]['bedroom'] .value_counts().reset_index()

btn_bed = st.button(label='Show',key = 'bedroom')

if btn_bed and sector_name:
   fig = px.pie(temp, values = 'count', names = 'bedroom', hover_name = 'bedroom', hole = 0.4, )
   fig.update_traces(textinfo = 'label+percent')
   st.plotly_chart(fig, use_container_width=True)

if btn_bed and sector_name is None:
    st.error('Please Select an Option')

st.divider()


# -----------------------------------------------------------------
st.subheader('Price Range by Bedroom')
fig = px.box(df2, x = 'bedroom',  y = 'price_in_cr', color = 'bedroom', points = 'all')
fig.update_layout(xaxis_title = 'Bedroom', yaxis_title = 'Price(In Crores)')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# ----------------------------------------------------------------
st.subheader('Price Range by Bathroom')
temp = df2[df2['bathroom'] < 5]
fig = px.box(temp, x = 'bathroom',  y = 'price_in_cr', color = 'bathroom', points = 'all')
fig.update_layout(xaxis_title = 'Bathroom',  yaxis_title = 'Price(In Crores)', width = 800)
st.plotly_chart(fig, use_container_width=True)
st.divider()


# ----------------------------------------------------------------
st.subheader('Price Range by Luxury Type')
fig = px.box(df2,  x = 'price_in_cr', y = 'luxury_category', color = 'luxury_category')
fig.update_layout(xaxis_title = 'Price(In Crores)', yaxis_title = 'Luxury Category')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# ----------------------------------------------------------------
st.subheader('Price Range by Property Type')
fig = px.box(df2, x = 'price_in_cr', y = 'property_type', color = 'property_type')
fig.update_layout(xaxis_title = 'Price(In Crores)', yaxis_title = 'Property Type')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# ----------------------------------------------------------------
st.subheader('Distribution of Price by Property Type')

x_flats = df2[df2['property_type'] == 'flat']['price_in_cr'].values
x_houses = df2[df2['property_type'] == 'house']['price_in_cr'].values

hist_data = [x_flats, x_houses]
group_labels = ['flat', 'house']

fig = ff.create_distplot(hist_data, group_labels, colors = ['lightgreen', 'magenta'])
fig.update_layout(xaxis_title = 'Price in Crores (Cr)', yaxis_title = 'Density')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Property Type vs. Number of Bedroom Distribution')
crosstab = pd.crosstab(df2['property_type'], df2['bedroom'])

fig = px.imshow(crosstab, text_auto = True)
fig.update_layout(xaxis_title = 'Bedroom', yaxis_title = 'Property Type')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Property Type vs. Furnishing Type Distribution')
crosstab = pd.crosstab(df2['property_type'], df2['furnishing_type'])

fig = px.imshow(crosstab, text_auto = True)
fig.update_layout(xaxis_title = 'Furnishing Type', yaxis_title = 'Property Type')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Property Type vs. Floor Type Distribution')
crosstab = pd.crosstab(df2['property_type'], df2['floor_category'])

fig = px.imshow(crosstab , text_auto = True, color_continuous_scale = 'jet')
fig.update_layout(xaxis_title = 'Floor Type', yaxis_title = 'Property Type')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Property Type vs. Age Possession Distribution')
crosstab = pd.crosstab(df2['property_type'], df2['agepossession'])

fig = px.imshow(crosstab, text_auto = True, color_continuous_scale = 'viridis')
fig.update_layout(xaxis_title = 'Age Possession', yaxis_title = 'Property Type')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Property Type vs. Luxury Category Distribution')
crosstab = pd.crosstab(df2['property_type'], df2['luxury_category'])

fig = px.imshow(crosstab, text_auto = True, color_continuous_scale = 'plasma')
fig.update_layout(xaxis_title = 'Luxury Category', yaxis_title = 'Property Type')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Distribution of Built-Up Area by Property Type')
fig = px.box(df2, x = 'built_up_area', color = 'property_type')
fig.update_layout(xaxis_title = 'Built-Up Area (in Sqft)')
st.plotly_chart(fig, use_container_width=True)
st.divider()


# -----------------------------------------------------------------
st.subheader('Top 25 Expensive Socities with Average Price(In Crores)')

temp = pd.pivot_table(df3, index = 'society', values = 'price_in_cr', aggfunc = 'median').reset_index()
temp = temp.sort_values(by = 'price_in_cr',ascending = False).round(2).head(25)

fig = px.bar(temp, x= 'society', y = 'price_in_cr', color = 'society', text_auto = True)
fig.update_layout(xaxis_title = 'Society', yaxis_title = 'Average Price(In Crores)')
st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader('Top 25 Budget Friendly Socities with Average Price(In Crores)')

temp = pd.pivot_table(df3, index = 'society', values = 'price_in_cr', aggfunc = 'median').reset_index()
temp = temp.sort_values(by = 'price_in_cr',ascending = True).round(2).head(25)

fig = px.bar(temp, x= 'society', y = 'price_in_cr', color = 'society', text_auto = True)
fig.update_layout(xaxis_title = 'Society', yaxis_title = 'Average Price(In Crores)')
st.plotly_chart(fig, use_container_width=True)
st.divider()


#-----------------------------------------------------------------
st.subheader('Other Analytics')

btn_other = st.button(label='Show', key = 'other')

if btn_other:

      # -----------------------------------------------------------------
      col1, col2 = st.columns(2, border= True, gap = 'large')

      with col1:
         temp = df2.groupby('property_type')['price_in_cr'].mean().round(2).reset_index().rename(columns={'property_type': 'Property Type', 'price_in_cr': 'Average Price (In Crores)'})
         fig = px.bar(temp, x = 'Property Type', y = 'Average Price (In Crores)', color = 'Property Type',text_auto = True, color_discrete_map= {'flat':'#e377c2', 'house':'lightgreen'})
         fig.update_layout(title='Average Price by Property Type', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)

      with col2:
         temp = df2.groupby('bedroom')['price_in_cr'].mean().reset_index().round(2)
         temp['bedroom'] = temp['bedroom'].astype(str)

         fig = px.bar(temp, x='bedroom', y='price_in_cr', color='bedroom', text_auto=True)
         fig.update_layout(title='Average Price by Number of Bedroom', xaxis_title='Bedroom', yaxis_title='Average Price (In Crores)', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)

      st.divider()

      # -----------------------------------------------------------------

      col1, col2 = st.columns([0.55,0.45], border= True, gap = 'large')

      with col1:
         temp = df2.groupby('bathroom')['price_in_cr'].mean().reset_index().round(2)
         temp['bathroom'] = temp['bathroom'].astype(str)

         fig = px.bar(temp, x='bathroom', y='price_in_cr', color='bathroom', text_auto=True)
         fig.update_layout(title='Average Price by Number of Bathroom', xaxis_title='Bathroom', yaxis_title='Average Price (In Crores)', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)


      with col2:
          temp = df2.groupby('study room')['price_in_cr'].mean().reset_index().round(2)
          temp['study room'] = temp['study room'].astype(str)

          fig = px.bar(temp, x='study room', y='price_in_cr', color='study room', text_auto=True, color_discrete_map = {'0':'#2ca02c', '1':'#1f77b4'})
          fig.update_layout(title='Average Price by Study room', xaxis_title='Study Room', yaxis_title = 'Average Price (In Crores)', title_x = 0.25)
          st.plotly_chart(fig, use_container_width=True)


      st.divider()


      # --------------------------------------------------------------
      col1, col2 = st.columns(2, border= True, gap = 'large')

      with col1:
         temp = df2.groupby('servant room')['price_in_cr'].mean().round(2).reset_index()
         temp['servant room'] = temp['servant room'].astype(str)

         fig = px.bar(temp, x='servant room', y='price_in_cr', color='servant room', text_auto=True)
         fig.update_layout(title='Average Price by Servant Room', xaxis_title='Servant Room', yaxis_title='Average Price (In Crores)', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)

      with col2:

         temp = df2.groupby('store room')['price_in_cr'].mean().reset_index().round(2)
         temp['store room'] = temp['store room'].astype(str)

         fig = px.bar(temp, x='store room', y='price_in_cr', color='store room', text_auto=True)
         fig.update_layout(title='Average Price by Store Room', xaxis_title='Store Room', yaxis_title='Average Price (In Crores)', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)

      st.divider()

      # -----------------------------------------------------------------

      col1, col2 = st.columns([0.45,0.55], border= True, gap = 'large')

      with col1:
         temp = df2.groupby('luxury_category')['price_in_cr'].mean().sort_values(ascending = True).round(2).reset_index().rename(columns = {'luxury_category': 'Luxury Category', 'price_in_cr': 'Average Price(In Crores)'})
         fig = px.bar(temp, x = 'Luxury Category', y = 'Average Price(In Crores)', color = 'Luxury Category', text_auto = True)
         fig.update_layout(title='Average Price by Luxury Type', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)

      with col2:
         temp = df2.groupby('floor_category')['price_in_cr'].mean().sort_values(ascending = True).round(2).reset_index().rename(columns = {'floor_category': 'Floor Category', 'price_in_cr': 'Average Price(In Crores)'})
         fig = px.bar(temp, x = 'Floor Category', y = 'Average Price(In Crores)', color = 'Floor Category', text_auto = True)
         fig.update_layout(title='Average Price by Floor Type', title_x = 0.25)
         st.plotly_chart(fig, use_container_width=True)

      st.divider()


      # -----------------------------------------------------------------

      temp = df2.groupby('agepossession').agg({'built_up_area':'mean','price_in_cr':'mean'}).round(2).sort_values(by = 'price_in_cr', ascending = True).reset_index()

      temp.rename(columns = {'agepossession': 'Age Possession', 'built_up_area' : 'Built-Up Area', 'price_in_cr': 'Average Price(In Crores)'}, inplace = True)

      fig = px.bar(temp, x = 'Age Possession', y = 'Average Price(In Crores)', color = 'Built-Up Area', hover_name = 'Built-Up Area', text_auto = True, color_continuous_scale = 'twilight')
      fig.update_layout(title = 'Average Price vs Age Possession with Built-Up Area', title_x = 0.25)
      st.plotly_chart(fig, use_container_width=True)
      st.divider()


# -----------------------------------------------------------------
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
