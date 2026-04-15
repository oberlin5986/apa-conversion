import streamlit as st
from docx import Document
import io

def convert_docx_to_markdown(docx_file):
    # Move imports inside to ensure stability
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        
        # 1. SAFE ALIGNMENT CHECK
        try:
            if para.alignment == WD_ALIGN_PARAGRAPH.CENTER:
                para_text += "[CENTERED] "
            elif para.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
                para_text += "[RIGHT ALIGNED] "
        except Exception:
            pass

        # 2. SAFE HANGING INDENT CHECK
        try:
            # We check if it exists before checking the value
            fmt = para.paragraph_format
            if fmt and fmt.first_line_indent and fmt.first_line_indent.twips < 0:
                para_text += "[HANGING INDENT] "
        except Exception:
            pass

        # 3. SAFE TEXT RUN PROCESSING
        try:
            for run in para.runs:
                text = run.text
                if not text: continue
                if run.italic:
                    text = f"_{text}_"
                if run.bold:
                    text = f"**{text}**"
                para_text += text
        except Exception:
            # If a run fails, just add the raw paragraph text as a backup
            para_text += para.text
        
        full_text.append(para_text)
    
    return "\n\n".join(full_text)

# --- STREAMLIT UI ---
st.set_page_config(page_title="APA Pre-Processor", page_icon="📝")

st.title("📝 APA Formatting Pre-Processor")
st.markdown("Use this to prepare your paper for the AI Bot.")

# Reset Button
if st.button("Reset / Clear File"):
    st.rerun()

uploaded_file = st.file_uploader("Upload your .docx paper", type="docx")

if uploaded_file:
    try:
        file_bytes = io.BytesIO(uploaded_file.getvalue())
        md_output = convert_docx_to_markdown(file_bytes)
        
        st.divider()
        
        # Action Buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button(
                label="📥 Download AI-Ready File",
                data=md_output,
                file_name="UPLOAD_TO_BOT.md",
                mime="text/markdown"
            )
        with col2:
            st.success("Conversion Ready!")

        with st.expander("View AI-Ready Text Preview"):
            st.text_area("Preview", value=md_output, height=300)
            
    except Exception as e:
        st.error(f"Error processing file: {e}")
