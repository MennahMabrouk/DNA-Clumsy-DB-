import streamlit as st
from Project.theme_utils import set_theme
import re

def show():
    # Set theme to "dark_purple"
    set_theme("dark_purple")

    st.title("Sign In/Sign Up")

    # User choice: Sign Up or Sign In
    choice = st.radio("", ["Sign Up", "Sign In"])

    # Sign Up section
    if choice == "Sign Up":
        st.subheader("Sign Up")

        # Necessary details for Sign Up
        username = st.text_input("Username for signup")
        password = st.text_input("Password for signup", type="password")
        password_repeat = st.text_input("Repeat Password for signup", type="password")
        user_type = st.selectbox("User type:", ["Student", "Researcher", "Academic"])
        phone_number = st.text_input("Phone number:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=150)
        gender = st.radio("Gender:", ["Male", "Female", "Other"])

        # Password confirmation and validation for Sign Up
        if password != password_repeat:
            st.warning("Passwords do not match. Please re-enter.")
        elif len(password) < 8 or not any(char.isupper() for char in password) or not re.search("[@#$%^&+=]", password):
            st.warning("Password Requirements: \n"
                    "\n • At least 8 characters long"
                    "\n • At least one uppercase letter"
                    "\n • At least one symbol (@#$%^&+=)"
                )
            
        else:
            st.success("Password is valid.")

        # Display Sign Up button
        if st.button("Sign Up"):
            # Additional actions for Sign Up
            pass

# Sign-in section
if choice == "Sign In":
    st.subheader("Sign In")

    # Allow user to sign in by email or username
    signin_identifier = st.text_input("Email or username")
    signin_password = st.text_input("Password for signin", type="password")
    signin_button = st.button("Sign In")

    # Display gallery after sign in
    if signin_button:
        st.success("Sign in successful!")
        st.markdown("<h2>Welcome to the DNA Gallery!</h2>", unsafe_allow_html=True)
        gene_gallery()

# Set default theme to "dark_purple"
set_theme("dark_purple")

# Call the show function directly
show()
