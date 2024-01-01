import streamlit as st
from project import test

# Set the theme colors
def set_theme(theme):
    if theme == "day":
        primary_color = "#8b00ff"  # Purple
        background_color = "#ffffff"  # White
        text_color = "#000000"  # Black
        secondary_color = "#e68a00"  # Dark Yellow
    elif theme == "night":
        primary_color = "#8b00ff"  # Purple
        background_color = "#000000"  # Black
        text_color = "#ffffff"  # White
        secondary_color = "#e68a00"  # Dark Yellow
    else:
        raise ValueError("Invalid theme")

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

# Day and Night Theme Toggle
if st.button("Toggle Theme"):
    current_theme = st.session_state.get("theme", "day")
    new_theme = "night" if current_theme == "day" else "day"
    set_theme(new_theme)
    st.session_state.theme = new_theme

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Home", "Test", "Contact"])

# Display content based on selected page
if page == "Home":
    # Display image at the beginning with caption
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg", width=None, caption="DNA Structure")
    st.markdown("</div>", unsafe_allow_html=True)

    # Page title with a gradient background
    st.title("Helical Hues Haven")
    st.markdown('<div class="title-container"></div>', unsafe_allow_html=True)
elif page == "Test":
    # Call the test.py file in the project directory
    test.show()
elif page == "Contact":
    st.title("Contact Us")
    st.write("Feel free to reach out to us for any inquiries or collaborations.")
    # Add more content for the "Contact" page as needed
