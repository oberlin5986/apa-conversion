import streamlit as st
from markitdown import MarkItDown
import io

# Initialize the converter
md = MarkItDown()

st.set_page_config(page_title="APA Formatting Pre-Processor", page_icon="📝")

st.title("📝 APA Formatting Pre-Processor")
st.markdown("""
Upload your paper below. This tool converts your document into a format 
that preserves **italics** and **indents** so your AI bot can review it accurately.
""")

uploaded_file = st.file_uploader("Choose a Word (.docx) file", type="docx")

if uploaded_file is not None:
    with st.spinner("Processing formatting..."):
        # Convert the uploaded byte stream to Markdown
        # MarkItDown handles the bold/italic preservation automatically
        result = md.convert_stream(io.BytesIO(uploaded_file.getvalue()), extension=".docx")
        markdown_text = result.text_content

    st.success("Conversion Complete!")
    
    # Display the result in a text area for easy copying
    st.subheader("Formatted Text for your Bot:")
    st.text_area("Copy and paste this into your AI feedback tool:", 
                 value=markdown_text, height=400)
    
    # Optional: Download button
    st.download_button("Download as .md file", markdown_text, file_name="formatted_paper.md")
