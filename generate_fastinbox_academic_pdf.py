from __future__ import annotations

import re
from dataclasses import dataclass
from html import escape
from pathlib import Path

try:
    import pikepdf
except Exception:  # pragma: no cover - optional post-processing
    pikepdf = None

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "docs" / "fastinbox-software-requirements-specification.md"
OUTPUT_PDF = ROOT / "output" / "pdf" / "fastinbox-ers-uniceub-abnt.pdf"
LOGO_PATH = ROOT / "tmp" / "pdfs" / "logoCEUB2021.png"


AUTHOR_NAME = "Thiago L. C. Alves"
CITY = "Brasilia - DF"
YEAR = "2026"

UNI_PURPLE = colors.HexColor("#43054E")
UNI_PURPLE_DARK = colors.HexColor("#330066")
UNI_MAGENTA = colors.HexColor("#C00088")
UNI_GOLD = colors.HexColor("#F0CC25")
TEXT = colors.black
LIGHT_BORDER = colors.HexColor("#B8B0BF")
LIGHT_FILL = colors.HexColor("#F7F3FA")


def md_to_rich_text(text: str) -> str:
    text = escape(text.strip())
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = text.replace("`", "<font name='Courier'>").replace("</font><font name='Courier'>", "")
    if text.count("<font name='Courier'>") % 2 == 0:
        parts = text.split("<font name='Courier'>")
        rebuilt = [parts[0]]
        for idx, part in enumerate(parts[1:], start=1):
            if idx % 2 == 1:
                rebuilt.append("<font name='Courier'>")
                rebuilt.append(part.replace("<font name='Courier'>", ""))
                rebuilt.append("</font>")
            else:
                rebuilt.append(part)
        text = "".join(rebuilt)
    return text


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip()).strip("-").lower()
    return slug or "secao"


def normalize_heading(text: str, level: int) -> str:
    if level == 1:
        return text.upper()
    return text


@dataclass
class Block:
    kind: str
    value: object
    level: int | None = None


def parse_markdown(path: Path) -> list[Block]:
    lines = path.read_text(encoding="utf-8").splitlines()

    start_idx = 0
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            start_idx = idx
            break

    blocks: list[Block] = []
    buffer: list[str] = []
    i = start_idx

    def flush_paragraph() -> None:
        nonlocal buffer
        if buffer:
            paragraph = " ".join(part.strip() for part in buffer if part.strip()).strip()
            if paragraph:
                blocks.append(Block("paragraph", paragraph))
            buffer = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            rows = []
            for row in table_lines:
                cols = [col.strip() for col in row.strip("|").split("|")]
                if cols and all(re.fullmatch(r"[: -]+", col) for col in cols):
                    continue
                rows.append(cols)

            if rows:
                blocks.append(Block("table", rows))
            continue

        heading_match = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            hashes, title = heading_match.groups()
            blocks.append(Block("heading", title.strip(), level=len(hashes) - 1))
            i += 1
            continue

        if re.match(r"^-\s+", stripped):
            flush_paragraph()
            items = []
            while i < len(lines) and re.match(r"^-\s+", lines[i].strip()):
                items.append(re.sub(r"^-\s+", "", lines[i].strip()))
                i += 1
            blocks.append(Block("ul", items))
            continue

        if re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            blocks.append(Block("ol", items))
            continue

        buffer.append(stripped)
        i += 1

    flush_paragraph()
    return blocks


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="BodyABNT",
            parent=styles["Normal"],
            fontName="Times-Roman",
            fontSize=12,
            leading=18,
            alignment=TA_JUSTIFY,
            firstLineIndent=1.25 * cm,
            spaceAfter=8,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyNoIndent",
            parent=styles["BodyABNT"],
            firstLineIndent=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyList",
            parent=styles["BodyNoIndent"],
            leftIndent=0.6 * cm,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading1ABNT",
            parent=styles["Heading1"],
            fontName="Times-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=12,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading2ABNT",
            parent=styles["Heading2"],
            fontName="Times-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=8,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading3ABNT",
            parent=styles["Heading3"],
            fontName="Times-BoldItalic",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=6,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PreTextTitle",
            parent=styles["Heading1"],
            fontName="Times-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=18,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverInstitution",
            parent=styles["Normal"],
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverAuthor",
            parent=styles["Normal"],
            fontName="Times-Roman",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Normal"],
            fontName="Times-Bold",
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Normal"],
            fontName="Times-Roman",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TitleNature",
            parent=styles["Normal"],
            fontName="Times-Roman",
            fontSize=12,
            leading=18,
            alignment=TA_JUSTIFY,
            leftIndent=8 * cm,
            rightIndent=0.5 * cm,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallRef",
            parent=styles["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=16,
            alignment=TA_LEFT,
            textColor=TEXT,
        )
    )
    return styles


