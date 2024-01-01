import streamlit as st
import pandas as pd
from PIL import Image

# Sample DNA data (you can replace this with your actual data)
dna_data = {
    'Name': ['DNA1', 'DNA2', 'DNA3'],
    'Image_Path': ['path_to_dna1_image.jpg', 'path_to_dna2_image.jpg', 'path_to_dna3_image.jpg'],
    'Sequence': ['ATCGATCG', 'GCTAGCTA', 'TAGCTAGC']
}

df = pd.DataFrame(dna_data)

def display_gallery():
    st.title("DNA Gallery")

    for index, row in df.iterrows():
        # Display DNA images and names in side windows
        col1, col2 = st.beta_columns(2)
        with col1:
            image = Image.open(row['Image_Path'])
            st.image(image, caption=row['Name'], use_column_width=True)

        with col2:
            st.write(f"**{row['Name']}**")

        # Add a click event to open a new page for each DNA entry
        if col1.button(f"View {row['Name']}"):
            display_dna_page(row)

def display_dna_page(dna_entry):
    st.title(f"{dna_entry['Name']} Details")

    # Display the full DNA image with all info and sequences
    image = Image.open(dna_entry['Image_Path'])
    st.image(image, caption=dna_entry['Name'], use_column_width=True)

    # Display other DNA information
    st.write(f"**Sequence:** {dna_entry['Sequence']}")
    # Add more information as needed
