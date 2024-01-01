import streamlit as st
from Project.theme_utils import set_theme

def show():
    st.title("Sign In/ Sign Up")

    # Day and Night Theme Toggle Inside Show Function
    if st.button("Toggle Theme Inside Show Function"):
        current_theme = st.session_state.get("theme", "day")
        new_theme = "night" if current_theme == "day" else "day"
        set_theme(new_theme)
        st.session_state.theme = new_theme


# Page title with a gradient background
st.title("Helical Hues Haven")
st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)

# Display image at the beginning with caption
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg", width=None, caption="DNA Structure")
st.markdown("</div>", unsafe_allow_html=True)

# User choice: Sign Up or Sign In
choice = st.radio("", ["Sign Up", "Sign In"])

# Sign-up section
if choice == "Sign Up":
    st.subheader("Sign Up")
    signup_username = st.text_input("Username for signup")
    signup_password = st.text_input("Password for signup", type="password")

    # Additional details with improved styling
    with st.form("signup-form"):
        st.text("Additional Details")
        user_type = st.selectbox("User type:", ["Student", "Researcher", "Academic"])
        phone_number = st.text_input("Phone number:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=150)
        gender = st.radio("Gender:", ["Male", "Female", "Other"])

        signup_button = st.form_submit_button("Sign Up")

# Sign-in section
elif choice == "Sign In":
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

