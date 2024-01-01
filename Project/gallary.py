import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import numpy as np

# Set page config first
st.set_page_config(page_title="DNA Gallery", page_icon="🧬", layout="wide")

# Sample DNA data (you can replace this with your actual data)
gallery_data = [
    {"Name": "DNA1", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATCG"},
    {"Name": "DNA2", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTA"},
    {"Name": "DNA3", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGC"},
    {"Name": "DNA4", "Image_Path": "https://w0.peakpx.com/wallpaper/611/928/HD-wallpaper-dna-molecule-blue-neon-dna-deoxyribonucleic-acid-dna-nucleic-acid-structure-blue-science-background-medicine-blue-background-science-concepts-blue-neon-molecule-black-background-with-dna.jpg", "Sequence": "ATCGATCG"},
    {"Name": "DNA5", "Image_Path": "https://w0.peakpx.com/wallpaper/548/840/HD-wallpaper-blue-science-background-dna-molecule-background-chemistry-background-blue-neon-background-science-texture-dna-concepts.jpg", "Sequence": "GCTAGCTA"},
    {"Name": "DNA6", "Image_Path": "https://w0.peakpx.com/wallpaper/659/633/HD-wallpaper-3d-molecule-dna-biology-chemistry-molecule.jpg", "Sequence": "TAGCTAGC"},
]

# Create a DataFrame from the gallery_data
df = pd.DataFrame(gallery_data)

def display_gallery():
    st.title("DNA Gallery")

    # Define the number of columns and rows in the grid
    num_columns = 3
    num_rows = len(df) // num_columns + (len(df) % num_columns > 0)

    # Use Streamlit's columns layout manager for grid view
    cols = st.columns(num_columns)

    for row_index in range(num_rows):
        for col_index in range(num_columns):
            index = row_index * num_columns + col_index
            if index < len(df):
                # Display DNA images and names in a grid
                with cols[col_index]:
                    st.write(f"**{df.iloc[index]['Name']}**")

                    if 'Image_Path' in df.iloc[index]:
                        image_url = df.iloc[index]['Image_Path']

                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content))
                            # Adjust the image size for the grid view
                            st.image(image, caption=df.iloc[index]['Name'], width=200, use_column_width=False)
                        else:
                            st.write(f"Failed to retrieve image for {df.iloc[index]['Name']}")
                            print(f"Failed to retrieve image for {df.iloc[index]['Name']}. Status code: {response.status_code}")

                    # Add a click event to open a new page for each DNA entry
                    button_key = f"View {df.iloc[index]['Name']}"
                    if st.button(button_key):
                        display_dna_page(df.iloc[index])

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

