import streamlit as st
import pandas as pd
import camelot
import io

def extract_tables_from_pdf(pdf_file):
    """Extract tables from PDF using Camelot."""
    tables = camelot.read_pdf(pdf_file, pages="all", flavor="stream")
    return tables

def save_to_csv(data):
    """Save extracted table data to CSV in BytesIO format."""
    output = io.BytesIO()
    data.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)  # Move cursor to the beginning
    return output

st.title("Welcome to Wei Jit's PDF Table Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    # Extract tables using Camelot
    tables = extract_tables_from_pdf(uploaded_file)

    if tables:
        # If tables are found, display and allow for CSV download
        st.write(f"{len(tables)} tables found.")
        
        for i, table in enumerate(tables, 1):
            st.write(f"Table {i}")
            st.write(table.df)  # Display the table as a dataframe
            
            # Convert the table to CSV (BytesIO)
            csv_file = save_to_csv(table.df)
            
            st.download_button(
                label=f"Download Table {i} as CSV",
                data=csv_file.getvalue(),
                file_name=f"table_{i}.csv",
                mime="text/csv",
            )
    else:
        st.warning("No tables found in the PDF.")
