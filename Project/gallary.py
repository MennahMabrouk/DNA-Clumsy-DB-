import base64
import requests
import cx_Oracle
import pandas as pd
from Bio import SeqIO
from PIL import Image
import streamlit as st
from io import BytesIO
from io import StringIO
from Bio.Seq import Seq
from io import StringIO
from Bio.SeqIO import write
from Bio.SeqUtils import nt_search
from Bio.SeqRecord import SeqRecord
from io import BytesIO, TextIOWrapper
from PIL import Image, ImageDraw, UnidentifiedImageError
from Project.db_utils import get_oracle_connection_string


@st.cache_data()
def fetch_data_from_database(connection_string, table_names, custom_query=None, bind_vars=None):
    
    data = {}
    try:
        connection = cx_Oracle.connect(connection_string)
        cursor = connection.cursor()

        for table_name in table_names:
            if custom_query:
                query = custom_query
            else:
                # Fetch data for each table
                query = f"SELECT * FROM {table_name}"

            # Execute the query with bind variables if provided
            if bind_vars:
                cursor.execute(query, bind_vars)
            else:
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
    if search_query.strip() != "":
        # Filter the DataFrame based on the exact match for gene ID
        exact_match_df = df[df['GENE_ID'].str.lower() == search_query.lower()]

        # Filter the DataFrame based on partial match for sequence
        partial_match_df = df[df['DNA_SEQ'].str.contains(search_query, case=False, na=False)]

        # Concatenate the DataFrames to include both exact and partial matches
        filtered_df = pd.concat([exact_match_df, partial_match_df]).drop_duplicates()

    else:
        # If the search query is empty, return the original DataFrame
        filtered_df = df

    return filtered_df

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

def generate_fasta_from_db(connection_string, gene_name):
    
    # Fetch the DNA sequence for the specified gene_name from the database
    sequence_query = f"SELECT DNA_SEQ FROM SEQUENCES WHERE GENE_ID IN (SELECT GENE_ID FROM GENES WHERE GENE_NAME = '{gene_name}')"
    sequence_result = fetch_data_from_database(connection_string, ["SEQUENCES"], custom_query=sequence_query)

    if sequence_result and sequence_result["SEQUENCES"]:
        dna_seq = sequence_result["SEQUENCES"][0]["DNA_SEQ"]

        # Remove newline characters from the DNA sequence
        dna_seq = dna_seq.replace("\n", "").replace("\r", "")

        # Create a Biopython SeqRecord from the DNA sequence string
        seq_record = SeqRecord(Seq(dna_seq), id=gene_name, description="")

        # Create a string buffer to store the FASTA data
        fasta_string_buffer = StringIO()

        # Write the SeqRecord to the string buffer as a FASTA file
        write([seq_record], fasta_string_buffer, 'fasta')

        # Get the content of the string buffer as a string
        fasta_string = fasta_string_buffer.getvalue()

        return fasta_string

    else:
        st.warning(f"No DNA sequence found for gene: {gene_name}")
        return None



def generate_download_link(data, text):
    # Check if data is a string
    if isinstance(data, str):
        # Encode the content to base64
        base64_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')

        # Generate the download link
        href = f"data:text/plain;charset=utf-8;base64,{base64_data}"
        return f'<a href="{href}" download="{text}">{text}</a>'

    else:
        st.warning("Invalid data format for generating download link.")
        return None




