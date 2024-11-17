import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

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
        default_index=1,  # Default to "📂 Upload & Extract"
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

# Function: Upload and Extract Table
def upload_and_extract_table():
    st.header("📂 Upload and Extract Table")
    
    # File uploader
    file = st.file_uploader("Upload a PDF, Image, or Excel File", type=["pdf", "png", "jpg", "jpeg", "xlsx"])
    
    if file:
        # Display success message
        st.success("File uploaded successfully!")
        
        # Simulated table extraction function
        table = extract_table(file)
        
        if not table.empty:
            # Display the extracted table
            st.write(table)
            
            # Allow user to download the table as CSV
            st.download_button("Download as CSV", table.to_csv(index=False), "table.csv")
            
            # Store the table in session state for further processing (e.g., summarization, chatbot)
            st.session_state["table"] = table
        else:
            st.warning("No tables found in the uploaded document. Please try a different file.")

# Simulated Extract Table Function (Replace with Actual Implementation)
def extract_table(file):
    # Simulated data extraction for demonstration purposes
    data = {
        "Item": ["Item A", "Item B", "Item C"],
        "Quantity": [10, 5, 7],
        "Price": [100, 200, 150],
        "Total": [1000, 1000, 1050],
    }
    return pd.DataFrame(data)

# Page Content Based on Selected Menu
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
        # Simulated chatbot response (Replace with actual chatbot logic)
        st.write(f"🤖 Bot: I'm here to help with your data questions!")

# Footer
st.markdown("---")
st.markdown("**Developed by TableSnap** - Powered by Streamlit 🚀")
