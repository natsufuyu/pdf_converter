import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import io

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF using PyMuPDF (fitz)"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def parse_table_from_text(text):
    """Attempt to parse table-like text into structured data."""
    lines = text.split('\n')
    table_data = []

    for line in lines:
        # Assuming columns are separated by spaces or tabs; adjust the split as needed
        row = line.split()
        if len(row) > 1:  # If row has more than one column, consider it part of the table
            table_data.append(row)
    
    # Debug: Check the structure of table_data
    if table_data:
        print("Table Data (first 5 rows):", table_data[:5])  # Show the first 5 rows for debugging
        
        # Ensuring all rows have the same number of columns as the header
        num_columns = len(table_data[0])  # Get the number of columns from the first row
        for i, row in enumerate(table_data[1:], start=1):
            # Pad shorter rows with empty values or truncate longer rows
            if len(row) < num_columns:
                row.extend([""] * (num_columns - len(row)))  # Extend row with empty strings
            elif len(row) > num_columns:
                row = row[:num_columns]  # Truncate extra columns
            table_data[i] = row  # Update the row with corrected number of columns
        
        # Convert list of rows into DataFrame
        df = pd.DataFrame(table_data[1:], columns=table_data[0])
    else:
        df = pd.DataFrame()  # If no data found, return empty DataFrame
    return df

def save_to_csv(data):
    """Save DataFrame to CSV file in BytesIO format."""
    output = io.BytesIO()
    data.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)  # Move cursor to the beginning
    return output

st.title("Welcome to Wei Jit's PDF Table Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", extracted_text, height=300)

    # Try to parse table from the extracted text
    df = parse_table_from_text(extracted_text)

    if not df.empty:
        st.write("Extracted Table", df)  # Display the table
        # Save to CSV (BytesIO)
        csv_file = save_to_csv(df)

        st.download_button(
            label="Download as CSV",
            data=csv_file.getvalue(),
            file_name="extracted_table.csv",
            mime="text/csv",
        )
    else:
        st.warning("No table-like structure found in the extracted text.")
