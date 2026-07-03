import os
import sys
import urllib.request
from pathlib import Path

# Paths
WORKSPACE = Path(__file__).resolve().parent
FONTS_DIR = WORKSPACE / 'fonts'
FONTS_DIR.mkdir(exist_ok=True)

REGULAR_FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf"
BOLD_FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf"

REGULAR_FONT_PATH = FONTS_DIR / "NotoSansDevanagari-Regular.ttf"
BOLD_FONT_PATH = FONTS_DIR / "NotoSansDevanagari-Bold.ttf"

LOGO_PATH = WORKSPACE / 'logo.webp'
SD_FORM_PATH = WORKSPACE / 'admission-form.pdf'
PRERNA_FORM_PATH = WORKSPACE / 'prerna-form.pdf'

def download_fonts():
    print("Downloading Hindi fonts...")
    if not REGULAR_FONT_PATH.exists():
        print("Downloading NotoSansDevanagari-Regular.ttf...")
        urllib.request.urlretrieve(REGULAR_FONT_URL, REGULAR_FONT_PATH)
    if not BOLD_FONT_PATH.exists():
        print("Downloading NotoSansDevanagari-Bold.ttf...")
        urllib.request.urlretrieve(BOLD_FONT_URL, BOLD_FONT_PATH)
    print("Fonts ready.")

