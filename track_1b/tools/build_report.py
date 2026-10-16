"""Render the report draft as a PDF. No inference or paid API calls.

Install authoring dependencies: python -m pip install reportlab pypdf
Usage: python tools/build_report.py --output /path/to/leGML_Report_DRAFT.pdf
Final export requires --final and a completed report source; review evidence separately.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import re

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted,
)

ROOT = Path(__file__).resolve().parents[1]
GREEN = colors.HexColor('#0B3D2C')


def inline(text: str) -> str:
    text = escape(text.replace('\u2014', '-').replace('\u2013', '-').replace('\u2011', '-'))
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#0B3D2C">\1</link>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
    return text


def render(source: Path, output: Path, final: bool = False) -> None:
    text = source.read_text(encoding='utf-8')
    pending = sorted(set(re.findall(r'\{\{([^}]+)\}\}', text)))
    if final and (pending or re.search(r'\bTODO\b|\bDRAFT\b', text)):
        raise SystemExit('Final export blocked: unresolved placeholders or draft markers remain.')
    text = re.sub(r'\{\{([^}]+)\}\}', r'[PENDING: \1]', text)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ReportBody', fontName='Helvetica', fontSize=9,
                              leading=12.1, spaceAfter=5, splitLongWords=True))
    styles.add(ParagraphStyle(name='ReportSmall', parent=styles['ReportBody'],
                              fontSize=7.4, leading=9.5, spaceAfter=0))
    styles.add(ParagraphStyle(name='ReportTitle', fontName='Helvetica-Bold', fontSize=19,
                              leading=22, textColor=GREEN, spaceAfter=10))
    styles.add(ParagraphStyle(name='ReportH2', fontName='Helvetica-Bold', fontSize=12,
                              leading=15, textColor=GREEN, spaceBefore=10, spaceAfter=6,
                              keepWithNext=True))
    styles.add(ParagraphStyle(name='ReportH3', fontName='Helvetica-Bold', fontSize=9.5,
                              leading=12, spaceBefore=7, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle(name='Notice', parent=styles['ReportBody'], fontSize=9,
                              borderColor=GREEN, borderWidth=0.6, borderPadding=7,
                              backColor=colors.HexColor('#F0F5F2'), spaceAfter=12))
    story = []
    if not final:
        story.append(Paragraph('<b>DRAFT FOR REVIEW - DO NOT SUBMIT YET</b><br/>'
            'Results and human-review fields are unfinished. The form offers Apertus v1.5; '
            'this report describes 2509. Confirm model eligibility before submission. '
            'Statements from the project draft remain subject to evidence checks.', styles['Notice']))
    lines = text.splitlines()
    i = 0
    width = A4[0] - 36 * mm
    while i < len(lines):
        line = lines[i].strip()
        if not line or line in ('----', '---'):
            i += 1
            continue
        if line.startswith('```'):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i])
                i += 1
            # Wrap code for a readable page rather than clipping long shell commands.
            import textwrap
            wrapped = '\n'.join('\n'.join(textwrap.wrap(s, 98, subsequent_indent='  ')) or '' for s in block)
            story.append(Preformatted(wrapped, ParagraphStyle('Code', fontName='Courier',
                                      fontSize=7.4, leading=10, spaceAfter=7)))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            ncols = max(map(len, rows))
            rows = [r + [''] * (ncols - len(r)) for r in rows]
            widths = ([width * .18, width * .41, width * .41] if ncols == 3
                      else [width * .25, width * .75] if ncols == 2
                      else [width / ncols] * ncols)
            table = Table([[Paragraph(inline(c), styles['ReportSmall']) for c in r] for r in rows],
                          colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E5EFE9')),
                ('GRID', (0, 0), (-1, -1), .3, colors.HexColor('#B7C8BD')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story += [table, Spacer(1, 7)]
            continue
        if line.startswith('# '):
            style = styles['ReportTitle']
            content = line[2:]
        elif line.startswith('## '):
            style, content = styles['ReportH2'], line[3:]
        elif line.startswith('### '):
            style, content = styles['ReportH3'], line[4:]
        else:
            style = styles['ReportBody']
            block = [line]
            is_item = bool(re.match(r'(- |\d+\. )', line))
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'(#|\||```|- |\d+\. )', lines[i].strip()):
                if lines[i].lstrip().startswith('**') and not is_item:
                    break
                block.append(lines[i].strip())
                i += 1
            content = ' '.join(block)
            if content.startswith('- '):
                content = '- ' + content[2:]
            story.append(Paragraph(inline(content), style))
            continue
        story.append(Paragraph(inline(content), style))
        i += 1

    output.parent.mkdir(parents=True, exist_ok=True)

    def page_footer(canvas, doc):
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(.6)
        canvas.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(GREEN)
        canvas.drawString(18 * mm, 10.7 * mm, 'leGML | Hack Apertus | Track 1B - Core Task Intelligence')
        canvas.drawRightString(A4[0] - 18 * mm, 10.7 * mm,
                              ('DRAFT | ' if not final else '') + str(doc.page))

    doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
                            topMargin=17 * mm, bottomMargin=20 * mm,
                            title='leGML - Apertus Swiss Insurance Law - ' + ('Report' if final else 'Draft'),
                            author='leGML')
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    pages = len(PdfReader(output).pages)
    print(f'PDF: {output} ({pages} pages; {len(pending)} pending fields)')
    if pages > 6:
        raise SystemExit('PDF exceeds six pages; shorten the source before submission.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, default=ROOT / 'technical_report.md')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--final', action='store_true')
    args = ap.parse_args()
    render(args.source, args.output, args.final)
