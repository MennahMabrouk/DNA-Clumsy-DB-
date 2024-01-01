import streamlit as st
from Project.theme_utils import set_theme
import re

def show():
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
            st.warning("Password must be at least 8 characters long and contain at least one uppercase letter and one symbol.")
            st.info(
                "Password Requirements:"
                "\n • At least 8 characters long"
                "\n • At least one uppercase letter"
                "\n • At least one symbol (@#$%^&+=)"
            )
        else:
            st.success("Password is valid.")

    # Display Sign Up button for both cases
    st.button("Sign Up" if choice == "Sign Up" else "Sign In")

    # Display success message after Sign In
    if st.button("Sign In") and choice == "Sign In":
        st.success("Sign in successful!")
        st.markdown("<h2>Welcome to the DNA Gallery!</h2>", unsafe_allow_html=True)
        # Assuming gene_gallery() is defined somewhere
        # gene_gallery()

# Set default theme
set_theme("day")

# Call the show function directly
show()

