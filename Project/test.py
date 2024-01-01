# Project/test.py
import streamlit as st
from project.theme_utils import set_theme

def show():
    st.title("Test Page")
    st.write("This is the content of the second page.")

    # Day and Night Theme Toggle
    if st.button("Toggle Theme"):
        current_theme = st.session_state.get("theme", "day")
        new_theme = "night" if current_theme == "day" else "day"
        set_theme(new_theme)
        st.session_state.theme = new_theme


# Day and Night Theme Toggle
if st.button("Toggle Theme"):
    current_theme = st.session_state.get("theme", "day")
    new_theme = "night" if current_theme == "day" else "day"
    set_theme(new_theme)
    st.session_state.theme = new_theme

# Navigation menu in the sidebar
selected_page = st.sidebar.radio("Select a page", ["Sign Up", "Sign In"])

# Page title with a gradient background
st.title("Helical Hues Haven")
st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)

# Display image at the beginning with caption
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg", width=None, caption="DNA Structure")
st.markdown("</div>", unsafe_allow_html=True)

# Render selected page
if selected_page == "Sign Up":
    st.subheader("Sign Up")
    signup_username = st.text_input("Enter your username for signup", key="signup_username")
    signup_password = st.text_input("Enter your password for signup", type="password", key="signup_password")

    # Additional details with improved styling
    with st.form("signup-form"):
        st.text("Additional Details")
        user_type = st.selectbox("Select your user type:", ["Student", "Researcher", "Academic"])
        phone_number = st.text_input("Enter your phone number:")
        email = st.text_input("Enter your email:")
        age = st.number_input("Enter your age:", min_value=0, max_value=150)
        gender = st.radio("Select your gender:", ["Male", "Female", "Other"])

        signup_button = st.form_submit_button("Sign Up")

elif selected_page == "Sign In":
    st.subheader("Sign In")

    # Allow user to sign in by email or username
    signin_identifier = st.text_input("Enter your email or username", key="signin_identifier")
    signin_password = st.text_input("Enter your password for signin", type="password", key="signin_password")
    signin_button = st.button("Sign In")

    if signin_button:
        # Add your sign-in logic here
        # You can access the collected data like signin_identifier and signin_password
        st.success("Sign in successful!")
