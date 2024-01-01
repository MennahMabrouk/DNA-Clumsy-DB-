import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px

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

    # Create a figure using plotly express
    fig = px.imshow()

    # Iterate through each DNA entry and add it to the figure
    for index, row in df.iterrows():
        image_url = row['Image_Path']
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # Resize the image for the grid view
            image = image.resize((150, 150))
            fig.add_trace(px.imshow(image).data[0])

    # Update the layout to create a grid view
    fig.update_layout(
        width=800,
        height=400,
        grid=dict(rows=1, columns=len(df)),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # Show the grid view
    st.plotly_chart(fig)

# Run the app
if __name__ == '__main__':
    display_gallery()
