import streamlit as st
import pandas as pd
from PIL import Image

# Sample DNA data (you can replace this with your actual data)
# Sample DNA data with direct image links
dna_data = {
    'Name': ['DNA1', 'DNA2', 'DNA3'],
    'Image_Path': [
'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwirecase3d.com%2Fproducts%2Fdna-3d-model&psig=AOvVaw0hqp_y50IY2MsJs68m95ST&ust=1704177903344000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNippNrLu4MDFQAAAAAdAAAAABAD'
'https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fimages%2Fdna-3d-dna-strands%2F82359905&psig=AOvVaw0hqp_y50IY2MsJs68m95ST&ust=1704177903344000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNippNrLu4MDFQAAAAAdAAAAABAP'
'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fphotos%2F3d-dna&psig=AOvVaw0hqp_y50IY2MsJs68m95ST&ust=1704177903344000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNippNrLu4MDFQAAAAAdAAAAABAV'
    ],
    'Sequence': ['ATCGATCG', 'GCTAGCTA', 'TAGCTAGC']
}


df = pd.DataFrame(dna_data)

def display_gallery():
    st.title("DNA Gallery")

    for index, row in df.iterrows():
        # Display DNA images and names in side windows
        col1, col2 = st.columns(2)  # Use st.columns() instead of st.beta_columns()
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

# Run the app
if __name__ == '__main__':
    display_gallery()
