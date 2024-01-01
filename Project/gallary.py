import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import numpy as np

def set_page_configuration():
    st.set_page_config(page_title="DNA Gallery", page_icon="🧬", layout="wide")

def display_gallery():
    st.title("DNA Gallery")

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

                    # Add a click event to open a new page for each DNA entry
                    button_key = f"View {df.iloc[index]['Name']}"
                    if st.button(button_key):
                        display_dna_page(df.iloc[index])

def display_dna_page(dna_entry):
    st.title(f"{dna_entry['Name']} Details")

    # Display DNA information
    if 'Sequence' in dna_entry:
        st.write(f"**Sequence:** {dna_entry['Sequence']}")

        # Calculate nucleotide percentages
        nucleotide_counts = {"A": 0, "T": 0, "C": 0, "G": 0}
        total_nucleotides = len(dna_entry['Sequence'])

        for nucleotide in dna_entry['Sequence']:
            if nucleotide in nucleotide_counts:
                nucleotide_counts[nucleotide] += 1

        # Calculate percentages
        percentages = {key: (count / total_nucleotides) * 100 for key, count in nucleotide_counts.items()}

        st.write("**Nucleotide Percentages:**")
        st.write(f"A: {percentages['A']:.2f}%")
        st.write(f"T: {percentages['T']:.2f}%")
        st.write(f"C: {percentages['C']:.2f}%")
        st.write(f"G: {percentages['G']:.2f}%")

        # Create a bar chart for nucleotide percentages
        data = pd.DataFrame({"Nucleotide": list(percentages.keys()), "Percentage": list(percentages.values())})
        st.bar_chart(data.set_index("Nucleotide"))

# Run the app
if __name__ == '__main__':
    set_page_configuration()
    display_gallery()