class RequirementsDoc(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        self.heading_entries: list[tuple[str, int]] = []
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="main",
        )
        self.addPageTemplates(
            [
                PageTemplate(id="main", frames=[frame], onPage=self.draw_page),
            ]
        )

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()
            if style_name == "Heading1ABNT":
                self.heading_entries.append((text, self.page - 1))

    def draw_page(self, canvas, doc):
        page = canvas.getPageNumber()
        if page == 1:
            canvas.saveState()
            canvas.setFillColor(UNI_PURPLE)
            canvas.rect(0, A4[1] - 4.5 * cm, A4[0], 4.5 * cm, fill=1, stroke=0)
            canvas.setFillColor(UNI_MAGENTA)
            canvas.rect(0, A4[1] - 4.8 * cm, A4[0], 0.3 * cm, fill=1, stroke=0)
            canvas.setFillColor(colors.white)
            canvas.setFont("Times-Bold", 15)
            canvas.drawCentredString(A4[0] / 2, A4[1] - 2.2 * cm, "CENTRO UNIVERSITARIO DE BRASILIA")
            canvas.setFont("Times-Roman", 13)
            canvas.drawCentredString(A4[0] / 2, A4[1] - 2.9 * cm, "UniCEUB")
            canvas.restoreState()
        elif page >= 6:
            canvas.saveState()
            canvas.setFont("Times-Roman", 10)
            canvas.setFillColor(TEXT)
            canvas.drawRightString(A4[0] - doc.rightMargin, A4[1] - 2.2 * cm, str(page - 1))
            canvas.restoreState()


def cover_page(styles):
    story = [
        Spacer(1, 5.5 * cm),
    ]

    story.extend(
        [
            Paragraph(AUTHOR_NAME, styles["CoverAuthor"]),
            Spacer(1, 6.2 * cm),
            Paragraph("FASTINBOX", styles["CoverTitle"]),
            Spacer(1, 0.3 * cm),
            Paragraph("Especificacao de Requisitos de Software", styles["CoverSubtitle"]),
            Spacer(1, 5.6 * cm),
            Paragraph(CITY, styles["CoverAuthor"]),
            Spacer(1, 0.2 * cm),
            Paragraph(YEAR, styles["CoverAuthor"]),
            PageBreak(),
        ]
    )
    return story


def title_page(styles):
    return [
        Spacer(1, 2.2 * cm),
        Paragraph(AUTHOR_NAME, styles["CoverAuthor"]),
        Spacer(1, 4.8 * cm),
        Paragraph("FASTINBOX", styles["CoverTitle"]),
        Spacer(1, 0.3 * cm),
        Paragraph("Especificacao de Requisitos de Software", styles["CoverSubtitle"]),
        Spacer(1, 2.2 * cm),
        Paragraph(
            "Documento academico apresentado ao Centro Universitario de Brasilia - UniCEUB "
            "como especificacao tecnica e funcional do produto FastInBox, estruturado em "
            "conformidade com orientacoes institucionais baseadas nas normas da ABNT.",
            styles["TitleNature"],
        ),
        Spacer(1, 4.2 * cm),
        Paragraph(CITY, styles["CoverAuthor"]),
        Spacer(1, 0.2 * cm),
        Paragraph(YEAR, styles["CoverAuthor"]),
        PageBreak(),
    ]


