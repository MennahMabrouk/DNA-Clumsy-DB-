import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

# Set page config first
st.set_page_config(page_title="DNA Gallery", page_icon="🧬", layout="wide")

# Sample DNA data (you can replace this with your actual data)
gallery_data = [
    {"Name": "DNA1", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATCG"},
    {"Name": "DNA2", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTA"},
    {"Name": "DNA3", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGC"},
]

# Create a DataFrame from the gallery_data
df = pd.DataFrame(gallery_data)

def display_gallery():
    st.title("DNA Gallery")

    for index, row in df.iterrows():
        # Display DNA images and names in a single row
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{row['Name']}**")

            if 'Image_Path' in row:
                image_url = row['Image_Path']

                response = requests.get(image_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    # Adjust the image size for the gallery-like view
                    st.image(image, caption=row['Name'], width=300, use_column_width=False)
                else:
                    st.write(f"Failed to retrieve image for {row['Name']}")

        with col2:
            # Add a click event to open a new page for each DNA entry
            button_key = f"View {row['Name']}"
            if st.button(button_key):
                display_dna_page(row)

def display_dna_page(dna_entry):
    st.title(f"{dna_entry['Name']} Details")

    # Display other DNA information
    if 'Sequence' in dna_entry:
        st.write(f"**Sequence:** {dna_entry['Sequence']}")

    # Create a simple plot using Streamlit's line_chart
    x = np.arange(0, 10, 0.1)
    y = np.sin(x)

    data = pd.DataFrame({"x": x, "y": y})

    # Display the plot in Streamlit
    st.line_chart(data.set_index("x"))

# Run the app
if __name__ == '__main__':
    display_gallery()

