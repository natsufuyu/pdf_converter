import streamlit as st
import pandas as pd
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO

# Set Tesseract path (if needed, update it to your Tesseract installation path)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_tables_from_image(image):
    """Detects and extracts tables from an image using OpenCV and Tesseract."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200)

    # Find contours for table detection
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    table_data = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 20:  # Filter out small boxes
            roi = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config="--psm 6")  # Page segmentation mode for tables
            table_data.append(text.strip())

    return table_data

def pdf_to_excel(pdf_file):
    """Converts PDF to images, extracts tables, and saves them in an Excel file."""
    images = convert_from_bytes(pdf_file.read())
    all_data = []

    for img in images:
        img_cv = np.array(img)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
        table_data = extract_tables_from_image(img_cv)
        all_data.append(table_data)

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(all_data).T  # Transpose to organize properly
    output = BytesIO()
    df.to_excel(output, index=False, header=False, engine="openpyxl")
    output.seek(0)
    return output

# Streamlit App
st.title("PDF Table Extractor & Converter")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    output_excel = pdf_to_excel(uploaded_file)
    st.success("Tables extracted successfully!")

    # Download button
    st.download_button(
        label="Download Excel file",
        data=output_excel,
        file_name="extracted_tables.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
