import streamlit as st

# Set the theme colors
primary_color = "#8b00ff"  # Purple
background_color = "#000000"  # Black
text_color = "#ffffff"  # White
secondary_color = "#e68a00"  # Dark Yellow

# Apply theme styles
st.markdown(
    f"""
    <style>
    body {{
        background-color: {background_color} !important;
        color: {text_color};
    }}

    .stApp {{
        color: {text_color};
    }}

    .image-container {{
        opacity: 0.9;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
    }}

    .image-container img {{
        width: 100%;
        border-radius: 15px;
    }}

    .title-container {{
        background: linear-gradient(90deg, {primary_color}, {secondary_color});
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        transition: background 0.3s ease-in-out;
    }}

    .title-container:hover {{
        background: linear-gradient(90deg, {secondary_color}, {primary_color});
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Display image at the beginning with caption
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg", width=None, caption="DNA Structure")
st.markdown("</div>", unsafe_allow_html=True)

# Page title with a gradient background
st.title("Helical Hues Haven")
st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)

# User choice: Sign Up or Sign In
choice = st.radio("", ["Sign Up", "Sign In"])

# Sign-up section
if choice == "Sign Up":
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

