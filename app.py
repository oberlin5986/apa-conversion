import streamlit as st
from docx import Document
import io

def convert_docx_to_markdown(docx_file):
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        # Check for paragraph-level styling (like Headings)
        if para.style.name.startswith('Heading'):
            level = para.style.name.split()[-1]
            if level.isdigit():
                para_text += "#" * int(level) + " "
        
        # Look at each "Run" (chunk of text with same formatting)
        for run in para.runs:
            text = run.text
            if not text.strip(): # Don't wrap empty spaces
                para_text += text
                continue
            
            # Apply Markdown tags based on formatting
            if run.bold:
                text = f"**{text}**"
            if run.italic:
                text = f"_{text}_"
            
            para_text += text
        
        full_text.append(para_text)
    
    return "\n\n".join(full_text)

st.set_page_config(page_title="APA Pre-Processor", page_icon="📝")

st.title("📝 APA Formatting Pre-Processor")
st.info("This tool prepares your paper for AI review by preserving italics and headings.")

uploaded_file = st.file_uploader("Upload your .docx paper", type="docx")

if uploaded_file:
    # Read the file
    md_output = convert_docx_to_markdown(io.BytesIO(uploaded_file.read()))
    
    st.subheader("Formatted Text")
    st.caption("Copy the text below and paste it into your AI bot:")
    st.text_area("Markdown Output", value=md_output, height=400)
    
    st.download_button("Download Markdown", md_output, file_name="student_paper.md")
