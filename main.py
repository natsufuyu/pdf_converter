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
    """Save extracted text as a CSV file"""
    df = pd.DataFrame({"Extracted Data": [data]})
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

st.title("PDF Table Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", extracted_text, height=300)

    # Convert to CSV
    csv_file = save_to_csv(extracted_text)
    st.download_button(
        label="Download as CSV",
        data=csv_file,
        file_name="extracted_data.csv",
        mime="text/csv",
    )
