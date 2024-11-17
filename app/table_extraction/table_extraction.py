import cv2
import pytesseract
import pdfplumber
import pandas as pd
import streamlit as st
import numpy as np

# Updated extract_table function
def extract_table(file, file_type):
    if file_type in ["png", "jpg", "jpeg"]:
        return extract_table_from_image(file)
    else:
        st.warning(f"Unsupported file type '{file_type}' for this demo.")
        return pd.DataFrame()

    
def extract_table_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_table():
                tables.append(page.extract_table())
    # Convert tables to DataFrame
    if tables:
        df = pd.DataFrame(tables[0][1:], columns=tables[0][0])  # Use the first table
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no tables found
    
def extract_table_from_image(image_file):
    # Read the uploaded file as bytes and decode it
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Decode to an image array
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Binarize the image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # OCR for text extraction
    ocr_data = pytesseract.image_to_string(binary, config="--psm 6")  # Assume a uniform table
    rows = ocr_data.split("\n")
    
    # Split rows into columns
    table_data = [row.split() for row in rows if row.strip()]  # Customize split logic based on table structure
    
    # Convert to DataFrame
    df = pd.DataFrame(table_data)
    return df

def extract_table_from_excel(excel_file):
    # Read the first sheet
    df = pd.read_excel(excel_file)
    return df
