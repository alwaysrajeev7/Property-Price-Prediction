import streamlit as st

# Set the page config
st.set_page_config(page_title = 'Property Price Prediction', page_icon='🏡', layout = 'wide')

# Custom CSS for styling
st.markdown("""
    <style>
        div.block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


# Add the title with custom styling
st.markdown("<h1 style='text-align: center; font-family: Arial, sans-serif;'> Gurgaon Property Price Prediction 🏡 </h1>",unsafe_allow_html=True )


# Introduction
st.markdown("""
Welcome to the **Gurgaon Real Estate Price Prediction** project—an advanced data-driven solution designed to analyze and predict real estate prices in Gurgaon with precision. 

This project leverages comprehensive real estate data, providing both insightful analytics and accurate price predictions to assist buyers, sellers, and investors in making informed decisions.
""")

# Project Modules
st.header("Project Modules")

# Analytics Module
st.subheader("1. Analytics Module")
st.markdown("""
This module offers an in-depth analysis of Gurgaon’s real estate market through interactive visualizations and statistical insights. **Key features include:**

- **Price Trends 📈:** Analyze price trends across different sectors.  
- **Distribution Analysis 📊:** Understand property types, bedrooms, bathrooms, and luxury categories.  
- **Correlation Analysis 🔍:** Discover relationships between price and various property features.  
- **Geo-mapping & Wordcloud 🌍🧠:** Gain spatial insights and visualize key terms influencing prices.  
- **Comparative Charts 📉:** Explore side-by-side distplots and bar charts for detailed property evaluation.  
- **Wordcloud 💬:** See key features in flats across sectors to understand the most influential attributes.
""")

# Price Predictor Module
st.subheader("2. Price Predictor Module")
st.markdown("""
This module allows users to input specific property features (e.g., sector, built-up area, furnishing type, number of bedrooms, bathrooms, etc.) to predict the estimated price of real estate properties in Gurgaon.

It utilizes a robust machine learning model trained on historical property data to deliver **accurate predictions**.
""")

# Key Features
st.header("Key Features")
st.markdown("""
- 🚀 **User-friendly Interface:** Designed for seamless navigation.
- 🔍 **Dynamic Visualizations:** Interactive charts powered by Plotly.
- 📂 **Real-time Predictions:** Get instant price estimates based on your inputs.
- 🌍 **Data-Driven Insights:** Tailored for buyers, sellers, and real estate professionals.

This project aims to **simplify real estate decision-making** by combining data analytics with predictive modeling, making it a valuable tool for anyone interested in Gurgaon’s real estate landscape.
""")

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
