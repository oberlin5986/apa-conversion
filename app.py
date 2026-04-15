def convert_docx_to_markdown(docx_file):
    doc = Document(docx_file)
    full_text = []
    
    for para in doc.paragraphs:
        para_text = ""
        
        # 1. CHECK FOR HANGING INDENT
        # We check if the first_line_indent is negative (the hallmark of a hanging indent)
        is_hanging = False
        if para.paragraph_format.first_line_indent is not None:
            if para.paragraph_format.first_line_indent < 0:
                is_hanging = True

        # 2. Add a visual marker for the LLM
        if is_hanging:
            para_text += "[HANGING INDENT] "
        
        # 3. Process formatting (Italics/Bold)
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
