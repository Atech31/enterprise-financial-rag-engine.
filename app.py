import streamlit as st
import os
from io import BytesIO
from PyPDF2 import PdfReader
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Financial RAG & Earnings Intelligence",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Enterprise Financial Document RAG & Earnings Intelligence")
st.markdown("Upload 10-K filings, annual reports, or earnings transcripts to query financial metrics, analyze risk factors, and extract insights using semantic search.")

# Sidebar for Configuration & Upload
st.sidebar.header("📁 Document Ingestion")
uploaded_files = st.sidebar.file_uploader(
    "Upload Financial PDFs (10-K, Reports, Transcripts)",
    type=["pdf"],
    accept_multiple_files=True
)

# Main Dashboard Layout
tab1, tab2, tab3 = st.tabs(["💬 Semantic RAG Q&A", "📊 Metric Extraction", "⚠️ Risk Summary"])

with tab1:
    st.subheader("Semantic Financial Assistant")
    
    if not uploaded_files:
        st.info("👈 Please upload one or more financial PDF documents in the sidebar to begin querying.")
    else:
        st.success(f"{len(uploaded_files)} document(s) loaded successfully!")
        
        # User query input
        user_query = st.text_input("Ask a question about the financial documents (e.g., 'What was the Q4 operating margin and revenue growth?'):")
        
        if user_query:
            with st.spinner("Analyzing financial documents..."):
                # Simulated RAG response structure for initial setup
                st.markdown("### **Analysis & Insights:**")
                st.write(f"Based on the uploaded documents, regarding your query: *'{user_query}'*")
                
                # Expandable source attribution mock
                with st.expander("View Source Citations"):
                    st.write("• Document: `Annual_Report_FY2025.pdf` | Page 42 | Relevance Score: 94.2%")
                    st.write("• Extracted context snippet: *'Operating margins expanded by 180 basis points year-over-year driven by operational efficiencies...'*")

with tab2:
    st.subheader("Automated Financial Metric Extraction")
    st.markdown("Extract key balance sheet, income statement, and cash flow metrics automatically.")
    
    # Mock extracted financial table
    sample_metrics = pd.DataFrame({
        "Financial Metric": ["Total Revenue", "Operating Income", "Net Income", "Free Cash Flow", "EPS (Diluted)"],
        "FY 2024": ["$14.2B", "$3.1B", "$2.4B", "$1.8B", "$4.12"],
        "FY 2025": ["$16.8B", "$3.9B", "$3.0B", "$2.3B", "$5.15"],
        "YoY Growth": ["+18.3%", "+25.8%", "+25.0%", "+27.7%", "+25.0%"]
    })
    st.dataframe(sample_metrics, use_container_width=True)

with tab3:
    st.subheader("Executive Risk Factor Summary")
    st.markdown("AI-generated breakdown of key operational, market, and regulatory risks identified in Item 1A of filings.")
    
    st.warning("**Macroeconomic & Inflationary Pressures:** Supply chain volatility and rising input costs could impact gross margins if pricing power cannot be maintained.")
    st.error("**Regulatory & Compliance:** Changing data privacy regulations across international jurisdictions present ongoing legal and operational challenges.")
    st.info("**Technological Disruption:** Rapid advancements in AI require continued high capital expenditure in R&D to maintain competitive advantage.")
