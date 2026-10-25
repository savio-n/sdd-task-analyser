from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

src = Path("docs/governance_ethics_report.md")
dst = Path("docs/governance_ethics_report.pdf")

if not src.exists():
    raise SystemExit(f"Relatório não encontrado: {src}")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="SectionHeading", parent=styles["Heading2"], spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="ReportBody", parent=styles["BodyText"], leading=14, spaceAfter=7))

story = []
in_code = False

for raw in src.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if line.startswith("```"):
        in_code = not in_code
    elif not line:
        story.append(Spacer(1, 4))
    elif line.startswith("# "):
        story.append(Paragraph(escape(line[2:]), styles["ReportTitle"]))
    elif line.startswith("## "):
        story.append(Paragraph(escape(line[3:]), styles["SectionHeading"]))
    elif line.startswith("### "):
        story.append(Paragraph(escape(line[4:]), styles["Heading3"]))
    elif line.startswith("- ") or re.match(r"^\d+\.\s", line):
        item = re.sub(r"^(- |\d+\.\s)", "", line)
        story.append(Paragraph("• " + escape(item), styles["ReportBody"]))
    elif line.startswith("> "):
        story.append(Paragraph(escape(line[2:]), styles["Italic"]))
    else:
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"`(.*?)`", r"\1", line)
        story.append(Paragraph(escape(line), styles["Code"] if in_code else styles["ReportBody"]))

doc = SimpleDocTemplate(
    str(dst), pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Relatório de Governança, Segurança e Ética no Uso de IA",
    author="Sávio Arbuês Abrahão Nery"
)
doc.build(story)
print(f"PDF criado: {dst.resolve()}")
