import streamlit as st
import camelot
import pandas as pd
import os

def pdf_to_excel(pdf_file, output_filename):
    tables = camelot.read_pdf(pdf_file, pages='all', flavor='stream')
    if tables.n > 0:
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                table.df.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)
        st.success(f"Conversion successful! Excel file saved as {output_filename}")
        with open(output_filename, "rb") as f:
            st.download_button(
                label="Download Excel file",
                data=f,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("No tables found in the PDF.")

st.title("PDF to Excel Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file is not None:
    filename = st.text_input("Enter output file name (without extension)", "output")
    if st.button("Convert to Excel"):
        output_filename = f"{filename}.xlsx"
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        pdf_to_excel("temp.pdf", output_filename)
        os.remove("temp.pdf")
