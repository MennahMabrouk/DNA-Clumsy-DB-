import streamlit as st
import cx_Oracle
from Project import signing, gallary
from Project.theme_utils import set_theme
from dotenv import load_dotenv
from Project.db_utils import get_oracle_connection_string  


load_dotenv()  
# Construct the connection string using the function
connection_string = get_oracle_connection_string()

# Set your Oracle database connection details
db_username = "m"
db_password = "00"
db_host = "localhost"
db_port = "1521"
db_service_name = "XE"  # Assuming XE is the service name based on your tnsnames.ora

# Construct the connection string
connection_string = f"{db_username}/{db_password}@{db_host}:{db_port}/{db_service_name}"

try:
    # Establish the connection
    connection = cx_Oracle.connect(connection_string)
    
    # Check if the connection is successful
    if connection:
        st.success("Connected to the Oracle database.")
    else:
        st.error("Failed to connect to the Oracle database.")


except cx_Oracle.DatabaseError as e:
    error, = e.args
    if error.code == 12514:
        st.error("ORA-12514: TNS:listener does not currently know of service requested in connect descriptor.")
    else:
        st.error(f"DatabaseError: {error}")



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

    st.write("Oracle Page - Database interaction code removed")

else:
    st.write("Page not found")
