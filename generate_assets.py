import os
import sys
import urllib.request
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
LOGO_URL = 'https://i.ibb.co/2YSGxfPd/IMG-20260324-WA0011.webp'
LOGO_PATH = WORKSPACE / 'logo.webp'
PROSPECTUS_PATH = WORKSPACE / 'prospectus.pdf'
ADMISSION_FORM_PATH = WORKSPACE / 'admission-form.pdf'


def download_logo():
    print('Downloading logo...')
    urllib.request.urlretrieve(LOGO_URL, LOGO_PATH)
    print('Saved logo to', LOGO_PATH)


def install_package(pkg):
    import subprocess
    print('Installing package', pkg)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])


def create_pdfs():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
    except ImportError:
        install_package('reportlab')
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors

    styles = getSampleStyleSheet()
    normal = styles['Normal']
    heading = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=22, leading=26, spaceAfter=12, textColor=colors.HexColor('#1e3a8a'))
    subheading = ParagraphStyle('Subheading', parent=styles['Heading2'], fontSize=16, leading=20, spaceAfter=10, textColor=colors.HexColor('#1e3a8a'))
    body = ParagraphStyle('Body', parent=normal, fontSize=11, leading=15, spaceAfter=8)

    prospectus = SimpleDocTemplate(str(PROSPECTUS_PATH), pagesize=A4, title='S.D. Public High School Prospectus')
    content = []
    content.append(Paragraph('S.D. Public High School Prospectus', heading))
    content.append(Paragraph('Quality Education for Every Child', subheading))
    content.append(Paragraph('Welcome to S.D. Public High School, a trusted English-medium school in Ghansoli, dedicated to providing academic excellence across all key stages.', body))
    content.append(Spacer(1, 6))

    prospectus_sections = [
        ('Primary Section (Classes 1 to 8)', 'Comprehensive education for students in Grades 1 to 8, focusing on English, Mathematics, Science, Social Studies, and Hindi, with strong emphasis on values, creativity and personality development.'),
        ('Secondary Section (Classes 9 and 10)', 'Structured exam preparation for Classes 9 and 10 with dedicated coaching, library support, digital learning tools, revision programs and counseling to help students achieve board-level success.'),
        ('Academic Approach', 'Our curriculum blends concept-based instruction, regular assessments, remedial support, activity-led learning and moral education to build confident, responsible learners.'),
        ('Infrastructure & Facilities', 'Well-equipped classrooms, science and computer labs, library, playground and a safe campus that supports both scholastic and co-scholastic growth.'),
        ('Admission Process', 'Simplified admission with transparent application steps, document verification, and support for parents at every stage. Prospective families can apply directly through our admission form PDF or contact school administration.'),
        ('School Highlights', 'Experienced B.Ed-qualified teachers, digital smart classrooms, cultural activities, sports programs, and a caring environment that nurtures each child.'),
        ('Contact Information', 'Address: S.D. Public High School, Ghansoli. Phone: +91 73042 46024. Email: info@sdpublichighschool.edu.in (example contact).'),
    ]

    for title, text in prospectus_sections:
        content.append(Paragraph(title, subheading))
        content.append(Paragraph(text, body))

    content.append(Spacer(1, 12))
    content.append(Paragraph('Class 10th Results & Achievements', subheading))
    results_text = ('Our Class 10th batch achieves strong academic performance year after year. We provide focused exam strategies, doubt clearing sessions, and a supportive school culture that helps students succeed.')
    content.append(Paragraph(results_text, body))

    prospectus.build(content)
    print('Created prospectus at', PROSPECTUS_PATH)

    form = SimpleDocTemplate(str(ADMISSION_FORM_PATH), pagesize=A4, title='S.D. Public High School Admission Form')
    form_content = []
    form_content.append(Paragraph('S.D. Public High School Admission Form', heading))
    form_content.append(Paragraph('Please print this form, fill it clearly, attach required documents, and submit offline at the school office.', body))
    form_content.append(Spacer(1, 12))

    lines = [
        'Student Name: ________________________________________________',
        'Class Applying For: __________________________________________',
        'Date of Birth: ________________________________________________',
        'Previous School Name: ________________________________________',
        'Parent / Guardian Name: _______________________________________',
        'Relationship to Student: ______________________________________',
        'Address: ______________________________________________________',
        '         ______________________________________________________',
        'Contact Number: ______________________________________________',
        'Email (optional): _____________________________________________',
        'Emergency Contact Number: ____________________________________',
        'Academic Details / Notes: _____________________________________',
        '         ______________________________________________________',
    ]
    for line in lines:
        form_content.append(Paragraph(line, body))
        form_content.append(Spacer(1, 4))

    form_content.append(Spacer(1, 12))
    form_content.append(Paragraph('Required Documents (Please attach photocopies):', subheading))
    required_items = [
        '• Birth Certificate',
        '• Previous School Leaving Certificate (if applicable)',
        '• Transfer Certificate (if applicable)',
        '• Two passport-size photographs',
        '• Aadhaar / ID proof of parent or guardian',
    ]
    for item in required_items:
        form_content.append(Paragraph(item, body))

    form_content.append(Spacer(1, 18))
    form_content.append(Paragraph('Declaration:', subheading))
    declaration = 'I certify that the information provided above is true to the best of my knowledge. I agree to comply with school rules and submit the required documents for admission processing.'
    form_content.append(Paragraph(declaration, body))
    form_content.append(Spacer(1, 18))
    form_content.append(Paragraph('Parent / Guardian Signature: ____________________________    Date: ________________', body))

    form.build(form_content)
    print('Created admission form at', ADMISSION_FORM_PATH)


if __name__ == '__main__':
    download_logo()
    create_pdfs()
