import os

class SimplePDFBuilder:
    """
    Pure Python PDF 1.4 Document Generator with zero external dependencies.
    Supports multi-page layout, text wrapping, title headers, tables, and page margins.
    """
    def __init__(self, filename, page_width=595, page_height=842): # A4 portrait
        self.filename = filename
        self.page_width = page_width
        self.page_height = page_height
        self.pages = [] # List of stream content bytes
        self.current_stream = []
        self.cursor_y = page_height - 50
        self.margin_left = 40
        self.margin_right = page_width - 40
        self.line_height = 14
        self.font_size = 10
        self.current_font = "Helvetica"

    def new_page(self):
        if self.current_stream:
            self.pages.append(b"\n".join(self.current_stream))
            self.current_stream = []
        self.cursor_y = self.page_height - 50

    def add_title(self, text):
        if self.cursor_y < 80:
            self.new_page()
        safe_text = self._escape_text(text)
        cmd = f"BT /F2 18 Tf 1 0 0 1 {self.margin_left} {self.cursor_y} Tm ({safe_text}) Tj ET".encode('latin1', 'replace')
        self.current_stream.append(cmd)
        self.cursor_y -= 26

    def add_subtitle(self, text):
        if self.cursor_y < 60:
            self.new_page()
        safe_text = self._escape_text(text)
        cmd = f"BT /F2 13 Tf 1 0 0 1 {self.margin_left} {self.cursor_y} Tm ({safe_text}) Tj ET".encode('latin1', 'replace')
        self.current_stream.append(cmd)
        self.cursor_y -= 20

    def add_heading(self, text):
        if self.cursor_y < 60:
            self.new_page()
        self.cursor_y -= 8
        safe_text = self._escape_text(text)
        cmd = f"BT /F2 11 Tf 1 0 0 1 {self.margin_left} {self.cursor_y} Tm ({safe_text}) Tj ET".encode('latin1', 'replace')
        self.current_stream.append(cmd)
        self.cursor_y -= 16

    def add_paragraph(self, text):
        lines = self._wrap_text(text, max_chars=85)
        for line in lines:
            if self.cursor_y < 50:
                self.new_page()
            safe_text = self._escape_text(line)
            cmd = f"BT /F1 9.5 Tf 1 0 0 1 {self.margin_left} {self.cursor_y} Tm ({safe_text}) Tj ET".encode('latin1', 'replace')
            self.current_stream.append(cmd)
            self.cursor_y -= 13
        self.cursor_y -= 4

    def add_bullet(self, text):
        lines = self._wrap_text(text, max_chars=80)
        first = True
        for line in lines:
            if self.cursor_y < 50:
                self.new_page()
            prefix = "- " if first else "  "
            safe_text = self._escape_text(prefix + line)
            cmd = f"BT /F1 9.5 Tf 1 0 0 1 {self.margin_left + 10} {self.cursor_y} Tm ({safe_text}) Tj ET".encode('latin1', 'replace')
            self.current_stream.append(cmd)
            self.cursor_y -= 13
            first = False
        self.cursor_y -= 2

    def add_table_row(self, col1, col2, col1_w=150, col2_w=360):
        lines1 = self._wrap_text(col1, max_chars=int(col1_w / 6.5))
        lines2 = self._wrap_text(col2, max_chars=int(col2_w / 6.5))
        max_lines = max(len(lines1), len(lines2))
        
        row_height = max_lines * 13 + 6
        if self.cursor_y - row_height < 50:
            self.new_page()
            
        start_y = self.cursor_y
        # Draw background rect
        rect_cmd = f"0.96 0.97 0.98 rg {self.margin_left} {start_y - row_height} {col1_w + col2_w} {row_height} re f 0 g".encode('latin1')
        self.current_stream.append(rect_cmd)
        
        for i in range(max_lines):
            t1 = lines1[i] if i < len(lines1) else ""
            t2 = lines2[i] if i < len(lines2) else ""
            y_pos = start_y - (i * 13) - 12
            
            if t1:
                st1 = self._escape_text(t1)
                cmd1 = f"BT /F2 9 Tf 1 0 0 1 {self.margin_left + 5} {y_pos} Tm ({st1}) Tj ET".encode('latin1', 'replace')
                self.current_stream.append(cmd1)
            if t2:
                st2 = self._escape_text(t2)
                cmd2 = f"BT /F1 9 Tf 1 0 0 1 {self.margin_left + col1_w + 5} {y_pos} Tm ({st2}) Tj ET".encode('latin1', 'replace')
                self.current_stream.append(cmd2)
                
        self.cursor_y -= (row_height + 4)

    def save(self):
        if self.current_stream:
            self.pages.append(b"\n".join(self.current_stream))
            
        num_pages = len(self.pages)
        objects = []
        
        # 1: Catalog
        objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        
        # 2: Pages tree
        page_refs = " ".join([f"{3 + i*3} 0 R" for i in range(num_pages)])
        objects.append(f"2 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {num_pages} >>\nendobj\n".encode('latin1'))
        
        # Fonts
        font_helv = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        font_helv_bold = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
        
        obj_id = 3
        for i, page_bytes in enumerate(self.pages):
            page_obj_id = obj_id
            content_obj_id = obj_id + 1
            font_obj_id = obj_id + 2
            
            # Page obj
            objects.append(f"{page_obj_id} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.page_width} {self.page_height}] /Resources << /Font << /F1 {font_obj_id} 0 R /F2 {font_obj_id+1} 0 R >> >> /Contents {content_obj_id} 0 R >>\nendobj\n".encode('latin1'))
            
            # Stream obj
            stream_obj = f"{content_obj_id} 0 obj\n<< /Length {len(page_bytes)} >>\nstream\n".encode('latin1') + page_bytes + b"\nendstream\nendobj\n"
            objects.append(stream_obj)
            
            # Fonts
            objects.append(f"{font_obj_id} 0 obj\n{font_helv.decode('latin1')}\nendobj\n".encode('latin1'))
            objects.append(f"{font_obj_id+1} 0 obj\n{font_helv_bold.decode('latin1')}\nendobj\n".encode('latin1'))
            
            obj_id += 4

        # Assemble PDF file
        pdf_data = b"%PDF-1.4\n"
        offsets = []
        for obj in objects:
            offsets.append(len(pdf_data))
            pdf_data += obj
            
        xref_offset = len(pdf_data)
        pdf_data += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode('latin1')
        for off in offsets:
            pdf_data += f"{off:010d} 00000 n \n".encode('latin1')
            
        pdf_data += f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('latin1')
        
        with open(self.filename, 'wb') as f:
            f.write(pdf_data)
        print(f"Generated PDF: {self.filename} ({len(pdf_data)} bytes, {num_pages} pages)")

    def _escape_text(self, text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)').replace('₹', 'INR ')

    def _wrap_text(self, text, max_chars=80):
        words = text.split(' ')
        lines = []
        current_line = []
        current_len = 0
        for w in words:
            if current_len + len(w) + 1 > max_chars:
                lines.append(" ".join(current_line))
                current_line = [w]
                current_len = len(w)
            else:
                current_line.append(w)
                current_len += len(w) + 1
        if current_line:
            lines.append(" ".join(current_line))
        return lines if lines else [""]
