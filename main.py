import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import io

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF using PyMuPDF (fitz)"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def save_to_csv(data):
    """Save extracted text as a CSV file (in BytesIO format)"""
    df = pd.DataFrame({"Extracted Data": [data]})
    output = io.BytesIO()  # Convert to BytesIO instead of StringIO
    df.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)  # Move cursor to the beginning
    return output

st.title("Welcome to Wei Jit's PDF Table Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", extracted_text, height=300)

    # Convert to CSV (BytesIO)
    csv_file = save_to_csv(extracted_text)

    # Fix: Use BytesIO format
    st.download_button(
        label="Download as CSV",
        data=csv_file.getvalue(),  # Convert BytesIO to binary data
        file_name="extracted_data.csv",
        mime="text/csv",
    )
