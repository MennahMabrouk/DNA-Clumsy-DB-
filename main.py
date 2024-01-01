# Project/main.py
import streamlit as st
from Project import signing
from Project.theme_utils import set_theme

# Set default theme
set_theme("day")

# Day and Night Theme Toggle
if st.button("Toggle Theme"):
    current_theme = st.session_state.get("theme", "day")
    new_theme = "night" if current_theme == "day" else "day"
    set_theme(new_theme)
    st.session_state.theme = new_theme

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Home", "signing", "Contact"])

# Display content based on selected page
if page == "Home":
    # Display image at the beginning with caption
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg", width=None, caption="DNA Structure")
    st.markdown("</div>", unsafe_allow_html=True)

    # Page title with a gradient background
    st.title("Helical Hues Haven")
    st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)
elif page == "signing":
    # Call the show function directly from signing.py
    signing.show()
elif page == "Contact":
    st.title("Contact Us")
    st.write("Feel free to reach out to us for any inquiries or collaborations.")
    # Add more content for the "Contact" page as needed

    signing.show()
elif page == "Contact":
    st.title("Contact Us")
    st.write("Feel free to reach out to us for any inquiries or collaborations.")
    # Add more content for the "Contact" page as needed
