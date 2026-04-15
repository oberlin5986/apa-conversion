import streamlit as st
from docx import Document
import io

def convert_docx_to_markdown(docx_file):
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        
        # --- SAFE HANGING INDENT CHECK ---
        try:
            # Check if the paragraph format exists and has a negative first_line_indent
            if para.paragraph_format and para.paragraph_format.first_line_indent:
                if para.paragraph_format.first_line_indent.twips < 0:
                    para_text += "[HANGING INDENT] "
        except Exception:
            # If anything goes wrong (missing attributes, etc.), just keep going
            pass

        # --- PROCESS TEXT RUNS (Italics/Bold) ---
        for run in para.runs:
            text = run.text
            if not text: continue
            
            if run.italic:
                text = f"_{text}_"
            if run.bold:
                text = f"**{text}**"
            
            para_text += text
        
        full_text.append(para_text)
    
    return "\n\n".join(full_text)

# --- STREAMLIT UI ---
st.set_page_config(page_title="APA Pre-Processor", page_icon="📝")

st.title("📝 APA Formatting Pre-Processor")
st.markdown("This tool translates Word formatting into tags your AI bot can understand.")

uploaded_file = st.file_uploader("Upload your .docx paper", type="docx")

if uploaded_file:
    try:
        # Get the file bytes
        file_bytes = io.BytesIO(uploaded_file.getvalue())
        md_output = convert_docx_to_markdown(file_bytes)
        
        st.subheader("Formatted Text")
        st.text_area("Copy this for your AI Bot:", value=md_output, height=450)
        
        st.download_button("Download Markdown", md_output, file_name="apa_prepped.md")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
