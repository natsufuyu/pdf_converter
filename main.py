import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

def extract_table_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                tables.append(pd.DataFrame(table))  # Convert table to DataFrame
    return tables

def convert_df_to_excel(tables):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for i, table in enumerate(tables):
            table.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False, header=False)
    output.seek(0)  # Reset pointer to start of the file
    return output

st.title("PDF Table Extractor & Excel Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    
    # Extract tables from PDF
    extracted_tables = extract_table_from_pdf(uploaded_file)

    if extracted_tables:
        excel_data = convert_df_to_excel(extracted_tables)
        excel_filename = uploaded_file.name.replace(".pdf", ".xlsx")
        
        st.download_button(
            label="Download Excel File",
            data=excel_data,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.success("Conversion successful! Click above to download.")
    else:
        st.error("No tables found in the PDF.")
