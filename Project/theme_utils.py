# theme_utils.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
from io import BytesIO

def create_wave_pattern(amplitude, frequency, phase_shift, x_values):
    return amplitude * np.sin(frequency * x_values + phase_shift)

def generate_wave_background():
    fig, ax = plt.subplots(figsize=(10, 2))

    x_values = np.linspace(0, 10, 1000)
    wave1 = create_wave_pattern(0.5, 2, 0, x_values)
    wave2 = create_wave_pattern(0.3, 1, np.pi / 2, x_values)
    wave3 = create_wave_pattern(0.2, 1.5, np.pi / 4, x_values)

    combined_wave = wave1 + wave2 + wave3

    ax.plot(x_values, combined_wave, color='white')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_facecolor((0, 0, 0, 0))

    buffer = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    plt.close(fig)

    return buffer

def set_theme(theme):
    # Call generate_wave_background to get the dynamic wave background
    wave_image = generate_wave_background()

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

    # Apply theme styles along with the dynamic wave background
    st.markdown(
        f"""
        <style>
        body {{
            background: url('data:image/png;base64,{wave_image.getvalue().decode("utf-8")}');
            background-size: cover;
            background-attachment: fixed;
            color: {text_color} !important;
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
