# theme_utils.py
import streamlit as st

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
    elif theme == "dark_purple":
        primary_color = "#4b0082"  # Dark Purple
        background_color = "#1E1E1E"  # Dark background
        text_color = "#ffffff"  # White text
        secondary_color = "#800080"  # Purple
    else:
        raise ValueError("Invalid theme")

    # Define common styles
    common_styles = f"""
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
    """

    # Apply theme styles
    st.markdown(f"<style>{common_styles}</style>", unsafe_allow_html=True)


