import streamlit as st
from docx import Document
import io

def convert_docx_to_markdown(docx_file):
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        try:
            # Check for hanging indent
            if para.paragraph_format and para.paragraph_format.first_line_indent:
                if para.paragraph_format.first_line_indent.twips < 0:
                    para_text += "[HANGING INDENT] "
        except Exception:
            pass

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
st.markdown("""
This tool prepares your paper for the **APA Bot**. 
1. Upload your Word document.
2. Download the 'AI-Ready' file.
3. Upload that file directly into the APA Bot.
""")

# Setup Sidebar or top-level Reset
if st.button("Reset / Clear File"):
    st.rerun()

uploaded_file = st.file_uploader("Upload your .docx paper", type="docx")

if uploaded_file:
    try:
        file_bytes = io.BytesIO(uploaded_file.getvalue())
        md_output = convert_docx_to_markdown(file_bytes)
        
        st.divider()
        
        # Action Buttons at the Top
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.download_button(
                label="📥 Download AI-Ready File",
                data=md_output,
                file_name="UPLOAD_TO_BOT.md",
                mime="text/markdown",
                help="Download this file and upload it to your APA Bot."
            )
        
        with col2:
            st.success("Conversion Successful!")

        # Preview area
        with st.expander("Preview Formatted Text (Optional)"):
            st.text_area("Markdown Preview", value=md_output, height=300)
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")
