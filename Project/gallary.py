import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urlparse

# Sample DNA data (you can replace this with your actual data)
# Sample DNA data with direct image links
dna_data = {
    'Name': ['DNA1', 'DNA2', 'DNA3'],
    'Image_Path': [
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwirecase3d.com%2Fproducts%2Fdna-3d-model&psig=AOvVaw0hqp_y50IY2MsJs68m95ST&ust=1704177903344000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNippNrLu4MDFQAAAAAdAAAAABAD',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fimages%2Fdna-3d-dna-strands%2F82359905&psig=AOvVaw0hqp_y50IY2MsJs68m95ST&ust=1704177903344000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNippNrLu4MDFQAAAAAdAAAAABAP',
        'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fphotos%2F3d-dna&psig=AOvVaw0hqp_y50IY2MsJs68m95ST&ust=1704177903344000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNippNrLu4MDFQAAAAAdAAAAABAV'
    ],
    'Sequence': ['ATCGATCG', 'GCTAGCTA', 'TAGCTAGC']
}

# Create a DataFrame with potentially different lengths
df = pd.DataFrame({key: pd.Series(value) for key, value in dna_data.items()})

def display_gallery():
    st.title("DNA Gallery")

    for index, row in df.iterrows():
        # Display DNA images and names in a single row
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{row['Name']}**")

        if 'Image_Path' in row:
            image_paths = row['Image_Path']
            for path in image_paths:
                # Check if the URL has a valid schema
                parsed_url = urlparse(path)
                if parsed_url.scheme and parsed_url.netloc:
                    response = requests.get(path)
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=row['Name'], use_column_width=True)
                else:
                    st.write(f"Invalid URL for {row['Name']}")

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
