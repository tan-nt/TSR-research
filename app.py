import streamlit as st
import pandas as pd
import json
from PIL import Image
from transformers import pipeline

# App Title and Header
st.set_page_config(page_title="TableSnap", layout="wide", page_icon="🧾")
st.title("🧾 TableSnap")
st.markdown("**Effortlessly extract, organize, and analyze tables from invoices, receipts, and more.**")

# Sidebar for Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to", ["Home", "Upload Document", "Extract Table", "Summarization", "Chatbot"]
)

# Function to Simulate Table Extraction
def extract_table(file):
    # Simulate table extraction for demonstration
    data = {
        "Item": ["Item A", "Item B", "Item C"],
        "Quantity": [10, 5, 7],
        "Price": [100, 200, 150],
        "Total": [1000, 1000, 1050],
    }
    return pd.DataFrame(data)

# Home Page
if menu == "Home":
    st.header("Welcome to TableSnap!")
    st.image("https://source.unsplash.com/featured/?data", use_column_width=True)
    st.markdown("""
        - 📂 **Upload and Extract**: Process tables from PDFs, images, or Excel files.
        - 📊 **Summarization**: Generate insights like totals, trends, and key highlights.
        - 🤖 **AI Chatbot**: Ask questions about your data and get instant answers.
        - 🌐 **Export**: Save data in CSV, Excel, or JSON formats.
    """)
    st.markdown("**Get started by uploading a document in the sidebar.**")

# Upload Document Page
elif menu == "Upload Document":
    st.header("📂 Upload Your Document")
    file = st.file_uploader("Upload a PDF, Image, or Excel File", type=["pdf", "png", "jpg", "jpeg", "xlsx"])
    if file:
        st.success("File uploaded successfully!")
        st.session_state["file"] = file
        st.markdown("Go to the **Extract Table** tab to process your document.")

# Extract Table Page
elif menu == "Extract Table":
    st.header("📊 Extracted Table")
    if "file" in st.session_state:
        st.write("Processing your file...")
        table = extract_table(st.session_state["file"])
        st.write(table)
        st.session_state["table"] = table
        st.markdown("**Summary Options**")
        st.download_button("Download as CSV", table.to_csv(index=False), "table.csv")
    else:
        st.warning("Please upload a file first.")

# Summarization Page
elif menu == "Summarization":
    st.header("📈 Table Summarization")
    if "table" in st.session_state:
        st.markdown("**Extracted Summary**")
        table = st.session_state["table"]
        total = table["Total"].sum()
        st.metric("Total Amount", f"{total} VND")
    else:
        st.warning("Please extract a table first.")

# Chatbot Page
elif menu == "Chatbot":
    st.header("🤖 AI Chatbot")
    if "table" in st.session_state:
        st.markdown("**Ask me anything about your data!**")
        query = st.text_input("Type your question:")
        if query:
            # Simulated chatbot response
            chatbot_response = f"I'm sorry, I can't fully understand your data yet. Try asking simpler questions!"
            st.write(f"**Bot:** {chatbot_response}")
    else:
        st.warning("Please extract a table first.")

# Footer
st.markdown("---")
st.markdown("**Developed by [TableSnap](https://github.com/your-repo)** - Powered by Streamlit 🚀")
