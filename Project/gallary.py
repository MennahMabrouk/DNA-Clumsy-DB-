import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Set page config first
st.set_page_config(page_title="DNA Gallery", page_icon="🧬", layout="wide")

# Sample DNA data (you can replace this with your actual data)
dna_data = {
    'Name': ['DNA1', 'DNA2', 'DNA3'],
    'Image_Path': [
        'https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823',
        'https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg',
        'https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg'
    ],
    'Sequence': ['ATCGATCG', 'GCTAGCTA', 'TAGCTAGC']
}

# Create a DataFrame with potentially different lengths
df = pd.DataFrame({key: pd.Series(value) for key, value in dna_data.items()})

def extract_image_url(search_url):
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img', class_='t0fcAb')
    
    if img_tags:
        return img_tags[0]['src']

    return None

def display_gallery():
    st.title("DNA Gallery")

    for index, row in df.iterrows():
        # Display DNA images and names in a single row
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{row['Name']}**")

        if 'Image_Path' in row:
            search_url = row['Image_Path']
            image_url = extract_image_url(search_url)

            if image_url:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=row['Name'], use_column_width=True)
            else:
                st.write(f"Failed to retrieve image for {row['Name']}")

        # Add a click event to open a new page for each DNA entry
        button_key = f"View {row['Name']}"
        if col1.button(button_key):
            display_dna_page(row)

def display_dna_page(dna_entry):
    st.title(f"{dna_entry['Name']} Details")

    # Display other DNA information
    if 'Sequence' in dna_entry:
        st.write(f"**Sequence:** {dna_entry['Sequence']}")

# Run the app
if __name__ == '__main__':
    display_gallery()