def create_sd_form():
    print("Creating S.D. Public School Admission Form...")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.platypus import Image

    doc = SimpleDocTemplate(
        str(SD_FORM_PATH),
        pagesize=A4,
        leftMargin=12*mm,
        rightMargin=12*mm,
        topMargin=10*mm,
        bottomMargin=10*mm,
        title="S.D. Public School Admission Form"
    )

    styles = getSampleStyleSheet()
    normal = styles['Normal']

    # Custom styles
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=normal,
        fontSize=8,
        leading=9,
        fontName='Helvetica'
    )
    bold_label_style = ParagraphStyle(
        'BoldLabelStyle',
        parent=normal,
        fontSize=8,
        leading=9,
        fontName='Helvetica-Bold'
    )

    story = []

    # Header with Logo
    logo_img = ""
    if LOGO_PATH.exists():
        try:
            logo_img = Image(str(LOGO_PATH), width=18*mm, height=18*mm)
        except Exception as e:
            print(f"Error loading logo: {e}")

    header_text = """
    <para align="center">
    <b><font size="12" color="#1e3a8a">MAHAVIR EDUCATIONAL TRUST, AIROLI</font></b><br/>
    <b><font size="10" color="#1e3a8a">S.D. PUBLIC SCHOOL GHANSOLI</font></b><br/>
    <font size="8" color="#1e3a8a"><u><b>ADMISSION FORM</b></u></font>
    </para>
    """
    
    header_table = Table([[logo_img, Paragraph(header_text, normal)]], colWidths=[22*mm, 164*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 2*mm))

    # Helper function for section headers
    def make_section_header(text):
        p = Paragraph(f"<b>{text}</b>", ParagraphStyle('SecHeader', parent=normal, fontSize=8, leading=10, textColor=colors.HexColor('#1e3a8a'), fontName='Helvetica-Bold'))
        t = Table([["", p]], colWidths=[1.5*mm, 184.5*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#1e3a8a')),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor('#e0f2fe')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (1,0), (1,0), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    # Helper function for grid rows
    def make_grid_row(fields, widths, height=26):
        total_field_width = sum(widths)
        remaining_space = 186 - total_field_width
        num_spacers = len(widths) - 1
        spacer_width = remaining_space / num_spacers if num_spacers > 0 else 0
        
        row_cells = []
        col_widths = []
        
        for i, f in enumerate(fields):
            row_cells.append(Paragraph(f if f else "", label_style))
            col_widths.append(widths[i] * mm)
            if i < len(fields) - 1:
                row_cells.append("")
                col_widths.append(spacer_width * mm)
                
        t = Table([row_cells], colWidths=col_widths, rowHeights=[height])
        
        style_commands = [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]
        
        for i in range(len(fields)):
            col_idx = i * 2
            style_commands.append(('LINEBELOW', (col_idx, 0), (col_idx, 0), 0.5, colors.HexColor('#94a3b8')))
            
        t.setStyle(TableStyle(style_commands))
        return t

    # Section 1: Student Primary Details
    story.append(make_section_header("1. STUDENT PRIMARY DETAILS"))
    story.append(Spacer(1, 1*mm))
    story.append(make_grid_row(["Surname", "Name", "Father's Name"], [58, 58, 58], height=24))
    story.append(make_grid_row(["Name in Devanagari Script"], [186], height=24))
    story.append(make_grid_row(["Date of Birth", "Age", "Nationality"], [70, 40, 70], height=24))
    story.append(make_grid_row(["Place of Birth", "District", "State"], [58, 58, 58], height=24))
    story.append(make_grid_row(["Religion", "Caste", "Sub Caste"], [58, 58, 58], height=24))
    story.append(make_grid_row(["Aadhaar No.", "Admission in (Class/Std.)"], [90, 90], height=24))
    story.append(Spacer(1, 2*mm))

    # Section 2: Parent & Background Information
    story.append(make_section_header("2. PARENT & BACKGROUND INFORMATION"))
    story.append(Spacer(1, 1*mm))
    story.append(make_grid_row(["Father's Name in Full"], [186], height=24))
    story.append(make_grid_row(["Father's Education", "Father's Occupation"], [90, 90], height=24))
    story.append(make_grid_row(["Office Address & Phone"], [186], height=24))
    story.append(make_grid_row(["Residential Address & Phone"], [186], height=24))
    story.append(make_grid_row(["Native Place", "Joint Monthly Income / Parent Income in Rs."], [90, 90], height=24))
    story.append(make_grid_row(["Languages Spoken at Home", "Languages Spoken by Child"], [90, 90], height=24))
    story.append(Spacer(1, 2*mm))

    # Section 3: Siblings Details
    story.append(make_section_header("3. OTHER CHILDREN DETAILS (SIBLINGS)"))
    story.append(Spacer(1, 1.5*mm))
    
    sibling_data = [
        [
            Paragraph("Name", ParagraphStyle('Th', parent=normal, fontSize=7.5, leading=9, alignment=0, fontName='Helvetica-Bold')),
            Paragraph("Age", ParagraphStyle('Th', parent=normal, fontSize=7.5, leading=9, alignment=0, fontName='Helvetica-Bold')),
            Paragraph("School", ParagraphStyle('Th', parent=normal, fontSize=7.5, leading=9, alignment=0, fontName='Helvetica-Bold')),
            Paragraph("Std.", ParagraphStyle('Th', parent=normal, fontSize=7.5, leading=9, alignment=0, fontName='Helvetica-Bold'))
        ],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""]
    ]
    sibling_table = Table(sibling_data, colWidths=[70*mm, 20*mm, 70*mm, 26*mm], rowHeights=[14, 16, 16, 16])
    sibling_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sibling_table)
    story.append(Spacer(1, 3*mm))

    # Footer section
    footer_data = [
        ["", "", ""], # Line row
        [
            Paragraph("Date", label_style),
            "",
            Paragraph("Parent / Guardian Signature", ParagraphStyle('RL', parent=label_style, alignment=2))
        ]
    ]
    footer_table = Table(footer_data, colWidths=[50*mm, 86*mm, 50*mm], rowHeights=[10, 12])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (0,0), 0.5, colors.HexColor('#94a3b8')),
        ('LINEBELOW', (2,0), (2,0), 0.5, colors.HexColor('#94a3b8')),
    ]))
    story.append(footer_table)

    doc.build(story)
    print("S.D. Public form created successfully.")

