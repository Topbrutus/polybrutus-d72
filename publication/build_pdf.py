#!/usr/bin/env python3
"""Rebuild a deterministic readable scientific PDF from the accompanying Markdown."""
from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
inp=HERE/'POLYBRUTUS_72D_NOTE.md'
out=HERE/'POLYBRUTUS_72D_NOTE.pdf'
normal,bold='Helvetica','Helvetica-Bold'
fonts=Path('C:/Windows/Fonts')
if (fonts/'arial.ttf').exists() and (fonts/'arialbd.ttf').exists():
    pdfmetrics.registerFont(TTFont('AstraArial',str(fonts/'arial.ttf')))
    pdfmetrics.registerFont(TTFont('AstraArialBold',str(fonts/'arialbd.ttf')))
    pdfmetrics.registerFontFamily('AstraArial',normal='AstraArial',bold='AstraArialBold')
    normal,bold='AstraArial','AstraArialBold'
navy=colors.HexColor('#152a3f')
muted=colors.HexColor('#3d716d')
styles={
 'title':ParagraphStyle('title',fontName=bold,fontSize=18.5,leading=24,textColor=navy,spaceAfter=11),
 'h2':ParagraphStyle('h2',fontName=bold,fontSize=12,leading=16,textColor=navy,spaceBefore=11,spaceAfter=6,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName=bold,fontSize=10,leading=14,textColor=navy,spaceBefore=9,spaceAfter=5,keepWithNext=True),
 'body':ParagraphStyle('body',fontName=normal,fontSize=9.1,leading=13.1,textColor=colors.HexColor('#1d2834'),spaceAfter=6),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=8.2,leading=11,textColor=muted,leftIndent=12,spaceBefore=5,spaceAfter=10),
}
story=[]
def put_para(lines):
    v=' '.join(x.strip() for x in lines).replace('**','').replace('\\','')
    if v:
        story.append(Paragraph(escape(v),styles['body']))
buf=[]
for raw in inp.read_text(encoding='utf-8').splitlines():
    line=raw.rstrip()
    if not line.strip():
        put_para(buf);buf=[]
        continue
    if line.startswith('#'):
        put_para(buf);buf=[]
        if line.startswith("## 4."):story.append(PageBreak())
        level=len(line)-len(line.lstrip('#'))
        content=line[level:].strip()
        story.append(Paragraph(escape(content),styles['title' if level==1 else 'h2' if level==2 else 'h3']))
        if level==1:story.append(HRFlowable(width='100%',thickness=1,color=colors.HexColor('#bdcbd8'),spaceAfter=12))
    elif line.startswith('  '):
        put_para(buf);buf=[]
        story.append(Preformatted(line.strip(),styles['code']))
    else:
        buf.append(line)
put_para(buf)
def footer(canv,doc):
    canv.saveState()
    w,h=A4
    canv.setStrokeColor(colors.HexColor('#c4d0dc'))
    canv.line(45,43,w-45,43)
    canv.setFont(normal,8)
    canv.setFillColor(muted)
    canv.drawString(46,29,'Polybrutus 72D | Gabriel St-Pierre | 21 Nov 2026')
    canv.drawRightString(w-46,29,f'Page {doc.page}')
    canv.restoreState()
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=47,leftMargin=47,topMargin=45,bottomMargin=52,
    title='Polybrutus 72D - Exact Euclidean metric and ideal graph spectrum',
    author='Gabriel St-Pierre',subject='Exact reproducible mathematical case study',invariant=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
assert out.exists() and out.stat().st_size>1000
print('PDF_READY',out.name,'BYTES',out.stat().st_size)