def resumo_pages(styles):
    resumo = (
        "Este documento apresenta a especificacao de requisitos de software da plataforma "
        "FastInBox, solucao digital voltada a integracao operacional entre nutricionistas, "
        "pacientes, cozinhas parceiras e administracao. O trabalho consolida objetivos do "
        "produto, escopo, stakeholders, premissas, regras de negocio, requisitos funcionais, "
        "requisitos nao funcionais, jornadas, telas necessarias, entidades de dominio, "
        "integracoes externas, riscos e pendencias para validacao. A proposta enfatiza a "
        "operacao white label, a seguranca dos dados, o fluxo de pedidos personalizados, "
        "o controle de comissoes e a rastreabilidade operacional, servindo como base "
        "para alinhamento entre produto, design, engenharia e avaliacao academica."
    )
    abstract = (
        "This document presents the software requirements specification for FastInBox, a digital "
        "platform designed to integrate nutritionists, patients, partner kitchens and administrative "
        "operations in a single workflow. The report consolidates product objectives, scope, "
        "stakeholders, assumptions, business rules, functional requirements, non-functional "
        "requirements, user journeys, required screens, domain entities, external integrations, "
        "risks and pending items for validation. The proposal emphasizes the white-label model, "
        "data security, personalized meal ordering, commission control and operational traceability, "
        "providing a solid basis for alignment across product, design, engineering and academic review."
    )
    return [
        Paragraph("RESUMO", styles["PreTextTitle"]),
        Paragraph(resumo, styles["BodyNoIndent"]),
        Spacer(1, 0.4 * cm),
        Paragraph(
            "<b>Palavras-chave:</b> FastInBox. Engenharia de requisitos. Plataforma white label. "
            "Sistema web. Marmitas personalizadas.",
            styles["BodyNoIndent"],
        ),
        PageBreak(),
        Paragraph("ABSTRACT", styles["PreTextTitle"]),
        Paragraph(abstract, styles["BodyNoIndent"]),
        Spacer(1, 0.4 * cm),
        Paragraph(
            "<b>Keywords:</b> FastInBox. Requirements engineering. White-label platform. "
            "Web system. Personalized meals.",
            styles["BodyNoIndent"],
        ),
        PageBreak(),
    ]


def toc_pages(styles, toc_flowables):
    return [
        Paragraph("SUMARIO", styles["PreTextTitle"]),
        *toc_flowables,
        PageBreak(),
    ]


