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
page = st.sidebar.selectbox("Select Page", ["signing"])

elif page == "signing":
    signing.show()

else:
    st.write("Page not found")  # Handle the case when none of the pages match
