import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

def set_page_configuration():
    st.set_page_config(page_title="DNA Gallery", page_icon="🧬", layout="wide")

def filter_data(df, search_query):
    return df[df['Name'].str.contains(search_query, case=False) | df['Sequence'].str.contains(search_query, case=False, na=False)]

def sort_data(df, sort_option):
    if sort_option == 'Name':
        return df.sort_values(by='Name')
    elif sort_option == 'A Percentage':
        return df.assign(APercentage=lambda x: x['Sequence'].apply(lambda seq: (seq.count('A') / len(seq)) * 100)).sort_values(by='APercentage')
    elif sort_option == 'T Percentage':
        return df.assign(TPercentage=lambda x: x['Sequence'].apply(lambda seq: (seq.count('T') / len(seq)) * 100)).sort_values(by='TPercentage')
    elif sort_option == 'C Percentage':
        return df.assign(CPercentage=lambda x: x['Sequence'].apply(lambda seq: (seq.count('C') / len(seq)) * 100)).sort_values(by='CPercentage')
    elif sort_option == 'G Percentage':
        return df.assign(GPercentage=lambda x: x['Sequence'].apply(lambda seq: (seq.count('G') / len(seq)) * 100)).sort_values(by='GPercentage')
    else:
        return df

def display_gallery():
    st.title("DNA Gallery")

    # Sample DNA data (you can replace this with your actual data)
    gallery_data = [
        {"Name": "DNA1", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATGGGGGGGGGGGGGGGCG"},
        {"Name": "DNA2", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTTTTTTTTTTTTTTGGGTTTTTA"},
        {"Name": "DNA3", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGCCCCCCCCCCCCCCCCCCC"},
        {"Name": "DNA4", "Image_Path": "https://w0.peakpx.com/wallpaper/611/928/HD-wallpaper-dna-molecule-blue-neon-dna-deoxyribonucleic-acid-dna-nucleic-acid-structure-blue-science-background-medicine-blue-background-science-concepts-blue-neon-molecule-black-background-with-dna.jpg", "Sequence": "ATCGATCG"},
        {"Name": "DNA5", "Image_Path": "https://w0.peakpx.com/wallpaper/548/840/HD-wallpaper-blue-science-background-dna-molecule-background-chemistry-background-blue-neon-background-science-texture-dna-concepts.jpg", "Sequence": "GCTAGCTA"},
        {"Name": "DNA6", "Image_Path": "https://w0.peakpx.com/wallpaper/659/633/HD-wallpaper-3d-molecule-dna-biology-chemistry-molecule.jpg", "Sequence": "TAGCTAGCAAAAGGAAAAAAAAA"},
        {"Name": "DNA7", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATGGGGGGGGGGGGGGGCG"},
        {"Name": "DNA8", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTTTTTTTTTTTTTTGGGTTTTTA"},
        {"Name": "DNA9", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGCCCCCCCCCCCCCCCCCCC"},
        {"Name": "DNA10", "Image_Path": "https://w0.peakpx.com/wallpaper/611/928/HD-wallpaper-dna-molecule-blue-neon-dna-deoxyribonucleic-acid-dna-nucleic-acid-structure-blue-science-background-medicine-blue-background-science-concepts-blue-neon-molecule-black-background-with-dna.jpg", "Sequence": "ATCGATCG"},
        {"Name": "DNA11", "Image_Path": "https://w0.peakpx.com/wallpaper/548/840/HD-wallpaper-blue-science-background-dna-molecule-background-chemistry-background-blue-neon-background-science-texture-dna-concepts.jpg", "Sequence": "GCTAGCTA"},
        {"Name": "DNA12", "Image_Path": "https://w0.peakpx.com/wallpaper/659/633/HD-wallpaper-3d-molecule-dna-biology-chemistry-molecule.jpg", "Sequence": "TAGCTAGCAAAAGGAAAAAAAAA"},
        {"Name": "DNA13", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATGGGGGGGGGGGGGGGCG"},
        {"Name": "DNA14", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTTTTTTTTTTTTTTGGGTTTTTA"},
        {"Name": "DNA15", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGCCCCCCCCCCCCCCCCCCC"},
        {"Name": "DNA16", "Image_Path": "https://w0.peakpx.com/wallpaper/611/928/HD-wallpaper-dna-molecule-blue-neon-dna-deoxyribonucleic-acid-dna-nucleic-acid-structure-blue-science-background-medicine-blue-background-science-concepts-blue-neon-molecule-black-background-with-dna.jpg", "Sequence": "ATCGATCG"},
        {"Name": "DNA17", "Image_Path": "https://w0.peakpx.com/wallpaper/548/840/HD-wallpaper-blue-science-background-dna-molecule-background-chemistry-background-blue-neon-background-science-texture-dna-concepts.jpg", "Sequence": "GCTAGCTA"},
        {"Name": "DNA18", "Image_Path": "https://w0.peakpx.com/wallpaper/659/633/HD-wallpaper-3d-molecule-dna-biology-chemistry-molecule.jpg", "Sequence": "TAGCTAGCAAAAGGAAAAAAAAA"},
        {"Name": "DNA19", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATGGGGGGGGGGGGGGGCG"},
        {"Name": "DNA20", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTTTTTTTTTTTTTTGGGTTTTTA"},
        {"Name": "DNA21", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGCCCCCCCCCCCCCCCCCCC"},
        {"Name": "DNA22", "Image_Path": "https://w0.peakpx.com/wallpaper/611/928/HD-wallpaper-dna-molecule-blue-neon-dna-deoxyribonucleic-acid-dna-nucleic-acid-structure-blue-science-background-medicine-blue-background-science-concepts-blue-neon-molecule-black-background-with-dna.jpg", "Sequence": "ATCGATCG"},
        {"Name": "DNA23", "Image_Path": "https://w0.peakpx.com/wallpaper/548/840/HD-wallpaper-blue-science-background-dna-molecule-background-chemistry-background-blue-neon-background-science-texture-dna-concepts.jpg", "Sequence": "GCTAGCTA"},
        {"Name": "DNA24", "Image_Path": "https://w0.peakpx.com/wallpaper/659/633/HD-wallpaper-3d-molecule-dna-biology-chemistry-molecule.jpg", "Sequence": "TAGCTAGCAAAAGGAAAAAAAAA"},
        {"Name": "DNA25", "Image_Path": "https://wirecase3d.com/cdn/shop/products/dna1.jpg?v=1532865464&width=823", "Sequence": "ATCGATGGGGGGGGGGGGGGGCG"},
        {"Name": "DNA26", "Image_Path": "https://w0.peakpx.com/wallpaper/511/206/HD-wallpaper-artistic-dna-structure-3d.jpg", "Sequence": "GCTAGCTTTTTTTTTTTTTTGGGTTTTTA"},
        {"Name": "DNA27", "Image_Path": "https://w0.peakpx.com/wallpaper/310/101/HD-wallpaper-artistic-dna-structure.jpg", "Sequence": "TAGCTAGCCCCCCCCCCCCCCCCCCC"},
        {"Name": "DNA26", "Image_Path": "https://w0.peakpx.com/wallpaper/611/928/HD-wallpaper-dna-molecule-blue-neon-dna-deoxyribonucleic-acid-dna-nucleic-acid-structure-blue-science-background-medicine-blue-background-science-concepts-blue-neon-molecule-black-background-with-dna.jpg", "Sequence": "ATCGATCG"},
        {"Name": "DNA27", "Image_Path": "https://w0.peakpx.com/wallpaper/548/840/HD-wallpaper-blue-science-background-dna-molecule-background-chemistry-background-blue-neon-background-science-texture-dna-concepts.jpg", "Sequence": "GCTAGCTA"},
        {"Name": "DNA28", "Image_Path": "https://w0.peakpx.com/wallpaper/659/633/HD-wallpaper-3d-molecule-dna-biology-chemistry-molecule.jpg", "Sequence": "TAGCTAGCAAAAGGAAAAAAAAA"},

    ]

    # Create a DataFrame from the gallery_data
    df = pd.DataFrame(gallery_data)

    # Search functionality
    search_query = st.text_input("Search by gene ID or sequence:", "")
    filtered_df = filter_data(df, search_query)

    # Sorting options
    sort_option = st.selectbox("Sort DNA entries by:", ['Name', 'A Percentage', 'T Percentage', 'C Percentage', 'G Percentage'])

    # Sort the data based on the selected option
    sorted_df = sort_data(filtered_df, sort_option)

    # Pagination
    page_number = st.number_input("Enter page number:", min_value=1, max_value=(len(sorted_df) - 1) // 20 + 1, value=1)
    start_index = (page_number - 1) * 20
    end_index = min(start_index + 20, len(sorted_df))

    # Display the sorted and filtered DNA entries for the current page
    current_page_df = sorted_df[start_index:end_index]
    if not current_page_df.empty:
        # Define the number of columns and rows in the grid
        num_columns = 3
        num_rows = len(current_page_df) // num_columns + (len(current_page_df) % num_columns > 0)

        # Use Streamlit's columns layout manager for grid view
        cols = st.columns(num_columns)

        for row_index in range(num_rows):
            for col_index in range(num_columns):
                index = row_index * num_columns + col_index
                if index < len(current_page_df):
                    # Display DNA images and names in a grid
                    with cols[col_index]:
                        st.write(f"**{current_page_df.iloc[index]['Name']}**")

                        if 'Image_Path' in current_page_df.iloc[index]:
                            image_url = current_page_df.iloc[index]['Image_Path']

                            response = requests.get(image_url)
                            if response.status_code == 200:
                                image = Image.open(BytesIO(response.content))
                                # Adjust the image size for the grid view
                                st.image(image, caption=current_page_df.iloc[index]['Name'], width=200, use_column_width=False)

                                # Add a button to view full-size image
                                button_key = f"View Full Size Image {index}"  # Unique key incorporating the index
                                if st.button(button_key):
                                    display_full_size_image(image)

                                # Add a button to view nucleotide percentages graph
                                graph_button_key = f"View Nucleotide Graph {index} Button"  # Unique key incorporating the index and type
                                if st.button(graph_button_key):
                                    display_nucleotide_graph(current_page_df.iloc[index]['Sequence'])

                                # Add a download button for FASTA format for each DNA entry
                                download_button_key = f"Download FASTA {index}"
                                fasta_data = generate_fasta(current_page_df.iloc[[index]])
                                st.download_button(f"Download DNA Data (FASTA) - {current_page_df.iloc[index]['Name']}", fasta_data, file_name=f"dna_data_{index}.fasta", key=download_button_key)

                            else:
                                st.write(f"Failed to retrieve image for {current_page_df.iloc[index]['Name']}")

    else:
        st.write("No matching or sorted DNA entries found on this page.")

    # Check if there are more pages
    if end_index < len(sorted_df):
        st.write("No further entries on subsequent pages.")


def generate_fasta(df):
    fasta_lines = []

    for index, row in df.iterrows():
        fasta_lines.append(f">{row['Name']}\n{row['Sequence']}")

    return "\n".join(fasta_lines)


def display_nucleotide_graph(sequence):
    st.write("**Nucleotide Percentages:**")

    # Calculate nucleotide percentages
    nucleotide_counts = {"A": 0, "T": 0, "C": 0, "G": 0}
    total_nucleotides = len(sequence)

    for nucleotide in sequence:
        if nucleotide in nucleotide_counts:
            nucleotide_counts[nucleotide] += 1

    # Calculate percentages
    percentages = {key: (count / total_nucleotides) * 100 for key, count in nucleotide_counts.items()}

    st.write(f"A: {percentages['A']:.2f}%")
    st.write(f"T: {percentages['T']:.2f}%")
    st.write(f"C: {percentages['C']:.2f}%")
    st.write(f"G: {percentages['G']:.2f}%")

    # Create a bar chart for nucleotide percentages
    data = pd.DataFrame({"Nucleotide": list(percentages.keys()), "Percentage": list(percentages.values())})
    st.bar_chart(data.set_index("Nucleotide"))

def display_full_size_image(image):
    st.image(image, caption="Full Size Image", use_column_width=True)

# Run the app
if __name__ == '__main__':
    set_page_configuration()
    display_gallery()

