import sys
import os

def convert_to_pdf():
    docx_file = "AI_Face_Recognition_Attendance_System_Report.docx"
    pdf_file = "AI_Face_Recognition_Attendance_System_Report.pdf"
    
    print(f"Attempting to convert {docx_file} to {pdf_file}...")
    
    try:
        from docx2pdf import convert
        convert(docx_file, pdf_file)
        print("Success! PDF created via docx2pdf (Microsoft Word Automation).")
        return True
    except Exception as e:
        print(f"docx2pdf conversion failed: {e}")
        print("This typically happens if Microsoft Word is not installed or not activated on this machine.")
        return False

if __name__ == '__main__':
    convert_to_pdf()
