import streamlit as st
from streamlit_option_menu import option_menu
import time
from app.table_extraction.table_extraction import extract_table
import os
from io import BytesIO

# App Title and Header
st.set_page_config(page_title="TableSnap", layout="wide", page_icon="🧾")
st.title("🧾 TableSnap")
st.markdown("**Effortlessly extract, organize, and analyze tables from invoices, receipts, and more.**")

# Sidebar for Navigation
st.sidebar.header("Navigation")
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "📂 Upload & Extract", "💬 Go Chat"],
        icons=["house", "file-earmark-arrow-up", "chat-dots"],
        menu_icon="cast",
        default_index=1,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )

# Update session state based on the selected menu option
if "page" not in st.session_state:
    st.session_state.page = "upload_extract"  # Default to "Upload & Extract" page

if selected == "🏠 Home":
    st.session_state.page = "home"
elif selected == "📂 Upload & Extract":
    st.session_state.page = "upload_extract"
elif selected == "💬 Go Chat":
    st.session_state.page = "chat"



def upload_and_extract_table():
    st.header("📂 Upload and Extract Table")
    
    file = st.file_uploader("Upload a PDF, Image, or Excel File", type=["pdf", "png", "jpg", "jpeg", "xlsx"])
    file_type = None 
    if not file:
        st.info("No file uploaded. Using the default image for table extraction.")
        default_file_path = os.path.join("assets", "04-phieu-xuat-kho-pdf.en.jpg")
        with open(default_file_path, "rb") as default_file:
            file_content = default_file.read()  
        file = BytesIO(file_content)  
        file_type = "jpg"  
    else:
        file_type = file.name.split(".")[-1].lower()

    st.success("File uploaded successfully!")
    
    if file_type in ["png", "jpg", "jpeg"]:
        st.image(file, caption="Uploaded Image", use_container_width=True)
    else:
        st.warning("Displaying images is supported only for PNG, JPG, and JPEG formats.")

    # Measure time for table extraction
    start_time = time.time()
    table = extract_table(file, file_type) 
    elapsed_time = time.time() - start_time
    st.info(f"⏱️ Table extraction completed in {elapsed_time:.2f} seconds.")
        
    if not table.empty:
        st.write(table)
        st.download_button("Download as CSV", table.to_csv(index=False), "table.csv")
        
        st.session_state["table"] = table
    else:
        st.warning("No tables found in the uploaded document. Please try a different file.")



if st.session_state.page == "home":
    st.title("Welcome to TableSnap! 🧾")
    st.markdown(
        """
        **TableSnap** is your all-in-one solution for extracting, summarizing, 
        and analyzing data from tables in invoices, receipts, and other documents.
        """
    )
    st.image("https://source.unsplash.com/featured/?data", use_column_width=True)

elif st.session_state.page == "upload_extract":
    upload_and_extract_table()

elif st.session_state.page == "chat":
    st.title("💬 Chat with AI")
    st.markdown("Ask me anything about your extracted data or tables!")
    user_input = st.text_input("Type your question:")
    if user_input:
        st.write(f"🤖 Bot: I'm here to help with your data questions!")

st.markdown("---")
st.markdown("**Developed by TableSnap** - Powered by Streamlit 🚀")
