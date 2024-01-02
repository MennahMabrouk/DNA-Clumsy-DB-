# Project/main.py
import streamlit as st
import cx_Oracle
from Project import signing, gallary 
from Project.theme_utils import set_theme

# Set default theme
set_theme("day")

# Function to connect to the Oracle database
def connect_to_oracle():
    username = "m"
    password = "00"
    host = "localhost"
    port = "1521"
    service_name = "your_service_name"  # Replace with your actual Oracle service name

    connection_str = f"{username}/{password}@{host}:{port}/{service_name}"
    connection = cx_Oracle.connect(connection_str)
    return connection

# Function to execute a sample SQL query
def execute_query(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table")
    result = cursor.fetchall()
    cursor.close()
    return result

# Day and Night Theme Toggle
if st.button("Toggle Theme"):
    current_theme = st.session_state.get("theme", "day")
    new_theme = "night" if current_theme == "day" else "day"
    set_theme(new_theme)
    st.session_state.theme = new_theme

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Home", "Signing", "DNA Gallery", "Oracle Page"])  # Added "Oracle Page"

if page == "Home":
    # Display image at the beginning with caption
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg", width=None, caption="DNA Structure")
    st.markdown("</div>", unsafe_allow_html=True)

    # Page title with a gradient background
    st.title("Helical Hues Haven")
    st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)

elif page == "Signing":
    # Call the signing.py file in the project directory
    signing.show()

elif page == "DNA Gallery":
    # Call the display_gallery function from gallary.py
    gallary.display_gallery()

elif page == "Oracle Page":
    # Connect to Oracle and execute a sample query
    oracle_connection = connect_to_oracle()
    result = execute_query(oracle_connection)
    st.write("Oracle Query Result:", result)

else:
    st.write("Page not found")

