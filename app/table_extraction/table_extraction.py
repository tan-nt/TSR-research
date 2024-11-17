import cv2
import pytesseract
import pdfplumber
import pandas as pd
import streamlit as st
from pytesseract import image_to_string
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
    

def extract_table_from_excel(excel_file):
    # Read the first sheet
    df = pd.read_excel(excel_file)
    return df


def detect_and_show_table(image_file):
    # Reset the file pointer to the beginning
    image_file.seek(0)
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Decode to an image array

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarize the image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Invert the binary image
    binary = 255 - binary

    # Detect horizontal and vertical lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)

    # Combine horizontal and vertical lines to detect table structure
    table_mask = cv2.add(horizontal_lines, vertical_lines)

    # Find contours to detect table regions
    contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes on the original image
    table_detected_image = image.copy()
    if contours:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(table_detected_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Convert the image with bounding boxes to RGB format for Streamlit
    table_detected_image_rgb = cv2.cvtColor(table_detected_image, cv2.COLOR_BGR2RGB)
    return table_detected_image_rgb, contours


def extract_table_from_image(image_file, contour):
    # Reset the file pointer to the beginning
    image_file.seek(0)
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Decode to an image array

    # Crop to the detected table region
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = image[y:y+h, x:x+w]

    # OCR for text extraction
    ocr_data = image_to_string(cropped_image, config="--psm 6")
    rows = ocr_data.split("\n")

    # Split rows into columns
    table_data = [row.split() for row in rows if row.strip()]

    # Convert to DataFrame
    df = pd.DataFrame(table_data)
    return df