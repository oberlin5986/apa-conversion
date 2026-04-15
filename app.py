import streamlit as st
from docx import Document
import io

def convert_docx_to_markdown(docx_file):
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        
        # Defensive check for styles
        if para.style and hasattr(para.style, 'name'):
            style_name = para.style.name
            if style_name.startswith('Heading'):
                level = style_name.split()[-1]
                if level.isdigit():
                    para_text += "#" * int(level) + " "
            
            # Special APA check: If the paragraph is a "Reference" style, 
            # we can tag it so the LLM knows to check for indents.
            if "Reference" in style_name:
                para_text += "[REF] "

        # Process the text chunks (Runs)
        for run in para.runs:
            text = run.text
            if not text:
                continue
            
            # Apply Markdown
            if run.italic:
                text = f"_{text}_"
            if run.bold:
                text = f"**{text}**"
            
            para_text += text
        
        full_text.append(para_text)
    
    return "\n\n".join(full_text)

st.set_page_config(page_title="APA Pre-Processor", page_icon="📝")

st.title("📝 APA Formatting Pre-Processor")
st.info("Upload your paper to convert visual formatting (italics/headings) into AI-readable text.")

uploaded_file = st.file_uploader("Upload your .docx paper", type="docx")

if uploaded_file:
    try:
        # We use getvalue() here as it's more stable for repeated reads in Streamlit
        file_bytes = io.BytesIO(uploaded_file.getvalue())
        md_output = convert_docx_to_markdown(file_bytes)
        
        st.subheader("Formatted Text")
        st.caption("Copy this into your AI bot:")
        st.text_area("Markdown Output", value=md_output, height=450)
        
        st.download_button("Download Markdown", md_output, file_name="apa_prepped_paper.md")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Try saving your Word document as a 'Strict Open XML Document (.docx)' and uploading again.")
