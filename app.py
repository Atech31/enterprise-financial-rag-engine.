import streamlit as st
import os
from io import BytesIO
from PyPDF2 import PdfReader
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Financial RAG & Earnings Intelligence",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Enterprise Financial Document & Earnings Intelligence Platform")
st.markdown("Upload financial filings, annual reports, or transcripts for instant lightweight text search, metric parsing, and interactive Plotly analytics.")

# Sidebar for Document Ingestion
st.sidebar.header("📁 Document Ingestion")
uploaded_files = st.sidebar.file_uploader(
    "Upload Financial PDFs (10-K, Reports, Transcripts)",
    type=["pdf"],
    accept_multiple_files=True
)

# Parse PDFs into session state text storage safely
if uploaded_files:
    if "doc_cache" not in st.session_state:
        st.session_state.doc_cache = {}
    
    for file in uploaded_files:
        if file.name not in st.session_state.doc_cache:
            try:
                reader = PdfReader(file)
                text_data = []
                for idx, page in enumerate(reader.pages):
                    t = page.extract_text()
                    if t:
                        text_data.append({"page": idx + 1, "text": t})
                st.session_state.doc_cache[file.name] = text_data
            except Exception as e:
                st.sidebar.error(f"Error reading {file.name}: {e}")

# Main Application Tabs
tab1, tab2, tab3 = st.tabs([
    "🧠 Lightweight PDF Text Search & Parsing", 
    "🎨 Interactive Financial Charts (Plotly)", 
    "📊 Financial Metrics & Risk Summary"
])

# TAB 1: Lightweight PDF Text Search & Parsing
with tab1:
    st.subheader("🧠 Lightweight Document Search & Keyword Extraction")
    st.markdown("Instantly search keywords, figures, or clauses across uploaded financial documents without heavy vector database overhead.")
    
    if not uploaded_files:
        st.info("👈 Please upload one or more financial PDFs in the sidebar to begin searching.")
    else:
        search_query = st.text_input("Enter search keyword or topic (e.g., 'revenue', 'operating margin', 'risk', 'cash flow'):")
        
        if search_query:
            st.markdown(f"### Search Results for: *'{search_query}'*")
            total_matches = 0
            
            for file_name, pages in st.session_state.doc_cache.items():
                file_matches = 0
                st.markdown(f"**📄 Document: `{file_name}`**")
                
                for page_obj in pages:
                    page_num = page_obj["page"]
                    page_text = page_obj["text"]
                    
                    if search_query.lower() in page_text.lower():
                        file_matches += 1
                        total_matches += 1
                        
                        # Extract context snippet around keyword
                        idx_pos = page_text.lower().find(search_query.lower())
                        start_idx = max(0, idx_pos - 150)
                        end_idx = min(len(page_text), idx_pos + 250)
                        snippet = page_text[start_idx:end_idx].replace("\n", " ")
                        
                        with st.expander(f"Match found on Page {page_num}"):
                            st.markdown(f"> *...{snippet}...*")
                
                if file_matches == 0:
                    st.caption(f"No direct matches found in {file_name}.")
            
            if total_matches == 0:
                st.warning("No matches found across any uploaded files. Try broader keywords.")

# TAB 2: Interactive Financial Charts with Plotly
with tab2:
    st.subheader("🎨 Dynamic Financial Performance Analytics")
    st.markdown("Interactive multi-metric visualization comparing revenue growth, operating margins, and free cash flow trends.")
    
    # Financial dataset for visualization
    financial_data = pd.DataFrame({
        "Fiscal Year": ["FY 2021", "FY 2022", "FY 2023", "FY 2024", "FY 2025"],
        "Revenue ($B)": [10.2, 11.8, 13.5, 14.2, 16.8],
        "Operating Income ($B)": [2.1, 2.5, 2.8, 3.1, 3.9],
        "Free Cash Flow ($B)": [1.4, 1.6, 1.7, 1.8, 2.3],
        "Operating Margin (%)": [20.6, 21.2, 20.7, 21.8, 23.2]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_choice = st.selectbox("Select Metric for Bar Chart:", ["Revenue ($B)", "Operating Income ($B)", "Free Cash Flow ($B)"])
        fig_bar = px.bar(
            financial_data, 
            x="Fiscal Year", 
            y=metric_choice, 
            title=f"Annual {metric_choice} Trajectory",
            color=metric_choice,
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        fig_line = px.line(
            financial_data, 
            x="Fiscal Year", 
            y="Operating Margin (%)", 
            title="Operating Margin Expansion (%)",
            markers=True,
            template="plotly_dark"
        )
        fig_line.update_traces(line_color="#00CC96", line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)

# TAB 3: Metric Table & Risk Summary
with tab3:
    st.subheader("📊 Executive Financial Summary & Risk Audit")
    
    sample_metrics = pd.DataFrame({
        "Financial Metric": ["Total Revenue", "Operating Income", "Net Income", "Free Cash Flow", "Diluted EPS"],
        "FY 2024": ["$14.2B", "$3.1B", "$2.4B", "$1.8B", "$4.12"],
        "FY 2025": ["$16.8B", "$3.9B", "$3.0B", "$2.3B", "$5.15"],
        "YoY Growth": ["+18.3%", "+25.8%", "+25.0%", "+27.7%", "+25.0%"]
    })
    st.dataframe(sample_metrics, use_container_width=True)
    
    st.markdown("### ⚠️ Key Risk Factors Identified")
    st.warning("**Macroeconomic & Input Costs:** Supply chain volatility and inflationary pressures could impact future gross margins.")
    st.error("**Regulatory Compliance:** Changing international tax and data privacy regulations present ongoing operational exposure.")
