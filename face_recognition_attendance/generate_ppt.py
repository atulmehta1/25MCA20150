import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    
    # Set to widescreen 16:9 aspect ratio
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    # Palette colors (Modern Dark Theme)
    BG_COLOR = RGBColor(9, 13, 22)        # Slate Dark #090d16
    CARD_COLOR = RGBColor(30, 41, 59)      # Slate Card #1e293b
    WHITE = RGBColor(248, 250, 252)        # Text Primary #f8fafc
    SLATE_LIGHT = RGBColor(148, 163, 184)  # Text Secondary #94a3b8
    INDIGO = RGBColor(99, 102, 241)        # Accent Indigo #6366f1
    EMERALD = RGBColor(16, 185, 129)       # Accent Emerald #10b981
    
    blank_layout = prs.slide_layouts[6] # Blank layout
    
    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_slide_header(slide, title_text):
        # Top title box
        title_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.4), Inches(11.83), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = 'Arial'
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = INDIGO
        
        # Sub title separator line or subtle glow
        # Let's add a decorative horizontal line
        line = slide.shapes.add_shape(
            1, # MSO_SHAPE.RECTANGLE
            Inches(0.75), Inches(1.2), Inches(11.83), Inches(0.04)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_COLOR
        line.line.fill.background() # borderless

    # ------------------ SLIDE 1: TITLE SLIDE ------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    
    # Large Decorative Rectangle (Left accent border)
    left_accent = slide1.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    left_accent.fill.solid()
    left_accent.fill.fore_color.rgb = INDIGO
    left_accent.line.fill.background()
    
    # Title & Subtitle in single text box
    title_box = slide1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10), Inches(3))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "FaceMark AI"
    p.font.name = 'Arial'
    p.font.size = Pt(64)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT
    
    p2 = tf.add_paragraph()
    p2.text = "Smart Face Recognition Attendance System"
    p2.font.name = 'Arial'
    p2.font.size = Pt(28)
    p2.font.color.rgb = INDIGO
    p2.space_before = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = "Automated • Touchless • Real-Time Web Solution"
    p3.font.name = 'Arial'
    p3.font.size = Pt(18)
    p3.font.color.rgb = SLATE_LIGHT
    p3.space_before = Pt(30)

    # ------------------ SLIDE 2: PROBLEM STATEMENT ------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_slide_header(slide2, "The Problem Statement")
    
    # Left column: Description
    desc_box = slide2.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(5.5), Inches(4.5))
    tf_desc = desc_box.text_frame
    tf_desc.word_wrap = True
    
    p_desc = tf_desc.paragraphs[0]
    p_desc.text = "Traditional attendance methods suffer from severe inefficiencies that disrupt class times and organizational workflows."
    p_desc.font.name = 'Arial'
    p_desc.font.size = Pt(20)
    p_desc.font.color.rgb = WHITE
    p_desc.space_after = Pt(20)
    
    # Right column: Highlighted cards for issues
    issues = [
        ("Time Consumption", "Manual registers and rolls calls consume 10-15 minutes of every lecture."),
        ("Buddy Punching", "Proxies allow students to check-in cards/registers for absent peers."),
        ("Data entry errors", "Manual transcription to excel sheets causes accuracy mistakes."),
        ("No instant updates", "Data is compiled monthly, leaving no room for live warnings or trends.")
    ]
    
    for idx, (title, desc) in enumerate(issues):
        x = Inches(6.8)
        y = Inches(1.8 + (idx * 1.25))
        
        # Draw background card shape
        card = slide2.shapes.add_shape(1, x, y, Inches(5.8), Inches(1.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_COLOR
        card.line.fill.background()
        
        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = Inches(0.2)
        tf_card.margin_top = Inches(0.1)
        
        pt = tf_card.paragraphs[0]
        pt.text = title
        pt.font.name = 'Arial'
        pt.font.size = Pt(16)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        
        pd = tf_card.add_paragraph()
        pd.text = desc
        pd.font.name = 'Arial'
        pd.font.size = Pt(12)
        pd.font.color.rgb = SLATE_LIGHT

    # ------------------ SLIDE 3: THE SOLUTION ------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_slide_header(slide3, "The Proposed Solution")
    
    # Three column layout of solution pillars
    pillars = [
        ("100% Touchless", "Fully automated face scanning requires zero physical contact, offering a hygienic and fast verification process at entrances."),
        ("Zero Proxies", "Since facial biometrics are unique and require physical presence, buddy punching/proxy check-ins are completely eliminated."),
        ("Real-time Analytics", "Web dashboard logs scans immediately. Admins view live presence, charts, receive toast notifications, and export Excel reports.")
    ]
    
    for idx, (title, desc) in enumerate(pillars):
        x = Inches(0.75 + (idx * 4.0))
        y = Inches(2.2)
        
        card = slide3.shapes.add_shape(1, x, y, Inches(3.7), Inches(4.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_COLOR
        card.line.fill.background()
        
        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = tf_card.margin_right = Inches(0.3)
        tf_card.margin_top = Inches(0.4)
        
        pt = tf_card.paragraphs[0]
        pt.text = title
        pt.font.name = 'Arial'
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = EMERALD
        pt.space_after = Pt(20)
        
        pd = tf_card.add_paragraph()
        pd.text = desc
        pd.font.name = 'Arial'
        pd.font.size = Pt(14)
        pd.font.color.rgb = WHITE
        pd.line_spacing = 1.3

    # ------------------ SLIDE 4: SYSTEM ARCHITECTURE ------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_slide_header(slide4, "System Architecture")
    
    # Text box detailing components
    arch_box = slide4.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.83), Inches(5.0))
    tf_arch = arch_box.text_frame
    tf_arch.word_wrap = True
    
    def add_bullet(tf, bold_prefix, text_content):
        p = tf.add_paragraph() if tf.text else tf.paragraphs[0]
        p.space_after = Pt(14)
        p.level = 0
        
        run_bold = p.add_run()
        run_bold.text = bold_prefix + ": "
        run_bold.font.bold = True
        run_bold.font.size = Pt(16)
        run_bold.font.color.rgb = INDIGO
        
        run_text = p.add_run()
        run_text.text = text_content
        run_text.font.size = Pt(16)
        run_text.font.color.rgb = WHITE
        
    add_bullet(tf_arch, "Webcam / Camera Feed", "Captures frame inputs at 30 FPS and sends them to the server generator context.")
    add_bullet(tf_arch, "FaceEngine pipeline", "Coordinates YuNet detector (for crop boundaries & 5 landmarks) and SFace recognizer (for feature embedding vector output).")
    add_bullet(tf_arch, "Biometric Cache Matcher", "Compares live vectors against in-memory signatures thread-safely using Cosine Similarity calculation.")
    add_bullet(tf_arch, "Database Integration", "Saves attendance status via SQLAlchemy ORM (MySQL/SQLite). Refreshes cache instantly upon new registrations.")
    add_bullet(tf_arch, "SSE Server Broadcast", "Uses Server-Sent Events to push attendance triggers dynamically to all open web browser dashboards.")

    # ------------------ SLIDE 5: TECHNICAL STACK ------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_slide_header(slide5, "Technical Stack Analysis")
    
    stack = [
        ("Python 3.14", "Core programming platform for heavy OpenCV calculations and threading."),
        ("Flask Core", "Serves web server endpoints, handles MJPEG streams, and manages SSE streams."),
        ("OpenCV DNN", "Loads pre-trained ONNX models natively without heavy C++ installation environments."),
        ("SQLAlchemy", "Database ORM with pymysql driver. SQLite fallback for zero-config local runs."),
        ("Pandas / openpyxl", "Structures attendance query outputs and generates auto-fit Excel sheets."),
        ("Chart.js", "Integrates dynamic weekly analytics line charts directly on the frontend dashboard.")
    ]
    
    for idx, (tech, usecase) in enumerate(stack):
        col = idx % 3
        row = idx // 3
        
        x = Inches(0.75 + (col * 4.0))
        y = Inches(2.0 + (row * 2.4))
        
        card = slide5.shapes.add_shape(1, x, y, Inches(3.7), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_COLOR
        card.line.fill.background()
        
        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = tf_card.margin_right = Inches(0.2)
        tf_card.margin_top = Inches(0.2)
        
        pt = tf_card.paragraphs[0]
        pt.text = tech
        pt.font.name = 'Arial'
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.space_after = Pt(10)
        
        pd = tf_card.add_paragraph()
        pd.text = usecase
        pd.font.name = 'Arial'
        pd.font.size = Pt(12)
        pd.font.color.rgb = SLATE_LIGHT

    # ------------------ SLIDE 6: FACE ENGINE ------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_slide_header(slide6, "AI Face Engine: YuNet & SFace")
    
    engine_box = slide6.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.83), Inches(5.0))
    tf_eng = engine_box.text_frame
    tf_eng.word_wrap = True
    
    add_bullet(tf_eng, "Modern ONNX Pipeline", "Replaces legacy dlib architectures. No visual studio compilation. Models download automatically on startup.")
    add_bullet(tf_eng, "YuNet Face Detector", "Detects face bounding boxes and 5 structural landmarks (Right Eye, Left Eye, Nose Tip, Right/Left Mouth Corners). Optimized for edge CPU speeds.")
    add_bullet(tf_eng, "SFace Recognition", "Uses landmarks to crop/align face, mapping visual cues to a 128-dimensional spherical float vector.")
    add_bullet(tf_eng, "Cosine Similarity Matching", "Computes the dot product of normalized embeddings. Values above threshold (0.60) trigger instant attendance marking.")

    # ------------------ SLIDE 7: DATABASE SCHEMA ------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_slide_header(slide7, "Database & Storage Design")
    
    db_box = slide7.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.83), Inches(5.0))
    tf_db = db_box.text_frame
    tf_db.word_wrap = True
    
    add_bullet(tf_db, "Student table", "Stores basic profiles: unique Student ID, Name, Email, and Department.")
    add_bullet(tf_db, "Face Embeddings table", "Saves face embeddings serialized to binary blobs (BLOB) for quick retrieval.")
    add_bullet(tf_db, "Attendance log table", "Stores check-in records containing foreign keys to Student ID and DateTime timestamps.")
    add_bullet(tf_db, "In-Memory Caching", "On startup, embeddings, names, and departments are loaded into RAM thread-safely. This reduces matching lookup times from seconds to milliseconds.")

    # ------------------ SLIDE 8: DYNAMIC DASHBOARD ------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_slide_header(slide8, "Interactive Admin Dashboard")
    
    dash_box = slide8.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.83), Inches(5.0))
    tf_dash = dash_box.text_frame
    tf_dash.word_wrap = True
    
    add_bullet(tf_dash, "Live Camera Overlay", "Webcam stream displays live bounding boxes. Recognized faces are boxed green with matching names; unknown faces are boxed red.")
    add_bullet(tf_dash, "Dynamic Counters", "Shows cards for Registered Students, Present, Absent, and Attendance rate in real-time.")
    add_bullet(tf_dash, "Server-Sent Events (SSE)", "Enables server-to-client notifications. Pushes name, ID, time, and updated chart vectors automatically.")
    add_bullet(tf_dash, "Audio Feedback Cue", "Uses HTML5 Web Audio context to trigger dual success chimes on attendance log, and error buzz on warnings.")

    # ------------------ SLIDE 9: OPERATIONAL FLOW ------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_slide_header(slide9, "System Operational Flow")
    
    steps = [
        ("Step 1: Register", "Admin adds student details into form (ID, Name, Email, Dept)."),
        ("Step 2: Face capture", "HTML5 webcam starts, aligns face in circle, base64 data sent to API."),
        ("Step 3: Enrollment", "YuNet/SFace extracts embedding and writes to DB. Cache refreshes."),
        ("Step 4: Verification", "Camera detects face, matches query, overlays green box, Marks Present."),
        ("Step 5: Dynamic UI", "Dashboard updates, stats increment, chime sounds, log pops up."),
        ("Step 6: Excel Reports", "Admin filters log database by search query or dates and exports report.")
    ]
    
    for idx, (title, desc) in enumerate(steps):
        col = idx % 2
        row = idx // 2
        
        x = Inches(0.75 + (col * 6.0))
        y = Inches(1.8 + (row * 1.7))
        
        card = slide9.shapes.add_shape(1, x, y, Inches(5.7), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_COLOR
        card.line.fill.background()
        
        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = tf_card.margin_right = Inches(0.2)
        tf_card.margin_top = Inches(0.15)
        
        pt = tf_card.paragraphs[0]
        pt.text = title
        pt.font.name = 'Arial'
        pt.font.size = Pt(16)
        pt.font.bold = True
        pt.font.color.rgb = INDIGO
        pt.space_before = Pt(0)
        pt.space_after = Pt(5)
        
        pd = tf_card.add_paragraph()
        pd.text = desc
        pd.font.name = 'Arial'
        pd.font.size = Pt(12)
        pd.font.color.rgb = SLATE_LIGHT

    # ------------------ SLIDE 10: CONCLUSION ------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_slide_header(slide10, "Conclusion & Future Work")
    
    conc_box = slide10.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.83), Inches(5.0))
    tf_conc = conc_box.text_frame
    tf_conc.word_wrap = True
    
    add_bullet(tf_conc, "Project Summary", "Delivered a fully functional, real-time AI Face Recognition Attendance System with zero compilation requirements, modern design layout, and automated spreadsheet logs.")
    add_bullet(tf_conc, "Liveness Anti-Spoofing Detection", "Integrate face depth checks or blink detection to prevent students from holding photos/phones to the camera.")
    add_bullet(tf_conc, "IP / Multi-camera Streams", "Connect multiple RTSP cameras to screen multiple entries at high-traffic doorways.")
    add_bullet(tf_conc, "Automated Notification Alerts", "Deploy SMS/Email hooks using Twilio/SMTP to auto-notify supervisors/parents when students are missing.")

    # Save presentation
    output_path = "AI_Face_Recognition_Attendance_System.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    create_presentation()
