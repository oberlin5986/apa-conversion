from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH # Add this import
import io

def convert_docx_to_markdown(docx_file):
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        
        # --- NEW: ALIGNMENT DETECTION ---
        try:
            if para.alignment == WD_ALIGN_PARAGRAPH.CENTER:
                para_text += "[CENTERED] "
            elif para.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
                para_text += "[RIGHT ALIGNED] "
            # Left is the default, so we usually don't need a tag for it
        except Exception:
            pass

        # --- HANGING INDENT CHECK ---
        try:
            if para.paragraph_format and para.paragraph_format.first_line_indent:
                if para.paragraph_format.first_line_indent.twips < 0:
                    para_text += "[HANGING INDENT] "
        except Exception:
            pass

        # --- PROCESS TEXT RUNS ---
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
