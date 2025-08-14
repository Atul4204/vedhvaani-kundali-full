from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pathlib import Path
import io, json

OUT = Path(__file__).resolve().parent.parent.parent / 'out'
OUT.mkdir(parents=True, exist_ok=True)

def make_pdf_report(kundali_data, lang='hi'):
    # kundali_data is a dict from main endpoint; render a simple PDF using ReportLab
    name = kundali_data.get('name','user')
    out_file = OUT / f"kundali_{name}_{int(kundali_data.get('rashi_lagna',0))}.pdf"
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin
    c.setFont('Helvetica-Bold', 16)
    c.drawString(margin, y, 'VedhVaani Kundali Report')
    y -= 30
    c.setFont('Helvetica', 12)
    c.drawString(margin, y, f"Name: {kundali_data.get('name')}")
    y -= 18
    c.drawString(margin, y, f"Language: {kundali_data.get('language')} | Chart: {kundali_data.get('chart_style')}")
    y -= 20
    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin, y, 'Ascendant / Rashi')
    y -= 16
    c.setFont('Helvetica', 11)
    c.drawString(margin, y, f"Ascendant: {round(kundali_data.get('ascendant',0),2)} | Rashi: {kundali_data.get('rashi_lagna')}")
    y -= 18
    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin, y, 'Moon Nakshatra')
    y -= 14
    c.setFont('Helvetica', 11)
    c.drawString(margin, y, f"{kundali_data.get('moon_nakshatra')} (Pada {kundali_data.get('moon_pada')})")
    y -= 18
    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin, y, 'Planets:')
    y -= 14
    c.setFont('Helvetica', 10)
    for p,info in kundali_data.get('planets', {}).items():
        if y < 60:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, f"{p}: {info.get('lon')}")
        y -= 12
    c.showPage()
    c.save()
    buffer.seek(0)
    with open(out_file, 'wb') as f:
        f.write(buffer.read())
    return str(out_file)