def build_toc(styles, entries):
    toc_style = ParagraphStyle(
        name="TOCText",
        parent=styles["SmallRef"],
        fontSize=11,
        leading=14,
    )
    rows = []
    for title, page_num in entries:
        rows.append(
            [
                Paragraph(md_to_rich_text(title), toc_style),
                Paragraph(str(page_num), ParagraphStyle(name="TOCPage", parent=toc_style, alignment=TA_RIGHT)),
            ]
        )

    table = Table(rows, colWidths=[14.6 * cm, 1.4 * cm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return [table]


def list_paragraphs(items, styles, numbered=False):
    flowables = []
    for idx, item in enumerate(items, start=1):
        rich_item = md_to_rich_text(item)
        prefix = f"{idx}. " if numbered else "&bull; "
        flowables.append(Paragraph(f"{prefix}{rich_item}", styles["BodyList"]))
    return flowables


def build_table(rows, styles):
    col_count = max(len(row) for row in rows)
    normalized = [row + [""] * (col_count - len(row)) for row in rows]
    paragraph_rows = [
        [Paragraph(md_to_rich_text(cell), styles["SmallRef"]) for cell in row] for row in normalized
    ]
    available_width = A4[0] - (3 * cm) - (2 * cm)
    col_widths = [available_width / col_count] * col_count
    table = Table(paragraph_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_FILL),
                ("TEXTCOLOR", (0, 0), (-1, 0), TEXT),
                ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def body_story(blocks, styles):
    story = []
    first_heading = True

    for block in blocks:
        if block.kind == "heading":
            level = block.level or 1
            style_name = {1: "Heading1ABNT", 2: "Heading2ABNT", 3: "Heading3ABNT"}.get(level, "Heading3ABNT")
            if level == 1 and not first_heading:
                story.append(PageBreak())
            story.append(Paragraph(md_to_rich_text(normalize_heading(str(block.value), level)), styles[style_name]))
            first_heading = False if level == 1 else first_heading
            continue

        if block.kind == "paragraph":
            story.append(Paragraph(md_to_rich_text(str(block.value)), styles["BodyABNT"]))
            continue

        if block.kind == "ul":
            story.extend(list_paragraphs(block.value, styles, numbered=False))
            story.append(Spacer(1, 0.15 * cm))
            continue

        if block.kind == "ol":
            story.extend(list_paragraphs(block.value, styles, numbered=True))
            story.append(Spacer(1, 0.15 * cm))
            continue

        if block.kind == "table":
            story.append(build_table(block.value, styles))
            story.append(Spacer(1, 0.25 * cm))
            continue

    return story


def references_story(styles):
    refs = [
        "CENTRO UNIVERSITARIO DE BRASILIA. <b>Orientacoes institucionais para a elaboracao "
        "de trabalho de conclusao de curso de graduacao</b>. 2. ed. Brasilia: CEUB, 2022. "
        "Disponivel em: https://repositorio.uniceub.br/. Acesso em: 20 mar. 2026.",
        "CENTRO UNIVERSITARIO DE BRASILIA. <b>Portal institucional UniCEUB</b>. Disponivel em: "
        "https://www.uniceub.br/. Acesso em: 20 mar. 2026.",
        "FASTINBOX. <b>Especificacao de Requisitos de Software (ERS)</b>. Documento interno "
        "consolidado para o projeto FastInBox, 2026.",
    ]
    story = [PageBreak(), Paragraph("REFERENCIAS", styles["Heading1ABNT"])]
    for ref in refs:
        story.append(Paragraph(ref, styles["SmallRef"]))
        story.append(Spacer(1, 0.15 * cm))
    return story


def prebuild_heading_entries(styles, blocks):
    prepass_pdf = ROOT / "tmp" / "pdfs" / f"{OUTPUT_PDF.stem}.prepass.pdf"
    prepass_pdf.parent.mkdir(parents=True, exist_ok=True)
    prepass_doc = RequirementsDoc(
        str(prepass_pdf),
        pagesize=A4,
        leftMargin=3 * cm,
        rightMargin=2 * cm,
        topMargin=3 * cm,
        bottomMargin=2 * cm,
        title="FastInBox - Especificacao de Requisitos de Software",
        author=AUTHOR_NAME,
    )
    prepass_story = []
    prepass_story.extend(cover_page(styles))
    prepass_story.extend(title_page(styles))
    prepass_story.extend(resumo_pages(styles))
    prepass_story.extend(body_story(blocks, styles))
    prepass_story.extend(references_story(styles))
    prepass_doc.build(prepass_story)
    return [(title, page + 1) for title, page in prepass_doc.heading_entries]


def main():
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    styles = build_styles()
    blocks = parse_markdown(SOURCE_MD)
    toc_entries = prebuild_heading_entries(styles, blocks)
    toc_flowables = build_toc(styles, toc_entries)

    doc = RequirementsDoc(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=3 * cm,
        rightMargin=2 * cm,
        topMargin=3 * cm,
        bottomMargin=2 * cm,
        title="FastInBox - Especificacao de Requisitos de Software",
        author=AUTHOR_NAME,
    )

    story = []
    story.extend(cover_page(styles))
    story.extend(title_page(styles))
    story.extend(resumo_pages(styles))
    story.extend(toc_pages(styles, toc_flowables))
    story.extend(body_story(blocks, styles))
    story.extend(references_story(styles))

    doc.build(story)
    if pikepdf is not None:
        normalized_pdf = OUTPUT_PDF.with_name(f"{OUTPUT_PDF.stem}.normalized.pdf")
        with pikepdf.open(str(OUTPUT_PDF)) as pdf:
            pdf.save(str(normalized_pdf), linearize=True)
        normalized_pdf.replace(OUTPUT_PDF)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