def create_prerna_form():
    print("Creating Prerna School Admission Form (Hindi)...")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.platypus import Image
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFontFamily

    # Register Hindi Font
    pdfmetrics.registerFont(TTFont('Hindi', str(REGULAR_FONT_PATH)))
    pdfmetrics.registerFont(TTFont('Hindi-Bold', str(BOLD_FONT_PATH)))
    registerFontFamily('Hindi', normal='Hindi', bold='Hindi-Bold')

    doc = SimpleDocTemplate(
        str(PRERNA_FORM_PATH),
        pagesize=A4,
        leftMargin=12*mm,
        rightMargin=12*mm,
        topMargin=10*mm,
        bottomMargin=10*mm,
        title="प्रेरणा विद्यालय प्रवेश अर्ज"
    )

    styles = getSampleStyleSheet()
    normal = styles['Normal']

    # Custom Hindi Styles
    hindi_style = ParagraphStyle(
        'HindiStyle',
        parent=normal,
        fontName='Hindi',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1f2937')
    )
    
    hindi_bold_style = ParagraphStyle(
        'HindiBoldStyle',
        parent=normal,
        fontName='Hindi-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#111827')
    )

    story = []

    # Header section with Logo, Mob, and Photo box
    logo_img = ""
    if LOGO_PATH.exists():
        try:
            logo_img = Image(str(LOGO_PATH), width=16*mm, height=16*mm)
        except Exception as e:
            print(f"Error loading logo: {e}")

    # Photo box
    photo_box_data = [[Paragraph("<font size='7' face='Hindi'>फोटो</font>", ParagraphStyle('PhotoStyle', parent=normal, alignment=1))]]
    photo_box_table = Table(photo_box_data, colWidths=[20*mm], rowHeights=[24*mm])
    photo_box_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    # Title block
    title_text = """
    <para align="center">
    <font size="7" face="Hindi-Bold">सरकार मान्य</font><br/>
    <b><font size="11" face="Hindi-Bold" color="#1e3a8a">महावीर एज्युकेशनल ट्रस्ट ऐरोली संचालित</font></b><br/>
    <b><font size="13" face="Hindi-Bold" color="#1e3a8a">प्रेरणा विद्यालय घणसोली</font></b><br/>
    <font size="8" face="Hindi-Bold">(हिंदी माध्यम)</font>
    </para>
    """
    
    # Left side: प्रवेश अर्ज
    left_header = Paragraph("<font size='8' face='Hindi-Bold'>-: प्रवेश अर्ज :-</font>", ParagraphStyle('LH', parent=normal, alignment=1))
    
    # Right side: Mob + Photo
    right_header_data = [
        [Paragraph("<font size='7' face='Hindi-Bold'>Mob.: 9004003160</font>", ParagraphStyle('RH', parent=normal, alignment=1))],
        [photo_box_table]
    ]
    right_header_table = Table(right_header_data, colWidths=[25*mm])
    right_header_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))

    # Main header grid
    header_grid_data = [
        [left_header, logo_img, Paragraph(title_text, normal), right_header_table]
    ]
    header_grid = Table(header_grid_data, colWidths=[28*mm, 18*mm, 115*mm, 25*mm])
    header_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(header_grid)

    # Sub-headers
    sub_addr = Paragraph("<font size='7' face='Hindi-Bold' color='#4b5563'>कार्यालय : भवानी मंदिर के पास, कौलआली, घणसोलीगांव, नवी मुंबई, जि. ठाणे, पिन:४०० ७०१.</font>", ParagraphStyle('SA', parent=normal, alignment=1))
    story.append(Table([[sub_addr]], colWidths=[186*mm], style=[('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')), ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)]))
    story.append(Spacer(1, 1*mm))

    sub_section = Paragraph("<u><b><font size='9' face='Hindi-Bold'>प्राथमिक / माध्यमिक</font></b></u>", ParagraphStyle('SS', parent=normal, alignment=1))
    story.append(Table([[sub_section]], colWidths=[186*mm], style=[('ALIGN', (0,0), (-1,-1), 'CENTER'), ('BOTTOMPADDING', (0,0), (-1,-1), 1), ('TOPPADDING', (0,0), (-1,-1), 1)]))
    story.append(Spacer(1, 1*mm))

    # Custom Hindi Form Row Helper
    def make_hindi_row(cells_and_widths, height=18):
        col_widths = []
        row_data = []
        style_commands = [
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]
        for i, (content, width, has_line) in enumerate(cells_and_widths):
            col_widths.append(width * mm)
            if isinstance(content, str) and content != "":
                row_data.append(Paragraph(content, hindi_style))
            else:
                row_data.append(content)
            if has_line:
                style_commands.append(('LINEBELOW', (i, 0), (i, 0), 0.5, colors.HexColor('#94a3b8')))
        t = Table([row_data], colWidths=col_widths, rowHeights=[height])
        t.setStyle(TableStyle(style_commands))
        return t

    # 1. Student Name with sub-labels
    name_fields = [
        ("", 50, True),
        ("", 4, False), # spacer
        ("", 50, True),
        ("", 4, False), # spacer
        ("", 45, True)
    ]
    name_table = Table([[
        "", "", "", "", ""
    ], [
        Paragraph("<font size='6' face='Hindi' color='#4b5563'>उपन्यास / उपनाम</font>", ParagraphStyle('HSub', parent=normal, alignment=1)),
        "",
        Paragraph("<font size='6' face='Hindi' color='#4b5563'>नाम</font>", ParagraphStyle('HSub', parent=normal, alignment=1)),
        "",
        Paragraph("<font size='6' face='Hindi' color='#4b5563'>पिता का नाम</font>", ParagraphStyle('HSub', parent=normal, alignment=1))
    ]], colWidths=[50*mm, 4*mm, 50*mm, 4*mm, 45*mm], rowHeights=[12, 8])
    name_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (0,0), 0.5, colors.HexColor('#94a3b8')),
        ('LINEBELOW', (2,0), (2,0), 0.5, colors.HexColor('#94a3b8')),
        ('LINEBELOW', (4,0), (4,0), 0.5, colors.HexColor('#94a3b8')),
    ]))

    story.append(Table([[Paragraph("<b>१. विद्यार्थी का नाम :</b>", hindi_style), name_table]], colWidths=[33*mm, 153*mm], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(Spacer(1, 1*mm))

    # Form Fields
    story.append(make_hindi_row([("<b>२. माँ का नाम :</b>", 22, False), ("", 164, True)], height=15))
    story.append(make_hindi_row([("<b>३. जन्म तिथी (अंको में) :</b>", 34, False), ("", 45, True), ("", 6, False), ("<b>(शब्दों में) :</b>", 20, False), ("", 81, True)], height=15))
    story.append(make_hindi_row([("<b>४. जन्म स्थान :</b>", 22, False), ("", 164, True)], height=15))
    story.append(make_hindi_row([("<b>५. निवास स्थान का पता :</b>", 34, False), ("", 152, True)], height=15))
    story.append(make_hindi_row([("<b>व फोन नं. :</b>", 18, False), ("", 168, True)], height=15))
    story.append(make_hindi_row([("<b>६. कार्यालय का पता :</b>", 28, False), ("", 158, True)], height=15))
    story.append(make_hindi_row([("<b>७. पालक की शिक्षा : पिता</b>", 36, False), ("", 54, True), ("", 6, False), ("<b>माता</b>", 12, False), ("", 78, True)], height=15))
    story.append(make_hindi_row([("<b>८. स्थायी पता :</b>", 22, False), ("", 164, True)], height=15))
    story.append(make_hindi_row([("<b>९. व्यवसाय :</b>", 18, False), ("", 70, True), ("", 6, False), ("<b>वार्षिक आय :</b>", 20, False), ("", 72, True)], height=15))
    story.append(make_hindi_row([
        ("<b>१०. जाति :</b>", 14, False), ("", 24, True), ("", 4, False),
        ("<b>उपजाति :</b>", 14, False), ("", 24, True), ("", 4, False),
        ("<b>धर्म :</b>", 11, False), ("", 24, True), ("", 4, False),
        ("<b>राष्ट्रीयता :</b>", 18, False), ("", 43, True)
    ], height=15))
    story.append(make_hindi_row([("<b>११. किस कक्षा में प्रवेश चाहता / चाहती है :</b>", 54, False), ("", 132, True)], height=15))
    story.append(make_hindi_row([("<b>१२. किस कक्षा को छोड़कर आया है, और कहाँ से :</b>", 64, False), ("", 122, True)], height=15))
    story.append(Spacer(1, 2*mm))

    # Sibling Section
    story.append(Paragraph("<b>१३. विद्यालय में शिक्षा ग्रहण कर रहें छात्र / छात्रा का नाम</b>", hindi_bold_style))
    story.append(Spacer(1, 1*mm))

    sibling_headers = [
        Paragraph("<b>क्र.</b>", ParagraphStyle('H1', parent=normal, fontName='Hindi-Bold', fontSize=7, alignment=1)),
        Paragraph("<b>नाम</b>", ParagraphStyle('H2', parent=normal, fontName='Hindi-Bold', fontSize=7, alignment=1)),
        Paragraph("<b>कक्षा</b>", ParagraphStyle('H3', parent=normal, fontName='Hindi-Bold', fontSize=7, alignment=1)),
        Paragraph("<b>वर्ष</b>", ParagraphStyle('H4', parent=normal, fontName='Hindi-Bold', fontSize=7, alignment=1))
    ]
    sibling_data = [
        sibling_headers,
        [Paragraph("<font face='Hindi'>१</font>", ParagraphStyle('C1', parent=normal, alignment=1)), "", "", ""],
        [Paragraph("<font face='Hindi'>२</font>", ParagraphStyle('C2', parent=normal, alignment=1)), "", "", ""],
        [Paragraph("<font face='Hindi'>३</font>", ParagraphStyle('C3', parent=normal, alignment=1)), "", "", ""]
    ]
    sibling_table = Table(sibling_data, colWidths=[15*mm, 101*mm, 35*mm, 35*mm], rowHeights=[13, 14, 14, 14])
    sibling_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(sibling_table)
    story.append(Spacer(1, 2*mm))

    # Declaration
    decl_text = "मैं, विद्यालय के सभी नियमों को अच्छी तरह से जान लिया हूँ और मैं उसका समुचित पालन करूँगा।"
    story.append(Paragraph(f"<font face='Hindi'>{decl_text}</font>", ParagraphStyle('Decl', parent=normal, fontName='Hindi', fontSize=7.5, leading=9)))
    
    note_text = "<b>सूचना: प्रवेश के समय छात्र का मूल प्रमाणपत्र / जन्म प्रमाणपत्र एवम् परीक्षाफल लाना आवश्यक है।</b>"
    story.append(Paragraph(f"<font face='Hindi'>{note_text}</font>", ParagraphStyle('Note', parent=normal, fontName='Hindi', fontSize=7, leading=9, alignment=1)))
    story.append(Spacer(1, 2*mm))

    # Parent Signature row
    sig_data = [["", Paragraph("............................................<br/><b>पालक हस्ताक्षर</b>", ParagraphStyle('PSig', parent=normal, fontName='Hindi', fontSize=7.5, leading=10, alignment=1))]]
    sig_table = Table(sig_data, colWidths=[126*mm, 60*mm])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 2*mm))

    # Office Section
    office_header = Paragraph("<b><u>कार्यालय के लिये.</u></b>", hindi_bold_style)
    story.append(office_header)
    story.append(Spacer(1, 1*mm))

    office_row1 = make_hindi_row([
        ("<b>१. परिक्षण कर्ता</b>", 25, False), ("", 50, True), ("", 10, False),
        ("<b>२. किस कक्षा में प्रवेश किया गया</b>", 45, False), ("", 56, True)
    ], height=14)
    story.append(office_row1)
    
    # Office Row 2 with Date and Headmaster Signature
    hm_sig_table = Table([["", ""], [Paragraph("<b>मुख्याध्यापक सही</b>", ParagraphStyle('HMSig', parent=normal, fontName='Hindi-Bold', fontSize=7.5, alignment=1)), ""]], colWidths=[66*mm, 8*mm], rowHeights=[12, 10])
    hm_sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (0,0), 0.5, colors.HexColor('#94a3b8')),
    ]))

    office_row2 = Table([
        [Paragraph("<b>दिनांक</b>", hindi_bold_style), "", "", hm_sig_table]
    ], colWidths=[12*mm, 40*mm, 60*mm, 74*mm], rowHeights=[22])
    office_row2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (1,0), (1,0), 0.5, colors.HexColor('#94a3b8')), # line for date
    ]))
    story.append(office_row2)
    story.append(Spacer(1, 3*mm))

    # Bottom left signature
    bottom_sig_table = Table([["", ""], [Paragraph("<b>सही</b>", ParagraphStyle('BSig', parent=normal, fontName='Hindi-Bold', fontSize=7.5, alignment=1)), ""]], colWidths=[40*mm, 146*mm], rowHeights=[12, 10])
    bottom_sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (0,0), 0.5, colors.HexColor('#94a3b8')),
    ]))
    story.append(bottom_sig_table)

    doc.build(story)
    print("Prerna Hindi school form created successfully.")

if __name__ == '__main__':
    download_fonts()
    create_sd_form()
    create_prerna_form()
