import streamlit as st
import pandas as pd
import cx_Oracle
from PIL import Image
import requests
from io import BytesIO
from Project.db_utils import get_oracle_connection_string

def fetch_data_from_database(connection_string, table_names):
    data = {}
    try:
        connection = cx_Oracle.connect(connection_string)
        cursor = connection.cursor()

        for table_name in table_names:
            # Fetch data for each table
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            table_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Store data in the dictionary
            data[table_name] = table_data

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        st.error(f"DatabaseError: {error}")
    
    return data



def set_page_configuration():
    st.set_page_config(page_title="DNA Gallery", page_icon="🧬", layout="wide")

def filter_data(df, search_query):
    # Adjust column names according to your actual data
    return df[df['GENE_NAME'].str.contains(search_query, case=False) | df['DNA_SEQ'].str.contains(search_query, case=False, na=False)]

def merge_data(genes_data, images_data, sequences_data):
    genes_df = pd.DataFrame(genes_data, columns=["GENE_ID", "GENE_NAME", "COMMENTS", "GENE_TYPE"])
    images_df = pd.DataFrame(images_data, columns=["GENE_ID", "IMAGE_FILE"])
    sequences_df = pd.DataFrame(sequences_data, columns=["SEQ_ID", "GENE_ID", "DNA_SEQ", "SEQ_LENGTH"])

    # Merge the DataFrames based on GENE_ID
    merged_data = pd.merge(genes_df, images_df, on="GENE_ID", how="inner")
    merged_data = pd.merge(merged_data, sequences_df, on="GENE_ID", how="inner")
    
    # Select only the "IMAGE_FILE" column
    merged_data = merged_data[["GENE_ID", "GENE_NAME", "COMMENTS", "GENE_TYPE", "IMAGE_FILE", "SEQ_ID", "DNA_SEQ", "SEQ_LENGTH"]]
    
    return merged_data


def sort_data(df, sort_option):
    if sort_option == 'Name':
        return df.sort_values(by='GENE_NAME')
    elif sort_option == 'A Percentage':
        return df.assign(APercentage=lambda x: x['DNA_SEQ'].apply(lambda seq: (seq.count('A') / len(seq)) * 100)).sort_values(by='APercentage')
    elif sort_option == 'T Percentage':
        return df.assign(TPercentage=lambda x: x['DNA_SEQ'].apply(lambda seq: (seq.count('T') / len(seq)) * 100)).sort_values(by='TPercentage')
    elif sort_option == 'C Percentage':
        return df.assign(CPercentage=lambda x: x['DNA_SEQ'].apply(lambda seq: (seq.count('C') / len(seq)) * 100)).sort_values(by='CPercentage')
    elif sort_option == 'G Percentage':
        return df.assign(GPercentage=lambda x: x['DNA_SEQ'].apply(lambda seq: (seq.count('G') / len(seq)) * 100)).sort_values(by='GPercentage')
    else:
        return df

def display_gallery(connection_string):
    # Fetching data from the database
    table_names = ["GENES", "SEQUENCES", "IMAGES"]
    data = fetch_data_from_database(connection_string, table_names)

    # Check if data retrieval was successful for all tables
    if all(data.get(table_name) is not None for table_name in table_names):
        genes_data, sequences_data, images_data = (data[table_name] for table_name in table_names)

        # Merge data
        gallery_data = merge_data(genes_data, images_data, sequences_data)
        gallery_data = merge_data(genes_data, images_data, sequences_data)


        # Create a DataFrame from the gallery_data
        df = pd.DataFrame(gallery_data)

        # Search functionality
        search_query = st.text_input("Search by gene ID or sequence:", "")
        filtered_df = filter_data(df, search_query)

        # Sorting options
        sort_option = st.selectbox("Sort DNA entries by:", ['Name', 'A Percentage', 'T Percentage', 'C Percentage', 'G Percentage'])

        # Sort the data based on the selected option
        sorted_df = sort_data(df, sort_option)

        # Pagination
        page_size = 9
        total_pages = (len(sorted_df) - 1) // page_size + 1
        page_number = st.number_input("Enter page number:", min_value=1, max_value=total_pages, value=1)
        start_index = (page_number - 1) * page_size
        end_index = min(start_index + page_size, len(sorted_df))

        # Display the sorted and filtered DNA entries for the current page
        current_page_df = sorted_df[start_index:end_index]

        # Debugging statements
        st.write(f"Start Index: {start_index}, End Index: {end_index}, Total Rows: {len(sorted_df)}")
        st.write(f"Sorted DataFrame:")
        st.write(sorted_df)

        # Check if there are more pages
        if end_index < len(sorted_df):
            st.write(f"No further entries on subsequent pages. Total pages: {total_pages}")
        else:
            st.write(f"No matching or sorted DNA entries found on this page. Total pages: {total_pages}")


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
                            st.write(f"**{current_page_df.iloc[index]['GENE_NAME']}**")

                            # Check if the 'IMAGE_FILE' column exists
                            if 'IMAGE_FILE' in current_page_df.columns:
                                image_url = current_page_df.iloc[index]['IMAGE_FILE']

                                # Check if the image URL is null or empty
                                if pd.isnull(image_url) or not image_url.strip():
                                    # If null or empty, use the default image URL
                                    image_url = "https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg"

                                response = requests.get(image_url)
                                if response.status_code == 200:
                                    image = Image.open(BytesIO(response.content))
                                    # Adjust the image size for the grid view
                                    st.image(image, caption=current_page_df.iloc[index]['GENE_NAME'], width=200, use_column_width=False)

                                    # Add a button to view full-size image
                                    button_key = f"View Full Size Image {index}"  # Unique key incorporating the index
                                    if st.button(button_key):
                                        display_full_size_image(image)

                                    # Add a button to view nucleotide percentages graph
                                    graph_button_key = f"View Nucleotide Graph {index} Button"  # Unique key incorporating the index and type
                                    if st.button(graph_button_key):
                                        display_nucleotide_graph(current_page_df.iloc[index]['DNA_SEQ'])

                                    # Add a download button for FASTA format for each DNA entry
                                    download_button_key = f"Download FASTA {index}"
                                    fasta_data = generate_fasta(current_page_df.iloc[[index]])
                                    st.download_button(f"Download DNA Data (FASTA) - {current_page_df.iloc[index]['GENE_NAME']}", fasta_data, file_name=f"dna_data_{index}.fasta", key=download_button_key)

                                else:
                                    st.write(f"Failed to retrieve image for {current_page_df.iloc[index]['GENE_NAME']}")

            # Pagination information
            st.write(f"Page {page_number}/{total_pages}")

        else:
            st.write("No matching or sorted DNA entries found on this page.")

    else:
        st.error("Failed to fetch data from one or more tables in the database.")


def generate_fasta(df):
    fasta_lines = []

    for index, row in df.iterrows():
        fasta_lines.append(f">{row['GENE_NAME']}\n{row['DNA_SEQ']}")  # Fix the column names

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

if __name__ == '__main__':
    # Replace "your_connection_string" with your actual Oracle database connection string
    connection_string = get_oracle_connection_string()
    
    # Set page configuration
    set_page_configuration()

    # Display the gallery
    display_gallery(connection_string)
