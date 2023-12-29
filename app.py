import streamlit as st

# Set page title and icon
st.set_page_config(
    page_title="DNA Harmony Hub",
    page_icon="🔒",
    layout="centered",
)

# Set background color to purple
st.markdown(
    """
    <style>
    body {
        background-color: #6e42c7;
        color: white;
    }

    .stApp {
        color: white;
    }

    .image-container {
        opacity: 0.9; /* Adjust the opacity for the fade effect */
        border-radius: 15px; /* Adjust the border-radius for rounded corners */
        overflow: hidden;
    }

    .image-container img {
        width: 100%;
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display image at the beginning
image_url = "https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg"
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image(image_url, width=None)
st.markdown("</div>", unsafe_allow_html=True)

# Page title
st.title("Helical Hues Haven")

# User choice: Sign Up or Sign In
choice = st.radio("Choose an option:", ["Sign Up", "Sign In"])

# Sign-up section
if choice == "Sign Up":
    st.subheader("Sign Up")
    signup_username = st.text_input("Enter your username for signup", key="signup_username")
    signup_password = st.text_input("Enter your password for signup", type="password", key="signup_password")

    # Additional details
    user_type = st.selectbox("Select your user type:", ["Student", "Researcher", "Academic"])
    phone_number = st.text_input("Enter your phone number:")
    email = st.text_input("Enter your email:")
    age = st.number_input("Enter your age:", min_value=0, max_value=150)
    gender = st.radio("Select your gender:", ["Male", "Female", "Other"])

    signup_button = st.button("Sign Up")

    if signup_button:
        # Add your sign-up logic here
        # You can access the collected data like signup_username, signup_password, user_type, phone_number, email, age, gender
        st.success("Account created successfully!")

# Sign-in section
elif choice == "Sign In":
    st.subheader("Sign In")

    # Allow user to sign in by email or username
    signin_identifier = st.text_input("Enter your email or username", key="signin_identifier")
    signin_password = st.text_input("Enter your password for signin", type="password", key="signin_password")
    signin_button = st.button("Sign In")

    if signin_button:
        # Add your sign-in logic here
        # You can access the collected data like signin_identifier and signin_password
        st.success("Sign in successful!")

# Footer
st.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; color: white;">
        © 2023 Purple Auth. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