def display_dna_section(index, current_page_df, connection_string):
    st.write(f"**{current_page_df.iloc[index]['GENE_NAME']}**")

    # Check if the 'IMAGE_FILE' column exists
    if 'IMAGE_FILE' in current_page_df.columns:
        image_url = current_page_df.iloc[index]['IMAGE_FILE']

        # Check if the image URL is null or empty
        if pd.isnull(image_url) or not image_url.strip():
            # If null or empty, use the default image URL
            image_url = "https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg"

        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                # Adjust the image size for the section
                st.image(image, caption=current_page_df.iloc[index]['GENE_NAME'], width=300, use_column_width=False)

                # Add a button to view full-size image
                button_key = f"View Full Size Image {index}"  # Unique key incorporating the index
                if st.button(button_key):
                    print(f"Button '{button_key}' clicked")
                    display_full_size_image(image)

                # Display nucleotide percentages graph
                display_nucleotide_graph(current_page_df.iloc[index]['DNA_SEQ'])

                # Inside display_dna_section function
                download_link_text = f"Download DNA Data (FASTA) - {current_page_df.iloc[index]['GENE_NAME']}"
                fasta_data = generate_fasta_from_db(connection_string, current_page_df.iloc[index]['GENE_NAME'])
                if fasta_data:
                    st.markdown(generate_download_link(fasta_data, download_link_text), unsafe_allow_html=True)

            else:
                st.write(f"Failed to retrieve image for {current_page_df.iloc[index]['GENE_NAME']}")

        except UnidentifiedImageError:
            st.image("https://hms.harvard.edu/sites/default/files/media/DNA-850.jpg",
                     caption=current_page_df.iloc[index]['GENE_NAME'], width=500, use_column_width=False)

            download_link_text = f"Download DNA Data (FASTA) - {current_page_df.iloc[index]['GENE_NAME']}"
            fasta_data = generate_fasta_from_db(connection_string, current_page_df.iloc[index]['GENE_NAME'])
            if fasta_data:
                st.markdown(generate_download_link(fasta_data, download_link_text), unsafe_allow_html=True)

    else:
        st.write(f"No image available for {current_page_df.iloc[index]['GENE_NAME']}")



def display_gallery(connection_string):
    # Fetching data from the database
    table_names = ["GENES", "SEQUENCES", "IMAGES"]
    data = fetch_data_from_database(connection_string, table_names)

    # Check if data retrieval was successful for all tables
    for table_name in table_names:
        if data.get(table_name) is None:
            st.error(f"Error fetching data from the {table_name} table.")
            return

    # Merge data
    gallery_data = merge_data(data["GENES"], data["IMAGES"], data["SEQUENCES"])

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
    page_size = 9
    total_pages = (len(sorted_df) - 1) // page_size + 1
    page_number = st.number_input("Enter page number:", min_value=1, max_value=total_pages, value=1)
    start_index = (page_number - 1) * page_size
    end_index = min(start_index + page_size, len(sorted_df))

    # Display the sorted and filtered DNA entries for the current page
    current_page_df = sorted_df[start_index:end_index]

    # Check if there are more pages
    if total_pages > 1 and end_index >= len(sorted_df):
        st.warning("No matching or sorted DNA entries found on this page.")

    if not current_page_df.empty:
        # Define the number of columns and rows in the grid
        num_columns = 3
        num_rows = len(current_page_df) // num_columns + (len(current_page_df) % num_columns > 0)

        # Use Streamlit's columns layout manager for grid view
        cols = st.columns(num_columns)

    # Inside display_gallery function
    for row_index in range(num_rows):
        st.write(f"--- DNA Section {row_index + 1} ---")
        for col_index in range(num_columns):
            index = row_index * num_columns + col_index
            if index < len(current_page_df):
                # Display DNA images and names in a section
                display_dna_section(index, current_page_df, connection_string)  # Pass connection_string as an argument

        # Pagination information
        st.write(f"Page {page_number}/{total_pages}")

    else:
        st.warning("No matching or sorted DNA entries found on this page.")

def display_nucleotide_graph(sequence):
    st.write("**Nucleotide Percentages:**")

    if not sequence:
        st.warning("No DNA sequence available.")
        return

    # Clean the sequence by removing non-nucleotide characters
    clean_sequence = ''.join([base for base in sequence.upper() if base in {'A', 'T', 'C', 'G'}])

    # Check if the cleaned sequence is empty
    if not clean_sequence:
        st.warning("No valid nucleotides found in the DNA sequence.")
        return

    # Count nucleotide occurrences
    count_A = clean_sequence.count('A')
    count_T = clean_sequence.count('T')
    count_C = clean_sequence.count('C')
    count_G = clean_sequence.count('G')

    total_nucleotides = len(clean_sequence)

    # Calculate percentages
    percentage_A = (count_A / total_nucleotides) * 100
    percentage_T = (count_T / total_nucleotides) * 100
    percentage_C = (count_C / total_nucleotides) * 100
    percentage_G = (count_G / total_nucleotides) * 100

    st.bar_chart({
        'A': percentage_A,
        'T': percentage_T,
        'C': percentage_C,
        'G': percentage_G
    })

def display_full_size_image(image):
    st.image(image, caption="Full Size Image", use_column_width=True)

if __name__ == '__main__':
    # Replace "your_connection_string" with your actual Oracle database connection string
    connection_string = get_oracle_connection_string()
    
    # Set page configuration
    set_page_configuration()

    # Display the gallery
    display_gallery(connection_string)
