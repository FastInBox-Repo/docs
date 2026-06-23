"""Gera o PDF do Projeto Integrador III (FastInBox) seguindo, em layout, tópicos
e estilos, o "Modelo de Projeto Integrador III - Profa Kadidja"."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as canvas_mod
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import Flowable

ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "tmp" / "pdfs" / "ceub_logo_white.png"
OUTPUT_PDF = ROOT / "output" / "pdf" / "projeto-integrador-iii-fastinbox.pdf"

PAGE_W, PAGE_H = A4
LAND_W, LAND_H = landscape(A4)

# ABNT NBR 14724 margins: left/top 3 cm, right/bottom 2 cm -> usable content width.
CONTENT_W = PAGE_W - 5 * cm
CONTENT_W_L = LAND_W - 5 * cm

BLACK = colors.black
WHITE = colors.white
RED = colors.HexColor("#D40000")
GREY_BORDER = colors.HexColor("#999999")
BMC_HEADER = colors.HexColor("#000000")
BMC_HEADER_TEXT = colors.white
EAP_BOX = colors.HexColor("#1F4E79")
EAP_TEXT = colors.white
HIGHLIGHT_YELLOW = colors.HexColor("#FFF59D")


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------


def build_styles():
    styles = getSampleStyleSheet()

    def add(style):
        if style.name in styles.byName:
            del styles.byName[style.name]
        styles.add(style)

    add(ParagraphStyle(
        name="CoverHeader",
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=20,
        alignment=TA_CENTER,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="CoverHeaderTurma",
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=20,
        alignment=TA_CENTER,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="CoverHeaderProf",
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="ProjectName",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="StudentName",
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="CityDate",
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=BLACK,
    ))

    add(ParagraphStyle(
        name="TocTitle",
        fontName="Helvetica",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=BLACK,
        spaceAfter=14,
    ))
    add(ParagraphStyle(
        name="TocItem",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=16,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="TocSubItem",
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=BLACK,
        leftIndent=20,
    ))

    add(ParagraphStyle(
        name="H1Section",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=18,
        alignment=TA_LEFT,
        textColor=BLACK,
        spaceBefore=4,
        spaceAfter=8,
    ))
    add(ParagraphStyle(
        name="H2Section",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=18,
        alignment=TA_LEFT,
        textColor=BLACK,
        spaceBefore=10,
        spaceAfter=4,
    ))
    add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        firstLineIndent=1.25 * cm,
        alignment=TA_JUSTIFY,
        textColor=BLACK,
        spaceAfter=6,
    ))
    add(ParagraphStyle(
        name="BodyItalic",
        parent=styles["Body"],
        fontName="Helvetica-Oblique",
    ))
    add(ParagraphStyle(
        name="Bullet",
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        leftIndent=18,
        bulletIndent=6,
        alignment=TA_LEFT,
        textColor=BLACK,
        spaceAfter=2,
    ))
    add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=9.5,
        leading=12.5,
        alignment=TA_LEFT,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="TableCellCenter",
        parent=styles["TableCell"],
        alignment=TA_CENTER,
    ))
    add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        textColor=BLACK,
    ))
    add(ParagraphStyle(
        name="BMCHeader",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        textColor=WHITE,
    ))
    add(ParagraphStyle(
        name="EAPBox",
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=EAP_TEXT,
    ))
    add(ParagraphStyle(
        name="Note",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
    ))
    return styles


# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------


def footer_canvas(canvas: canvas_mod.Canvas, doc):
    """ABNT NBR 14724 pagination: arabic numeral in the upper-right corner,
    2 cm from the top and right edges. All pages from the title page are
    counted, but the number is shown only from the first textual page
    (Introdução / Seção 1). The cover is not counted."""
    canvas.saveState()
    phys = canvas.getPageNumber()
    page_num = phys - 1  # cover = physical page 1, not counted
    first = getattr(doc, "first_textual_page", 999)
    if phys >= first and page_num >= 1:
        width, height = canvas._pagesize
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(BLACK)
        canvas.drawRightString(width - 2 * cm, height - 2 * cm + 0.05 * cm, str(page_num))
    canvas.restoreState()


def cover_canvas(canvas: canvas_mod.Canvas, doc):
    """Cover has no footer."""
    return None


# ----------------------------------------------------------------------------
# Custom flowables
# ----------------------------------------------------------------------------


class EAPDiagram(Flowable):
    """Estrutura Analítica do Projeto FastInBox - hierarchical WBS.

    Layout (root + 3 main branches):
        Projeto FastInBox
        |- Documentação  -> Negócio (BMC, Visão), Projeto (Plano, Sprints),
        |                   Arquitetura (UML, ERS, BD), Termos Legais
        |- Produto       -> Requisitos, Protótipo (Figma), Codificação,
        |                   Testes (Internos, Alfa, Beta), Publicação
        |                   Codificação -> Front-end Web, Back-end API
        |- Marketing     -> Planejamento, Vídeo demo, Insights e métricas
    """

    LEAF_W = 4.4 * cm
    LEAF_H = 0.78 * cm
    SUB_W = 4.0 * cm
    BRANCH_W = 4.2 * cm
    BRANCH_H = 0.85 * cm
    ROOT_W = 5.4 * cm
    ROOT_H = 0.95 * cm
    LEAF_GAP = 1.0 * cm
    LINE_COLOR = colors.HexColor("#5A6B7A")

    def __init__(self, available_width=None, available_height=None):
        super().__init__()
        self.width = available_width or (CONTENT_W_L)
        self.height = available_height or 13 * cm

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def _box(self, c, x, y, w, h, label, font_size=9.5):
        c.setFillColor(EAP_BOX)
        c.setStrokeColor(EAP_BOX)
        c.roundRect(x, y, w, h, 2.5, fill=1, stroke=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica", font_size)
        c.drawCentredString(x + w / 2, y + h / 2 - font_size / 3, label)

    def _stub_line(self, c, x1, y1, x2, y2):
        c.setStrokeColor(self.LINE_COLOR)
        c.setLineWidth(0.7)
        c.line(x1, y1, x2, y2)

    def _draw_subtree(self, c, trunk_x, branch_top_y, leaves, leaf_x_start):
        """Draw a vertical trunk with horizontal stubs to each leaf.

        The trunk is at trunk_x, leaves' left edge starts at leaf_x_start.
        Each leaf entry is either a string (simple leaf) or a tuple
        (label, [sub_labels]) for a leaf with children.

        Returns the y-coordinate of the bottom of the last leaf drawn
        (useful for the caller to know where to continue).
        """
        leaf_y = branch_top_y - self.LEAF_GAP
        last_center_y = None
        for entry in leaves:
            if isinstance(entry, tuple):
                label, sub_labels = entry
            else:
                label = entry
                sub_labels = None

            # Draw leaf box
            self._box(c, leaf_x_start, leaf_y, self.LEAF_W, self.LEAF_H, label)
            cy = leaf_y + self.LEAF_H / 2
            # horizontal stub from trunk to leaf left edge
            self._stub_line(c, trunk_x, cy, leaf_x_start, cy)
            last_center_y = cy

            if sub_labels:
                # sub-trunk drops from leaf bottom-center
                sub_trunk_x = leaf_x_start + self.LEAF_W / 2
                sub_leaf_x = leaf_x_start + self.LEAF_W + 0.4 * cm
                sub_y = leaf_y - self.LEAF_GAP
                last_sub_center_y = None
                for sub in sub_labels:
                    self._box(c, sub_leaf_x, sub_y, self.SUB_W, self.LEAF_H, sub, font_size=9)
                    scy = sub_y + self.LEAF_H / 2
                    self._stub_line(c, sub_trunk_x, scy, sub_leaf_x, scy)
                    last_sub_center_y = scy
                    sub_y -= self.LEAF_GAP
                # sub-trunk vertical line: from leaf bottom to last sub center
                self._stub_line(
                    c,
                    sub_trunk_x,
                    leaf_y,
                    sub_trunk_x,
                    last_sub_center_y,
                )
                # advance leaf_y past the sub-tree
                leaf_y = sub_y
            else:
                leaf_y -= self.LEAF_GAP

        return last_center_y

    def draw(self):
        c = self.canv
        W = self.width
        H = self.height

        # ------- root -------
        root_x = (W - self.ROOT_W) / 2
        root_y = H - self.ROOT_H
        root_cx = root_x + self.ROOT_W / 2
        self._box(c, root_x, root_y, self.ROOT_W, self.ROOT_H, "Projeto FastInBox", font_size=10.5)

        # ------- 3 branches in a row -------
        # Fixed positions to avoid collisions:
        # Doc has leaves on the LEFT of its trunk (uses left strip).
        # Produto has leaves on RIGHT and sub-leaves further RIGHT (needs the
        # most horizontal space, sits in the middle).
        # Marketing has leaves on the LEFT of its trunk (uses right strip).
        branch_centers_x = [
            6.0 * cm,                # Documentação
            12.5 * cm,               # Produto
            W - 2.5 * cm,            # Marketing (anchored to right edge)
        ]
        branch_y = root_y - 1.4 * cm

        # Horizontal bus from root to all branches
        bus_y = root_y - 0.55 * cm
        # vertical from root bottom to bus
        self._stub_line(c, root_cx, root_y, root_cx, bus_y)
        # horizontal bus across branches
        self._stub_line(c, branch_centers_x[0], bus_y, branch_centers_x[2], bus_y)

        branches = [
            ("Documentação", branch_centers_x[0]),
            ("Produto", branch_centers_x[1]),
            ("Marketing", branch_centers_x[2]),
        ]
        for label, bcx in branches:
            bx = bcx - self.BRANCH_W / 2
            self._box(c, bx, branch_y, self.BRANCH_W, self.BRANCH_H, label, font_size=10.5)
            # vertical from bus to branch top
            self._stub_line(c, bcx, bus_y, bcx, branch_y + self.BRANCH_H)

        # ------- leaves under each branch -------
        # Trunk x for each branch is the branch center; leaves are placed to
        # the right of the trunk so the trunk never crosses any leaf box.
        # Documentação: simple list (no sub-leaves)
        doc_leaves = [
            "Negócio (BMC, Visão)",
            "Projeto (Plano, Sprints)",
            "Arquitetura (UML, ERS, BD)",
            "Termos Legais",
        ]
        doc_branch_top_y = branch_y
        doc_trunk_x = branch_centers_x[0]
        doc_leaf_x = doc_trunk_x - self.LEAF_W - 0.6 * cm  # leaves on the LEFT of trunk
        # adjust: place leaves to the LEFT for first branch (uses left half of canvas),
        # and stub goes from trunk to leaf RIGHT edge
        doc_last = None
        ly = doc_branch_top_y - self.LEAF_GAP
        for label in doc_leaves:
            self._box(c, doc_leaf_x, ly, self.LEAF_W, self.LEAF_H, label)
            cy = ly + self.LEAF_H / 2
            self._stub_line(c, doc_trunk_x, cy, doc_leaf_x + self.LEAF_W, cy)
            doc_last = cy
            ly -= self.LEAF_GAP
        # vertical trunk for Documentação
        self._stub_line(c, doc_trunk_x, doc_branch_top_y, doc_trunk_x, doc_last)

        # Produto: leaves on the RIGHT, with Codificação having sub-leaves
        prod_leaves = [
            "Requisitos (RF, RNF, RNB)",
            "Protótipo (Figma)",
            (
                "Codificação",
                ["Front-end Web (Next.js)", "Back-end API (NestJS)"],
            ),
            "Testes (Internos, Alfa, Beta)",
            "Publicação e CI/CD",
        ]
        prod_branch_top_y = branch_y
        prod_trunk_x = branch_centers_x[1]
        prod_leaf_x = prod_trunk_x + 0.6 * cm
        ly = prod_branch_top_y - self.LEAF_GAP
        prod_last = None
        for entry in prod_leaves:
            if isinstance(entry, tuple):
                label, sub_labels = entry
            else:
                label, sub_labels = entry, None
            self._box(c, prod_leaf_x, ly, self.LEAF_W, self.LEAF_H, label)
            cy = ly + self.LEAF_H / 2
            self._stub_line(c, prod_trunk_x, cy, prod_leaf_x, cy)
            prod_last = cy

            if sub_labels:
                # sub-trunk drops from leaf BOTTOM-CENTER
                sub_trunk_x = prod_leaf_x + self.LEAF_W / 2
                sub_leaf_x = prod_leaf_x + self.LEAF_W + 0.5 * cm
                sub_y = ly - self.LEAF_GAP
                last_sub_cy = None
                for sub in sub_labels:
                    self._box(c, sub_leaf_x, sub_y, self.SUB_W, self.LEAF_H, sub, font_size=9)
                    scy = sub_y + self.LEAF_H / 2
                    self._stub_line(c, sub_trunk_x, scy, sub_leaf_x, scy)
                    last_sub_cy = scy
                    sub_y -= self.LEAF_GAP
                self._stub_line(c, sub_trunk_x, ly, sub_trunk_x, last_sub_cy)
                ly = sub_y
            else:
                ly -= self.LEAF_GAP
        # vertical trunk for Produto
        self._stub_line(c, prod_trunk_x, prod_branch_top_y, prod_trunk_x, prod_last)

        # Marketing: leaves on the LEFT of trunk (mirrors Documentação on the
        # right side of the canvas).
        mkt_leaves = [
            "Planejamento (Estratégia)",
            "Vídeo demo (apresentação)",
            "Insights e métricas",
        ]
        mkt_branch_top_y = branch_y
        mkt_trunk_x = branch_centers_x[2]
        mkt_leaf_x = mkt_trunk_x - self.LEAF_W - 0.6 * cm
        ly = mkt_branch_top_y - self.LEAF_GAP
        mkt_last = None
        for label in mkt_leaves:
            self._box(c, mkt_leaf_x, ly, self.LEAF_W, self.LEAF_H, label)
            cy = ly + self.LEAF_H / 2
            self._stub_line(c, mkt_trunk_x, cy, mkt_leaf_x + self.LEAF_W, cy)
            mkt_last = cy
            ly -= self.LEAF_GAP
        self._stub_line(c, mkt_trunk_x, mkt_branch_top_y, mkt_trunk_x, mkt_last)


class DBSchemaDiagram(Flowable):
    """ER-style hierarchical schema diagram with orthogonal routing."""

    def __init__(self, available_width=None, height=15 * cm):
        super().__init__()
        self.width = available_width or (CONTENT_W)
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def _table(self, c, x, y, w, h, title, fields, font_size=8):
        # Header bar
        c.setFillColor(colors.HexColor("#1F4E79"))
        c.setStrokeColor(colors.HexColor("#1F4E79"))
        c.rect(x, y + h - 0.6 * cm, w, 0.6 * cm, fill=1, stroke=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + w / 2, y + h - 0.42 * cm, title)
        # Body
        c.setFillColor(WHITE)
        c.setStrokeColor(BLACK)
        c.setLineWidth(0.6)
        c.rect(x, y, w, h - 0.6 * cm, fill=1, stroke=1)
        c.setFillColor(BLACK)
        c.setFont("Helvetica", font_size)
        ty = y + h - 0.9 * cm
        for f in fields:
            c.drawString(x + 0.18 * cm, ty, f)
            ty -= 0.34 * cm

    def draw(self):
        c = self.canv
        W = self.width
        H = self.height

        # ----- Layout: 4 hierarchical rows -----
        # Row A (top):    users
        # Row B:          clinics, patients, audit_log
        # Row C:          orders
        # Row D (bottom): order_items, payments, production_events, commissions

        gap_x = 0.35 * cm
        gap_y = 1.0 * cm
        row_h = 2.85 * cm

        users_w = 5.5 * cm
        users_x = (W - users_w) / 2
        users_y = H - row_h

        rowB_y = users_y - gap_y - row_h
        rowB_n = 3
        rowB_w = (W - (rowB_n - 1) * gap_x) / rowB_n

        orders_w = 6.0 * cm
        orders_x = (W - orders_w) / 2
        orders_y = rowB_y - gap_y - row_h

        rowD_y = orders_y - gap_y - row_h
        rowD_n = 4
        rowD_w = (W - (rowD_n - 1) * gap_x) / rowD_n

        tables = {
            "users": (users_x, users_y, users_w, row_h, "users",
                      ["PK user_id (UUID)", "email", "password_hash",
                       "role (ENUM)", "created_at"], 8.5),
            "clinics": (0, rowB_y, rowB_w, row_h, "clinics",
                        ["PK clinic_id (UUID)", "FK owner_user_id",
                         "name, brand_logo", "white_label_settings"], 8.5),
            "patients": (rowB_w + gap_x, rowB_y, rowB_w, row_h, "patients",
                         ["PK patient_id (UUID)", "FK nutritionist_id",
                          "name, email, phone", "restrictions, address"], 8.5),
            "audit_log": (2 * (rowB_w + gap_x), rowB_y, rowB_w, row_h, "audit_log",
                          ["PK audit_id (UUID)", "FK actor_user_id",
                           "entity, action", "payload (JSONB), created_at"], 8.5),
            "orders": (orders_x, orders_y, orders_w, row_h, "orders",
                       ["PK order_id (UUID)", "UQ order_code",
                        "FK patient_id, FK clinic_id",
                        "status, total, delivery_date"], 8.5),
            "order_items": (0, rowD_y, rowD_w, row_h, "order_items",
                            ["PK order_item_id (UUID)", "FK order_id",
                             "ingredients, packaging",
                             "quantity, unit_price"], 7.8),
            "payments": (rowD_w + gap_x, rowD_y, rowD_w, row_h, "payments",
                         ["PK payment_id (UUID)", "FK order_id",
                          "method, payment_status",
                          "approved_at, gateway_ref"], 7.8),
            "production_events": (2 * (rowD_w + gap_x), rowD_y, rowD_w, row_h,
                                  "production_events",
                                  ["PK production_event_id (UUID)",
                                   "FK order_id, FK actor_id",
                                   "status (ENUM)", "created_at"], 7.6),
            "commissions": (3 * (rowD_w + gap_x), rowD_y, rowD_w, row_h,
                            "commissions",
                            ["PK commission_id (UUID)",
                             "FK order_id, FK nutritionist_id",
                             "base_value, final_value",
                             "commission_value"], 7.6),
        }

        for name, (x, y, w, h, title, fields, fs) in tables.items():
            self._table(c, x, y, w, h, title, fields, fs)

        # ----- Relationships (child → parent), top-down hierarchy -----
        rels = [
            ("clinics", "users"),
            ("patients", "users"),
            ("audit_log", "users"),
            ("orders", "clinics"),
            ("orders", "patients"),
            ("order_items", "orders"),
            ("payments", "orders"),
            ("production_events", "orders"),
            ("commissions", "orders"),
        ]

        # Pre-compute counts to spread entry/exit points along edges
        parent_count = {}
        child_count = {}
        for ch, pa in rels:
            parent_count[pa] = parent_count.get(pa, 0) + 1
            child_count[ch] = child_count.get(ch, 0) + 1

        parent_idx = {}
        child_idx = {}

        # Group lines by gap (rowB_y, rowC_y, rowD_y) to stagger mid_y per line
        gap_groups = {}
        gap_order = {}
        for ch, pa in rels:
            py = tables[pa][1]
            gap_groups.setdefault(py, []).append((ch, pa))
        gap_track_idx = {key: 0 for key in gap_groups}

        c.setStrokeColor(colors.HexColor("#5A6B7A"))
        c.setLineWidth(0.7)
        c.setLineCap(0)
        c.setLineJoin(0)

        for ch, pa in rels:
            cx, cy, cw, chh, _, _, _ = tables[ch]
            px, py, pw, ph, _, _, _ = tables[pa]

            # Distribute exit points along child top edge
            ci = child_idx.get(ch, 0)
            child_idx[ch] = ci + 1
            ct = child_count[ch]
            x1 = cx + cw * (ci + 1) / (ct + 1)
            y1 = cy + chh

            # Distribute entry points along parent bottom edge
            pi = parent_idx.get(pa, 0)
            parent_idx[pa] = pi + 1
            pt = parent_count[pa]
            x2 = px + pw * (pi + 1) / (pt + 1)
            y2 = py

            # Stagger mid_y per gap to avoid horizontal overlaps
            gi = gap_track_idx[py]
            gap_track_idx[py] += 1
            gn = len(gap_groups[py])
            gap_top = py
            gap_bot = cy + chh
            # Distribute tracks from 30% to 70% of the gap height
            t = (gi + 1) / (gn + 1)
            mid_y = gap_bot + (gap_top - gap_bot) * (0.30 + 0.40 * t)

            # Orthogonal three-segment route
            c.line(x1, y1, x1, mid_y)
            c.line(x1, mid_y, x2, mid_y)
            c.line(x2, mid_y, x2, y2)

            # Small endpoint markers
            r = 0.05 * cm
            c.setFillColor(colors.HexColor("#5A6B7A"))
            c.circle(x1, y1, r, fill=1, stroke=0)
            c.circle(x2, y2, r, fill=1, stroke=0)


# ----------------------------------------------------------------------------
# Helpers to build content blocks
# ----------------------------------------------------------------------------


def styled_table(rows, col_widths, styles, header=True, body_align="LEFT", max_w=None):
    """Build a Table with grid + bold header, mirroring the template look.

    Column widths are proportionally scaled to fit the ABNT content width
    when their sum exceeds it.
    """
    max_w = max_w or CONTENT_W
    total = sum(col_widths)
    if total > max_w:
        factor = max_w / total
        col_widths = [w * factor for w in col_widths]
    paragraph_rows = []
    for r_idx, row in enumerate(rows):
        if header and r_idx == 0:
            paragraph_rows.append(
                [Paragraph(c, styles["TableHeader"]) for c in row]
            )
        else:
            paragraph_rows.append(
                [Paragraph(c, styles["TableCell"]) for c in row]
            )
    t = Table(paragraph_rows, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BLACK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F2F2") if header else WHITE),
    ]))
    return t


def cronograma_table(rows, styles):
    paragraph_rows = [
        [Paragraph("Marco", styles["TableHeader"]), Paragraph("Data", styles["TableHeader"])]
    ]
    for marco, data in rows:
        paragraph_rows.append([Paragraph(marco, styles["TableCell"]), Paragraph(data, styles["TableCell"])])
    t = Table(paragraph_rows, colWidths=[8 * cm, 7 * cm])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BLACK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def bmc_table(data, styles):
    """Render a 3x3 Business Model Canvas with black bars."""
    paragraph_rows = []
    headers_row1 = ["Parcerias Chave", "Atividades Chave", "Recursos Chave"]
    headers_row2 = ["Proposta de Valor", "Relacionamento", "Canais"]
    headers_row3 = ["Clientes", "Estrutura de Custos", "Fontes de Receita"]

    cell_h = [Paragraph(c, styles["BMCHeader"]) for c in headers_row1]
    cell_b = [Paragraph(data["parcerias"], styles["TableCell"]),
              Paragraph(data["atividades"], styles["TableCell"]),
              Paragraph(data["recursos"], styles["TableCell"])]
    cell_h2 = [Paragraph(c, styles["BMCHeader"]) for c in headers_row2]
    cell_b2 = [Paragraph(data["proposta"], styles["TableCell"]),
               Paragraph(data["relacionamento"], styles["TableCell"]),
               Paragraph(data["canais"], styles["TableCell"])]
    cell_h3 = [Paragraph(c, styles["BMCHeader"]) for c in headers_row3]
    cell_b3 = [Paragraph(data["clientes"], styles["TableCell"]),
               Paragraph(data["custos"], styles["TableCell"]),
               Paragraph(data["receita"], styles["TableCell"])]

    rows = [cell_h, cell_b, cell_h2, cell_b2, cell_h3, cell_b3]
    col_w = (CONTENT_W) / 3
    t = Table(rows, colWidths=[col_w] * 3, rowHeights=[0.6 * cm, 4.7 * cm, 0.6 * cm, 4.7 * cm, 0.6 * cm, 4.7 * cm])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, BLACK),
        ("BACKGROUND", (0, 0), (-1, 0), BMC_HEADER),
        ("BACKGROUND", (0, 2), (-1, 2), BMC_HEADER),
        ("BACKGROUND", (0, 4), (-1, 4), BMC_HEADER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def bullet_list(items, styles):
    flow = []
    for item in items:
        flow.append(Paragraph(f"&bull;&nbsp;&nbsp;{item}", styles["Bullet"]))
    return flow


# ----------------------------------------------------------------------------
# ABNT captions (legenda above + fonte below) for illustrations and tables
# ----------------------------------------------------------------------------


def caption(text, styles):
    st = ParagraphStyle(
        name="LegendaCap", parent=styles["Body"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, alignment=TA_LEFT, firstLineIndent=0,
        spaceBefore=6, spaceAfter=2,
    )
    return Paragraph(text, st)


def fonte(text, styles):
    st = ParagraphStyle(
        name="LegendaFonte", parent=styles["Body"], fontName="Helvetica",
        fontSize=10, leading=12, alignment=TA_LEFT, firstLineIndent=0,
        spaceBefore=1, spaceAfter=10,
    )
    return Paragraph(f"Fonte: {text}", st)


# ----------------------------------------------------------------------------
# Pre-textual elements (ABNT NBR 14724): folha de rosto, resumo, abstract,
# listas de ilustrações e tabelas
# ----------------------------------------------------------------------------


def _center_title(text, styles, space_before=0.0):
    st = ParagraphStyle(
        name="PreTitle", parent=styles["Body"], fontName="Helvetica-Bold",
        fontSize=12, leading=18, alignment=TA_CENTER, firstLineIndent=0,
        spaceBefore=space_before, spaceAfter=10,
    )
    return Paragraph(text, st)


def folha_rosto_story(styles):
    story = []
    author_style = ParagraphStyle(
        name="FrAutor", parent=styles["Body"], alignment=TA_CENTER,
        firstLineIndent=0, fontSize=12, leading=18, spaceAfter=2,
    )
    title_style = ParagraphStyle(
        name="FrTitulo", parent=styles["Body"], alignment=TA_CENTER,
        firstLineIndent=0, fontName="Helvetica-Bold", fontSize=14, leading=20,
    )
    subtitle_style = ParagraphStyle(
        name="FrSub", parent=styles["Body"], alignment=TA_CENTER,
        firstLineIndent=0, fontSize=12, leading=16,
    )
    nature_style = ParagraphStyle(
        name="FrNatureza", parent=styles["Body"], alignment=TA_JUSTIFY,
        firstLineIndent=0, leftIndent=7.5 * cm, fontSize=11, leading=15,
    )
    city_style = ParagraphStyle(
        name="FrCidade", parent=styles["Body"], alignment=TA_CENTER,
        firstLineIndent=0, fontSize=12, leading=16,
    )

    story.append(Spacer(1, 0.4 * cm))
    for name in ["Thiago Lucas Alves", "João Vitor Thomas Marra", "Gabriel Pahl"]:
        story.append(Paragraph(name, author_style))

    story.append(Spacer(1, 5.5 * cm))
    story.append(Paragraph("FASTINBOX", title_style))
    story.append(Paragraph(
        "Plataforma white label para pedidos personalizados de marmitas",
        subtitle_style,
    ))

    story.append(Spacer(1, 2.2 * cm))
    story.append(Paragraph(
        "Trabalho apresentado ao curso de Ciência da Computação do Centro "
        "Universitário de Brasília (CEUB), como requisito parcial da "
        "disciplina Projeto Integrador III, sob orientação da Profa. Kadidja "
        "Valéria Reginaldo de Oliveira.",
        nature_style,
    ))

    story.append(Spacer(1, 5.5 * cm))
    story.append(Paragraph("BRASÍLIA", city_style))
    story.append(Paragraph("2026", city_style))
    story.append(PageBreak())
    return story


def resumo_story(styles):
    body = ParagraphStyle(
        name="ResumoBody", parent=styles["Body"], firstLineIndent=0,
        alignment=TA_JUSTIFY, fontSize=12, leading=18, spaceAfter=12,
    )
    kw = ParagraphStyle(
        name="Palavras", parent=body, fontName="Helvetica", spaceAfter=0,
    )
    story = [_center_title("RESUMO", styles)]
    story.append(Paragraph(
        "Este trabalho apresenta o FastInBox, plataforma SaaS <i>white label</i> "
        "desenvolvida no Projeto Integrador III do curso de Ciência da "
        "Computação do Centro Universitário de Brasília para digitalizar a "
        "venda de marmitas personalizadas em clínicas de nutrição. O objetivo "
        "foi conduzir o desenvolvimento integrado de um produto demonstrável e "
        "<i>production-ready</i> que conecta nutricionistas, pacientes, cozinhas "
        "e administração em um fluxo único de pedido, pagamento, produção e "
        "governança. A solução foi construída com Next.js e NestJS sobre "
        "PostgreSQL, aplicando engenharia de requisitos, arquitetura modular e "
        "testes em três camadas, e conduzida por processo ágil <i>Scrum-like</i> "
        "ao longo de cinco sprints. Os resultados consolidam o MVP web "
        "publicado, com 100% de aprovação nos cenários de teste, velocidade "
        "média de 43,4 pontos por sprint, NPS de 66,7 e nenhum defeito "
        "bloqueante em aberto. Conclui-se que o produto valida as hipóteses de "
        "negócio e está apto à continuidade no Projeto Integrador IV.",
        body,
    ))
    story.append(Paragraph(
        "<b>Palavras-chave:</b> plataforma white label; SaaS; nutrição; gestão "
        "ágil; engenharia de software.",
        kw,
    ))
    story.append(PageBreak())

    story.append(_center_title("ABSTRACT", styles))
    story.append(Paragraph(
        "This work presents FastInBox, a white label SaaS platform developed "
        "in the Integrative Project III of the Computer Science program at "
        "Centro Universitário de Brasília to digitize the sale of customized "
        "meal boxes in nutrition clinics. The goal was to conduct the "
        "integrated development of a demonstrable, production-ready product "
        "that connects nutritionists, patients, kitchens and administration in "
        "a single flow of ordering, payment, production and governance. The "
        "solution was built with Next.js and NestJS over PostgreSQL, applying "
        "requirements engineering, modular architecture and three-layer "
        "testing, and was managed through a Scrum-like agile process across "
        "five sprints. The results consolidate the published web MVP, with a "
        "100% pass rate on test scenarios, an average velocity of 43.4 points "
        "per sprint, an NPS of 66.7 and no open blocking defects. We conclude "
        "that the product validates the business hypotheses and is ready to "
        "proceed to Integrative Project IV.",
        body,
    ))
    story.append(Paragraph(
        "<b>Keywords:</b> white label platform; SaaS; nutrition; agile "
        "management; software engineering.",
        kw,
    ))
    story.append(PageBreak())
    return story


def _ref_list(title, entries, styles):
    story = [_center_title(title, styles)]
    item = ParagraphStyle(
        name="ListItem", parent=styles["Body"], firstLineIndent=0,
        fontSize=12, leading=17, alignment=TA_LEFT,
    )
    page = ParagraphStyle(name="ListPage", parent=item, alignment=2)
    rows = [[Paragraph(t, item), Paragraph(p, page)] for t, p in entries]
    t = Table(rows, colWidths=[CONTENT_W - 1.5 * cm, 1.5 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t)
    story.append(PageBreak())
    return story


def lista_figuras_story(styles):
    entries = [
        ("Figura 1 - Estrutura Analítica do Projeto (EAP)", "12"),
        ("Figura 2 - Telas do protótipo de alta fidelidade (Figma)", "24"),
        ("Figura 3 - Diagrama entidade-relacionamento do banco de dados", "27"),
        ("Figura 4 - Capturas do sistema funcional em execução", "30"),
        ("Figura 5 - Cadência das cerimônias Scrum", "38"),
        ("Figura 6 - Painéis administrativos (Sprint #05)", "41"),
        ("Figura 7 - Velocidade da equipe por sprint", "43"),
        ("Figura 8 - Burndown da Sprint 5", "45"),
        ("Figura 9 - WIP médio versus limite por coluna", "47"),
    ]
    return _ref_list("LISTA DE FIGURAS", entries, styles)


def lista_quadros_story(styles):
    entries = [
        ("Quadro 1 - Business Model Canvas do FastInBox", "16"),
        ("Quadro 2 - Análise de cenários por dimensão PEST", "17"),
        ("Quadro 3 - Cronograma de marcos", "20"),
        ("Quadro 4 - Requisitos funcionais", "21"),
        ("Quadro 5 - Requisitos não funcionais", "22"),
        ("Quadro 6 - Matriz de teste e devolutiva", "32"),
        ("Quadro 7 - Histórias de usuário", "33"),
        ("Quadro 8 - Regras de negócio", "37"),
        ("Quadro 9 - Sprint Backlog #05", "38"),
        ("Quadro 10 - Registros das reuniões diárias (Daily Scrum)", "39"),
        ("Quadro 11 - Impedimentos e plano de contingência", "39"),
        ("Quadro 12 - Comparativo de evidências de entrega por sprint", "42"),
        ("Quadro 13 - Quadro-resumo dos indicadores ágeis", "47"),
        ("Quadro 14 - Matriz de rastreabilidade dos requisitos", "48"),
    ]
    return _ref_list("LISTA DE QUADROS", entries, styles)


def lista_tabelas_story(styles):
    entries = [
        ("Tabela 1 - Resultados consolidados dos testes internos", "31"),
        ("Tabela 2 - Velocidade planejada e entregue por sprint", "43"),
        ("Tabela 3 - Tempo de ciclo por sprint", "45"),
        ("Tabela 4 - Taxa de defeitos por camada de teste", "46"),
    ]
    return _ref_list("LISTA DE TABELAS", entries, styles)


# ----------------------------------------------------------------------------
# Document content
# ----------------------------------------------------------------------------


def cover_story(styles):
    story = []
    if LOGO_PATH.exists():
        img = Image(str(LOGO_PATH), width=4.4 * cm, height=2.4 * cm)
        img.hAlign = "CENTER"
        story.append(Spacer(1, 1.2 * cm))
        story.append(img)
    else:
        story.append(Spacer(1, 4 * cm))

    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("CENTRO UNIVERSITÁRIO DE BRASÍLIA", styles["CoverHeader"]))
    story.append(Paragraph(
        "FACULDADE DE TECNOLOGIA E CIÊNCIAS SOCIAIS APLICADAS", styles["CoverHeader"]
    ))
    story.append(Paragraph("CURSO DE CIÊNCIA DA COMPUTAÇÃO", styles["CoverHeader"]))
    story.append(Paragraph(
        'PROJETO INTEGRADOR III - TURMA A',
        styles["CoverHeaderTurma"],
    ))
    story.append(Paragraph(
        "PROFESSORA ORIENTADORA: KADIDJA VALÉRIA REGINALDO DE OLIVEIRA",
        styles["CoverHeaderProf"],
    ))

    story.append(Spacer(1, 2.2 * cm))
    story.append(Paragraph("FASTINBOX", styles["ProjectName"]))
    story.append(Paragraph(
        "Plataforma white label para pedidos personalizados de marmitas",
        styles["StudentName"],
    ))

    story.append(Spacer(1, 1.6 * cm))
    students = [
        "Thiago Lucas Alves",
        "João Vitor Thomas Marra",
        "Gabriel Pahl",
    ]
    for s in students:
        story.append(Paragraph(s, styles["StudentName"]))

    story.append(Spacer(1, 4.5 * cm))
    story.append(Paragraph("BRASÍLIA, 2026", styles["CityDate"]))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    return story


def toc_story(styles):
    story = [Paragraph("SUMÁRIO", styles["TocTitle"])]

    entries = [
        ("1 Descrição do Projeto", "9", True),
        ("1.1 Objetivo", "9", False),
        ("1.2 Descrição", "9", False),
        ("2 Escopo do Projeto (EAP)", "11", True),
        ("3 Problema/Oportunidade", "14", True),
        ("4 Modelo de Negócio (BMC ou SMC)", "16", True),
        ("5 Cenários de Negócio", "17", True),
        ("6 Benefícios da Solução", "18", True),
        ("7 Público Alvo", "18", True),
        ("8 Cronograma de Marcos", "20", True),
        ("9 Requisitos Funcionais", "21", True),
        ("10 Requisitos Não Funcionais", "22", True),
        ("11 Protótipo Visual", "23", True),
        ("12 Requisito dos MVPs", "25", True),
        ("12.1 Aplicativo Móvel", "25", False),
        ("12.2 Web Application", "25", False),
        ("13 Modelo de Dados (Web Application)", "27", True),
        ("14 Resultados de Teste", "29", True),
        ("14.1 Testes Internos", "30", False),
        ("14.2 Testes Fechados", "31", False),
        ("14.3 Testes Beta", "31", False),
        ("14.4 Matriz de Teste e Devolutiva", "31", False),
        ("15 Histórias de Usuário e Critérios de Aceitação", "33", True),
        ("16 Regras de Negócio", "37", True),
        ("17 Governança Ágil e Sprint #05", "38", True),
        ("18 Métricas Ágeis", "43", True),
        ("19 Rastreabilidade dos Requisitos", "48", True),
        ("20 Marketing Digital", "49", True),
        ("21 Conclusão e Próximos Passos", "51", True),
        ("22 Referências", "52", True),
        ("APÊNDICE A - TECNOLOGIAS UTILIZADAS", "54", True),
    ]
    rows = []
    for title, page, is_main in entries:
        style = styles["TocItem"] if is_main else styles["TocSubItem"]
        rows.append([
            Paragraph(title, style),
            Paragraph(page, ParagraphStyle(
                name="tocp", parent=style, alignment=2,
            )),
        ])
    t = Table(rows, colWidths=[14.5 * cm, 1.5 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t)
    story.append(PageBreak())
    return story


def glossary_story(styles):
    story = [_center_title("GLOSSÁRIO E LISTA DE SIGLAS", styles)]
    story.append(Paragraph(
        "<i>Lista, em ordem alfabética, de termos, siglas e acrônimos importantes para a "
        "compreensão do domínio do projeto/produto FastInBox.</i>",
        styles["Body"],
    ))
    items = [
        "<b>BMC</b> - Business Model Canvas, modelo gráfico para descrição da proposta de valor e operação.",
        "<b>CI/CD</b> - Continuous Integration / Continuous Delivery, automação de build, teste e implantação.",
        "<b>EAP</b> - Estrutura Analítica do Projeto, decomposição hierárquica dos pacotes de trabalho.",
        "<b>ERS</b> - Especificação de Requisitos de Software.",
        "<b>HTTPS</b> - Hyper Text Transfer Protocol Secure, protocolo seguro para tráfego web.",
        "<b>IHC</b> - Interação Humano-Computador.",
        "<b>JWT</b> - JSON Web Token, padrão para autenticação em APIs.",
        "<b>MFA</b> - Multi Factor Authentication, autenticação em múltiplos fatores.",
        "<b>MVP</b> - Minimum Viable Product, produto mínimo viável.",
        "<b>NestJS</b> - Framework Node.js para back-end estruturado em módulos.",
        "<b>Next.js</b> - Framework React para aplicações web full-stack.",
        "<b>PEST</b> - Política, Econômica, Social, Tecnológica - técnica de análise de cenários.",
        "<b>RF</b> - Requisito Funcional.",
        "<b>RNF</b> - Requisito Não Funcional.",
        "<b>RNB</b> - Regra de Negócio.",
        "<b>SLA</b> - Service Level Agreement, acordo formal de nível de serviço.",
        "<b>UML</b> - Unified Modeling Language, linguagem unificada de modelagem.",
        "<b>UX</b> - User Experience, experiência do usuário.",
        "<b>White Label</b> - Operação em que a marca exposta ao cliente final é a do parceiro.",
    ]
    story.extend(bullet_list(items, styles))
    story.append(PageBreak())
    return story


def descricao_story(styles):
    story = [Paragraph("1&nbsp;&nbsp;&nbsp;Descrição do Projeto", styles["H1Section"])]

    story.append(Paragraph(
        "O FastInBox é uma plataforma SaaS (<i>Software as a Service</i>) white label "
        "desenvolvida no contexto do Projeto Integrador III do curso de Ciência da "
        "Computação do Centro Universitário de Brasília (CEUB). A solução conecta, em "
        "uma única operação digital, quatro perfis de usuário hoje atendidos por canais "
        "fragmentados: <b>nutricionistas</b> que prescrevem alimentação personalizada, "
        "<b>pacientes</b> que consomem refeições saudáveis, <b>cozinhas parceiras</b> "
        "responsáveis pela produção e entrega, e o <b>administrador</b> da plataforma, "
        "responsável por governança, conciliação financeira e indicadores estratégicos.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "O modelo white label é central à proposta: a marca exposta ao paciente é "
        "sempre a da clínica de nutrição parceira, enquanto o FastInBox atua como "
        "fornecedor de tecnologia em segundo plano. Esse posicionamento preserva o "
        "vínculo de confiança entre o profissional de saúde e o paciente, ao mesmo "
        "tempo em que entrega à clínica uma operação comercial completa - cadastro de "
        "pacientes, montagem de pedido, checkout integrado, fila qualificada da "
        "cozinha, entrega monitorada e relatórios financeiros - sem que ela precise "
        "construir, manter ou sustentar tecnologia própria.",
        styles["Body"],
    ))

    story.append(Paragraph("1.1&nbsp;&nbsp;Objetivo", styles["H2Section"]))
    story.append(Paragraph(
        "Conduzir o desenvolvimento integrado da plataforma FastInBox, aplicando, de "
        "forma acadêmica e profissional, as disciplinas de gestão de projetos e de "
        "engenharia de software para entregar um produto digital white label, "
        "demonstrável, auditável e production-ready, que conecte nutricionistas, "
        "pacientes, cozinhas parceiras e administração em um fluxo único de pedido "
        "personalizado de marmitas, com criação, revisão, pagamento, produção, entrega "
        "e governança rastreáveis. O objetivo secundário é validar, junto a clínicas "
        "parceiras, hipóteses comerciais e operacionais que sustentem a continuidade "
        "do produto após o ciclo acadêmico do Projeto Integrador.",
        styles["Body"],
    ))

    story.append(Paragraph("1.2&nbsp;&nbsp;Descrição", styles["H2Section"]))
    story.append(Paragraph(
        "O projeto FastInBox compreende a elaboração e a publicação do conjunto "
        "completo de artefatos técnicos e de negócio necessários para construir e "
        "validar a plataforma. No eixo de produto, isso inclui o Business Model "
        "Canvas (BMC), o Documento de Visão, a Especificação de Requisitos de "
        "Software (ERS) com 18 requisitos funcionais e 9 requisitos não funcionais, o "
        "Plano de Projeto, a Arquitetura UML, o Esquema de Banco de Dados relacional, "
        "Termos Legais e LGPD, o planejamento e as evidências de cada sprint, os "
        "protótipos de interface em Figma, a implementação do front-end web (Next.js "
        "15 + React 19 + TypeScript), a implementação do back-end em NestJS sobre "
        "Node.js, a modelagem em PostgreSQL 17, a estratégia de testes automatizados "
        "e a estratégia mínima de marketing digital para validação de hipóteses junto "
        "a clínicas e pacientes.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "No eixo de gestão, o projeto entrega cronograma macro, Estrutura Analítica "
        "do Projeto (EAP), matriz RACI, governança por sprints com cerimônias de "
        "planejamento, daily, review e retrospectiva, controle de risco com plano de "
        "contingência e matriz de comunicação. O backlog é mantido em GitHub "
        "Projects, com issues categorizadas por épico, prioridade e perfil de "
        "usuário. A documentação técnica é publicada em GitHub Pages "
        "(<i>fastinbox-repo.github.io/docs/</i>) com deploy automático via GitHub "
        "Actions, garantindo rastreabilidade entre o que está descrito formalmente e "
        "o que está, de fato, em execução no repositório.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Estão sendo exercitadas, ao longo do ciclo, as disciplinas de Engenharia de "
        "Requisitos (com técnicas de elicitação por entrevista, análise documental e "
        "observação), Engenharia de Software (padrões SOLID, Clean Architecture, "
        "modularização por domínio), Banco de Dados (modelagem relacional "
        "normalizada, integridade referencial, índices), Programação Web "
        "(componentização React, App Router, Server Components, API REST), Interação "
        "Humano-Computador (heurísticas de Nielsen, WCAG 2.1 AA, design responsivo), "
        "Gestão de Projetos (PMBOK adaptado a contexto ágil, Scrum-like), Qualidade "
        "de Software (testes unitários, integração e end-to-end) e Empreendedorismo "
        "(modelagem de negócio, validação de hipóteses, métricas de tração). A "
        "entrega final compreende um sistema web responsivo demonstrável, com fluxo "
        "ponta a ponta validado em ambiente público, documentação técnica completa e "
        "uma estrutura de governança preparada para a continuidade do Projeto "
        "Integrador IV.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "A equipe responsável pelo projeto é composta por estudantes do curso de "
        "Ciência da Computação do CEUB com responsabilidades distribuídas conforme "
        "matriz RACI: <b>Thiago Lucas Alves</b> atua como líder de produto, "
        "responsável também por front-end, back-end e QA; <b>João Vitor Thomas "
        "Marra</b> assume DevOps, automação e infraestrutura; <b>Gabriel Pahl</b> é "
        "responsável por design de interface e experiência do usuário. A orientação "
        "acadêmica é da Profa. Kadidja Valéria Reginaldo de Oliveira, que valida "
        "marcos de entrega e revisa a aderência metodológica do projeto.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def eap_story(styles):
    story = [Paragraph("2&nbsp;&nbsp;&nbsp;Escopo do Projeto (EAP)", styles["H1Section"])]
    story.append(Paragraph(
        "<i>Estrutura Analítica do Projeto FastInBox, decompondo o trabalho em "
        "documentação, produto e marketing. Cada nó pai é dividido em pelo menos "
        "dois nós filhos, conforme orientação acadêmica.</i>",
        styles["Body"],
    ))
    # Use NextPageTemplate to render landscape EAP page
    story.append(NextPageTemplate("eap_landscape"))
    story.append(PageBreak())
    story.append(Spacer(1, 0.2 * cm))
    story.append(caption("Figura 1 - Estrutura Analítica do Projeto (EAP)", styles))
    story.append(EAPDiagram(available_width=LAND_W - 4 * cm, available_height=13.0 * cm))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "Estrutura Analítica do Projeto FastInBox decomposta em três pacotes de "
        "trabalho. <b>Documentação</b> reúne os artefatos de negócio (BMC, "
        "Documento de Visão), de projeto (Plano de Projeto, Sprints), de "
        "arquitetura (UML, ERS, Banco de Dados) e os termos legais. "
        "<b>Produto</b> consolida o ciclo de engenharia: requisitos (RF, RNF, "
        "regras de negócio), protótipo em Figma, codificação dividida entre "
        "front-end web (Next.js) e back-end API (NestJS), testes em três "
        "estágios (internos, alfa e beta) e a publicação com CI/CD. "
        "<b>Marketing</b> agrupa o planejamento estratégico, o vídeo demonstrativo "
        "para banca e o acompanhamento de insights e métricas operacionais.",
        styles["Note"],
    ))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    return story


def problema_story(styles):
    story = [Paragraph("3&nbsp;&nbsp;&nbsp;Problema/Oportunidade", styles["H1Section"])]
    story.append(Paragraph(
        "A operação de venda de marmitas personalizadas em clínicas de nutrição e "
        "academias parceiras ainda é majoritariamente manual. Pedidos são coletados "
        "por WhatsApp, ajustes são registrados em planilhas, o pagamento ocorre por "
        "links avulsos e a comunicação com a cozinha depende de mensagens informais. "
        "Esse modelo gera retrabalho, falhas de comunicação, abandono no checkout e "
        "baixa previsibilidade operacional para todos os envolvidos.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Dados públicos reforçam o problema. De acordo com a Associação Brasileira "
        "das Indústrias da Alimentação (ABIA, 2024), o segmento de refeições "
        "saudáveis prontas cresceu mais de 12% ao ano nos últimos cinco anos, e "
        "estima-se mais de 90 mil nutricionistas ativos no Conselho Federal de "
        "Nutricionistas (CFN, 2024). Ao mesmo tempo, pesquisa do SEBRAE (2023) "
        "aponta que 67% dos pequenos negócios do setor de alimentação operam sem "
        "ferramenta digital integrada para pedidos e gestão financeira, "
        "configurando uma lacuna evidente para um produto digital white label.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Do lado do paciente, a Conferência Nacional do Comércio Eletrônico "
        "Brasileiro (Comitê Gestor da Internet, 2024) registra que cerca de 28% "
        "dos abandonos de checkout estão associados à insegurança quanto ao "
        "pagamento e à falta de clareza sobre o produto. No fluxo atual, o "
        "paciente paga por canais externos à clínica, sem revisão formal do "
        "pedido, o que aumenta a fricção e reduz a confiança na compra.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Para a cozinha, a ausência de uma fila qualificada faz com que pedidos "
        "incompletos ou não pagos cheguem à produção, gerando retrabalho, descarte "
        "de insumo e atraso na entrega. Para a administração da clínica, falta "
        "uma visão consolidada de pedidos, pagamentos, produção e comissões, "
        "dificultando a tomada de decisão e o controle financeiro.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "A oportunidade que o FastInBox endereça consiste em consolidar todo esse "
        "fluxo em uma única plataforma white label - na qual a marca da clínica "
        "permanece em primeiro plano - reduzindo operação manual, aumentando a "
        "conversão de pagamento, qualificando a fila operacional da cozinha e "
        "oferecendo governança centralizada. O resultado esperado é maior "
        "previsibilidade, escalabilidade e percepção de valor para os quatro "
        "perfis envolvidos: nutricionista, paciente, cozinha e administrador.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "A janela de oportunidade é reforçada pela aceleração da digitalização do "
        "setor de saúde no pós-pandemia. Pesquisas do IBGE (PNAD-TIC 2023) indicam "
        "que mais de 84% da população urbana adulta utiliza serviços digitais para "
        "pagamento ou compra recorrente, com Pix superando cartões em volume de "
        "transações de baixo valor. O ambiente regulatório também é favorável: a Lei "
        "Geral de Proteção de Dados (LGPD - Lei 13.709/2018) exige tratamento "
        "estruturado de dados de saúde - exatamente o terreno em que uma plataforma "
        "como o FastInBox, com auditoria nativa e segregação por perfil, oferece "
        "vantagem competitiva sobre planilhas e mensagens dispersas. A combinação "
        "desses vetores - demanda crescente por alimentação saudável, baixa adoção "
        "digital no setor, exigência regulatória e maturação dos pagamentos "
        "instantâneos - configura um cenário propício para a entrada do FastInBox "
        "como infraestrutura digital de clínicas nutricionais.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def bmc_story(styles):
    story = [Paragraph("4&nbsp;&nbsp;&nbsp;Modelo de Negócio (BMC ou SMC)", styles["H1Section"])]
    story.append(Paragraph(
        "O modelo de negócio do FastInBox foi estruturado segundo o Business Model "
        "Canvas (BMC) de Osterwalder e Pigneur (2010), instrumento amplamente "
        "adotado na engenharia de software empreendedora para descrever, de forma "
        "visual e integrada, como uma organização cria, entrega e captura valor. "
        "Os nove blocos a seguir consolidam as definições estratégicas validadas "
        "pela equipe junto a clínicas parceiras durante a fase de descoberta do "
        "projeto e servem de base tanto para o backlog de produto quanto para a "
        "estratégia de validação de hipóteses no MVP.",
        styles["Body"],
    ))
    data = {
        "parcerias": (
            "Clínicas de nutrição e nutricionistas autônomos.<br/>"
            "Cozinhas parceiras de produção e entrega.<br/>"
            "Gateway de pagamento integrado.<br/>"
            "Hospedagem (Vercel, Railway).<br/>"
            "Provedores de banco de dados (PostgreSQL gerenciado)."
        ),
        "atividades": (
            "Desenvolvimento e evolução da plataforma web.<br/>"
            "Onboarding de clínicas e cozinhas parceiras.<br/>"
            "Operação de checkout e conciliação financeira.<br/>"
            "Suporte técnico e operacional.<br/>"
            "Governança de dados, auditoria e segurança."
        ),
        "recursos": (
            "Equipe de produto, design e engenharia.<br/>"
            "Plataforma web Next.js + NestJS.<br/>"
            "Banco relacional e infraestrutura cloud.<br/>"
            "Marca FastInBox e identidade white label.<br/>"
            "Documentação técnica pública."
        ),
        "proposta": (
            "Plataforma white label que permite ao nutricionista vender marmitas "
            "personalizadas com sua própria marca, ao paciente revisar e pagar com "
            "segurança e à cozinha receber apenas pedidos válidos e pagos. "
            "Reduz operação manual, aumenta a conversão do checkout e oferece "
            "rastreabilidade ponta a ponta."
        ),
        "relacionamento": (
            "Onboarding guiado para clínicas.<br/>"
            "Suporte por canal digital.<br/>"
            "Comunicação transacional automatizada.<br/>"
            "Painel de autoatendimento por perfil."
        ),
        "canais": (
            "Aplicação web responsiva (desktop, tablet, mobile).<br/>"
            "Landing page do paciente acessada por código único.<br/>"
            "Painel da clínica e da cozinha.<br/>"
            "Documentação pública via GitHub Pages."
        ),
        "clientes": (
            "Nutricionistas e clínicas parceiras (cliente direto).<br/>"
            "Pacientes finais (consumidor da marmita).<br/>"
            "Cozinhas parceiras (operação).<br/>"
            "Administração FastInBox (governança)."
        ),
        "custos": (
            "Infraestrutura cloud e observabilidade.<br/>"
            "Manutenção de gateway de pagamento.<br/>"
            "Evolução do produto (engenharia, design, QA).<br/>"
            "Suporte e operação comercial."
        ),
        "receita": (
            "Comissão progressiva por pedido processado.<br/>"
            "Plano de assinatura por volume de pedidos.<br/>"
            "Serviços premium de analytics e previsão operacional.<br/>"
            "Onboarding pago para clínicas de maior porte."
        ),
    }
    story.append(caption("Quadro 1 - Business Model Canvas do FastInBox", styles))
    story.append(bmc_table(data, styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026), adaptado de Osterwalder e Pigneur (2010).", styles))
    story.append(PageBreak())
    return story


def cenarios_beneficios_publico_story(styles):
    story = [Paragraph("5&nbsp;&nbsp;&nbsp;Cenários de Negócio", styles["H1Section"])]
    story.append(Paragraph(
        "A análise de cenários combina os métodos PEST (Política, Econômica, "
        "Social, Tecnológica) e a leitura prospectiva pessimista/realista/otimista "
        "recomendada pela literatura de planejamento estratégico (Schwartz, 1996). "
        "O objetivo é identificar oportunidades e riscos exógenos que afetam "
        "diretamente a viabilidade do FastInBox e estruturar hipóteses sobre como "
        "o produto se comporta em cada configuração de futuro. As fontes "
        "consultadas incluem ABIA, IBGE, SEBRAE, CFN, Datafolha, Gartner, CGI.br, "
        "Banco Mundial, McKinsey e relatórios setoriais públicos. Os três cenários "
        "abaixo indicam o intervalo de variação esperado para os próximos 24 meses "
        "e orientam decisões de produto, precificação e roadmap.",
        styles["Body"],
    ))

    rows = [
        ["Dimensão", "Pessimista", "Realista", "Otimista"],
        [
            "Política",
            "Aumento de carga regulatória sobre alimentação saudável e "
            "exigência de notas fiscais detalhadas eleva custo de operação "
            "informal.",
            "Manutenção do marco regulatório atual com ANVISA e PROCON, "
            "incentivos pontuais a pequenas operações.",
            "Políticas públicas de incentivo à alimentação saudável e "
            "digitalização dos pequenos negócios reforçam adoção de "
            "plataformas como o FastInBox.",
        ],
        [
            "Econômica",
            "Inflação de insumos pressiona ticket médio e reduz margem "
            "do nutricionista (IBGE, 2024).",
            "Crescimento estável do segmento de alimentação saudável pronta "
            "(ABIA, 2024) - 6 a 8% ao ano - mantendo demanda.",
            "Expansão acelerada de serviços por assinatura e crescimento de "
            "12% ao ano (ABIA, 2024) ampliam mercado endereçável.",
        ],
        [
            "Social",
            "Resistência cultural à digitalização de pequenas clínicas "
            "limita adesão inicial.",
            "Nutricionistas com perfil digital médio adotam ferramentas que "
            "reduzem operação manual quando há ganho claro.",
            "Forte busca por alimentação saudável e personalizada (Datafolha, "
            "2024) impulsiona adesão de pacientes e clínicas.",
        ],
        [
            "Tecnológica",
            "Custo de manutenção e segurança cresce mais rápido que receita; "
            "incidentes com gateway elevam atrito.",
            "Gateways nacionais consolidados (Mercado Pago, Pagar.me, "
            "Stripe) reduzem barreira técnica para checkout integrado.",
            "Maturidade de cloud, IA generativa para suporte e dashboards "
            "(Gartner, 2025) habilitam diferenciação do FastInBox como "
            "plataforma SaaS.",
        ],
    ]
    col_w = [3 * cm, 4.4 * cm, 4.4 * cm, 4.2 * cm]
    story.append(caption("Quadro 2 - Análise de cenários por dimensão PEST", styles))
    story.append(styled_table(rows, col_w, styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026), com base em ABIA, IBGE, SEBRAE, CFN, Datafolha e Gartner.", styles))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("6&nbsp;&nbsp;&nbsp;Benefícios da Solução", styles["H1Section"]))
    story.append(Paragraph(
        "Os benefícios da plataforma são organizados por perfil de usuário e "
        "alinhados ao princípio de que cada persona deve perceber valor próprio "
        "e mensurável já no MVP. A abordagem segue a recomendação de Caroli "
        "(2018) para MVP Canvas, segundo a qual o produto mínimo viável precisa "
        "entregar valor relevante e validável a cada lado da rede de usuários "
        "para sustentar adoção real, e não apenas demonstração.",
        styles["Body"],
    ))
    benefits = [
        "<b>Para o nutricionista:</b> redução estimada de até 70% no tempo de "
        "criação de pedido (de uma média de 12 minutos via WhatsApp para até "
        "3 minutos no FastInBox), controle visual da carteira de pacientes em "
        "uma única tela, identidade visual da clínica preservada em todos os "
        "pontos de contato (white label), comissão progressiva rastreável por "
        "pedido e relatórios financeiros mensais exportáveis.",
        "<b>Para o paciente:</b> jornada clara iniciada por código único enviado "
        "pelo nutricionista, revisão do pedido sem ambiguidade (ingredientes, "
        "embalagem, observações nutricionais e valor consolidado), checkout "
        "integrado sem redirecionamento externo - reduzindo o atrito que, "
        "segundo o CGI.br (2024), responde por cerca de 28% dos abandonos no "
        "comércio eletrônico - e acompanhamento de status em tempo real.",
        "<b>Para a cozinha:</b> fila operacional contendo apenas pedidos pagos "
        "e validados, eliminando o retrabalho com pedidos cancelados; "
        "informações nutricionais completas e leitura escaneável; atualização "
        "de status com trilha de auditoria; consolidação automática por janela "
        "de entrega para otimização logística.",
        "<b>Para a administração:</b> dashboard centralizado com indicadores "
        "comerciais (volume de pedidos, ticket médio, taxa de conversão), "
        "financeiros (faturamento, comissões, conciliação por gateway) e "
        "operacionais (tempo médio em produção, taxa de entrega, incidentes); "
        "suporte completo à auditoria por trilha de eventos sensíveis; "
        "governança multi-perfil com segregação de acessos por papel.",
        "<b>Para o ecossistema:</b> redução de custos com retrabalho e descarte "
        "de insumos, aumento da previsibilidade operacional, base de dados "
        "estruturada para evoluir com previsão de demanda baseada em histórico "
        "e conciliação financeira automatizada com gateways de pagamento.",
    ]
    story.extend(bullet_list(benefits, styles))

    story.append(Paragraph("7&nbsp;&nbsp;&nbsp;Público Alvo", styles["H1Section"]))
    story.append(Paragraph(
        "O público-alvo do FastInBox foi modelado em quatro personas, derivadas "
        "de entrevistas semiestruturadas com nutricionistas e pacientes reais "
        "durante a fase de descoberta, complementadas por dados secundários do "
        "Conselho Federal de Nutricionistas (CFN), do SEBRAE e da Datafolha. As "
        "personas são utilizadas pela equipe como referência permanente em "
        "decisões de design, priorização de backlog e validação de hipóteses, "
        "conforme a metodologia de Cooper, Reimann e Cronin (2014).",
        styles["Body"],
    ))
    publico = [
        "<b>Dra. Mariana Alves - Nutricionista Parceira (persona primária):</b> "
        "34 anos, especialização em nutrição esportiva, atende em consultório "
        "próprio em Brasília-DF e atualmente possui carteira ativa de "
        "aproximadamente 80 pacientes. Familiaridade digital média a alta, "
        "utiliza Google Agenda, WhatsApp Business e planilhas. Suas dores são "
        "o excesso de etapas manuais para concluir um pedido, o risco de erro "
        "ao transcrever dados entre canais e a dificuldade de acompanhar "
        "status sem entrar em contato com cozinha. Seu critério de sucesso é "
        "concluir um pedido seguro em poucos minutos preservando a marca da "
        "clínica e tendo visão clara da comissão.",
        "<b>Camila Rocha - Paciente Final (persona secundária):</b> 29 anos, "
        "profissional de marketing, rotina intensa entre escritório e "
        "compromissos pessoais. Acessa serviços majoritariamente pelo "
        "smartphone (Android), valoriza conveniência, transparência e "
        "segurança no pagamento. Suas dores são receio de erro no pedido, "
        "desconfiança em fluxos pouco profissionais e dificuldade com "
        "interfaces poluídas. Seu critério de sucesso é revisar a marmita sem "
        "ajuda, pagar com confiança em até dois minutos e acompanhar a "
        "entrega no dia D.",
        "<b>Juliana Santos - Operadora de Cozinha (persona operacional):</b> "
        "38 anos, líder de produção em cozinha parceira que processa em "
        "média 120 pedidos/dia. Opera sob pressão de tempo, utiliza "
        "principalmente desktop e tablet em ambiente operacional. Suas "
        "dores são interfaces sobrecarregadas, risco de perder detalhes "
        "nutricionais críticos e dificuldade em distinguir prioridades. Seu "
        "critério de sucesso é localizar o pedido correto rapidamente e "
        "executar a operação com mínima ambiguidade.",
        "<b>Fernanda Lima - Administradora FastInBox (persona de governança):</b> "
        "41 anos, perfil de gestora de operação SaaS, orientada a "
        "indicadores e governança. Necessita consolidar várias fontes de "
        "informação em painéis confiáveis, identificar gargalos operacionais "
        "e ajustar regras de comissão e janelas de entrega. Suas dores são "
        "falta de visão centralizada e baixa rastreabilidade. Seu critério "
        "de sucesso é responder rapidamente o que está atrasado e tomar "
        "decisões baseadas em dados.",
    ]
    story.extend(bullet_list(publico, styles))
    story.append(PageBreak())
    return story


def cronograma_story(styles):
    story = [Paragraph("8&nbsp;&nbsp;&nbsp;Cronograma de Marcos", styles["H1Section"])]
    story.append(Paragraph(
        "O cronograma macro do FastInBox segue um modelo incremental orientado a "
        "risco, distribuído em sprints de duas a três semanas dentro do semestre "
        "letivo de 2026/1, com fechamento previsto para 31 de julho de 2026. Cada "
        "marco (M1 a M8) corresponde a uma entrega verificável, com critérios de "
        "aceite explícitos, evidências documentais (commit, deploy ou print de "
        "execução) e revisão orientada pela professora orientadora. O cronograma "
        "detalhado de atividades é mantido no GitHub Project da organização "
        "(<i>github.com/orgs/fastinbox-repo/projects</i>), com sincronização "
        "diária do status das issues. A tabela a seguir consolida os marcos "
        "principais.",
        styles["Body"],
    ))
    rows = [
        ("M1 - Kickoff e definição de escopo (BMC, Visão, ERS)", "26/02/2026"),
        ("M2 - Entrega Sprint 1 - MVP navegável publicado", "10/04/2026"),
        ("M3 - Entrega Sprint 2 - Persistência + smoke tests", "08/05/2026"),
        ("M4 - Entrega Sprint 3 - Pagamento integrado + auditoria", "05/06/2026"),
        ("M5 - Entrega Sprint 4 - Dashboard administrativo", "26/06/2026"),
        ("M6 - Testes Internos consolidados (PI III)", "10/07/2026"),
        ("M7 - Apresentação acadêmica do Projeto Integrador III", "24/07/2026"),
        ("M8 - Hardening e backlog de evolução para PI IV", "31/07/2026"),
    ]
    story.append(caption("Quadro 3 - Cronograma de marcos", styles))
    story.append(cronograma_table(rows, styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(PageBreak())
    return story


def requisitos_funcionais_story(styles):
    story = [Paragraph("9&nbsp;&nbsp;&nbsp;Requisitos Funcionais", styles["H1Section"])]
    story.append(Paragraph(
        "Os requisitos funcionais (RF) descrevem o que o sistema FastInBox deve "
        "fazer, segundo a definição clássica de Sommerville (2019). A elicitação "
        "foi realizada por entrevistas com nutricionistas e cozinhas parceiras, "
        "análise de fluxos atuais (WhatsApp, planilhas) e benchmark com soluções "
        "comerciais. Cada RF possui código único, descrição objetiva, "
        "rastreabilidade ao perfil de usuário primário e dependência mapeada a "
        "regras de negócio (RNB-001 a RNB-007) e a requisitos não funcionais. A "
        "tabela a seguir lista os 14 RFs prioritários para o MVP do Projeto "
        "Integrador III; outros 4 RFs (RF015 a RF018, relacionados a planos "
        "recorrentes, autoatendimento, previsão de demanda e conciliação "
        "financeira) estão na ERS completa e foram mapeados para o Projeto "
        "Integrador IV.",
        styles["Body"],
    ))
    rfs = [
        ("RF001", "Permitir autenticação por e-mail e senha, com recuperação segura, segregada por perfil (nutricionista, paciente, cozinha, administrador)."),
        ("RF002", "Permitir o cadastro e a edição de pacientes vinculados ao nutricionista autenticado."),
        ("RF003", "Permitir ao nutricionista criar pedido de marmitas com múltiplos itens, embalagem e comissão, gerando código único de acesso."),
        ("RF004", "Permitir configurar a identidade visual da clínica (logotipo e parâmetros visuais) para operação white label."),
        ("RF005", "Permitir ao paciente acessar o pedido pela landing page mediante código único recebido."),
        ("RF006", "Permitir ao paciente revisar, editar (quando permitido) e confirmar o pedido antes do pagamento."),
        ("RF007", "Integrar checkout seguro e nativo para pagamento do pedido sem redirecionamento externo."),
        ("RF008", "Disponibilizar perfil do paciente com dados, histórico e acompanhamento de status."),
        ("RF009", "Disponibilizar painel da cozinha em tempo real com pedidos pagos e suas informações operacionais."),
        ("RF010", "Permitir a atualização auditável de status operacionais (em produção, pronto, em entrega, entregue)."),
        ("RF011", "Disponibilizar dashboard administrativo para gestão de usuários, pedidos, transações e regras."),
        ("RF012", "Permitir a administração de cozinhas e parceiros operacionais."),
        ("RF013", "Calcular e registrar a comissão progressiva por pedido (valor base x valor final)."),
        ("RF014", "Registrar trilha de auditoria de eventos sensíveis (login, pagamento, mudança de status)."),
    ]
    rows = [["Código", "Descrição"]]
    rows.extend([[c, d] for c, d in rfs])
    story.append(caption("Quadro 4 - Requisitos funcionais", styles))
    story.append(styled_table(rows, [2.4 * cm, 13.6 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(PageBreak())
    return story


def requisitos_nao_funcionais_story(styles):
    story = [Paragraph("10&nbsp;&nbsp;Requisitos Não Funcionais", styles["H1Section"])]
    story.append(Paragraph(
        "Os requisitos não funcionais (RNF) definem características de qualidade "
        "que o FastInBox deve apresentar, classificados conforme a norma "
        "ISO/IEC 25010 (Pressman e Maxim, 2021). Eles são tratados como "
        "restrições arquiteturais e direcionam decisões de tecnologia, "
        "infraestrutura e processo. A aderência a cada RNF é validada por "
        "métricas objetivas (tempos de resposta, cobertura de testes, "
        "compatibilidade de navegadores) acompanhadas continuamente ao longo das "
        "sprints. A tabela abaixo apresenta os 9 RNFs aplicáveis ao MVP.",
        styles["Body"],
    ))
    rnfs = [
        ("RNF001", "Performance",
         "Página inicial responde em até 3 segundos em condições normais; APIs críticas com latência mediana abaixo de 500 ms."),
        ("RNF002", "Usabilidade",
         "Layout responsivo (mobile, tablet, desktop) com aderência a diretrizes WCAG 2.1 AA e fluxo guiado por perfil."),
        ("RNF003", "Segurança",
         "Senhas armazenadas com hashing + salt; tráfego sob HTTPS; suporte a MFA para perfis administrativos; aderência LGPD."),
        ("RNF004", "Manutenibilidade",
         "Código modular e testável, padrões de lint e formatação automatizados, documentação técnica viva no GitHub Pages."),
        ("RNF005", "Confiabilidade",
         "Estratégia de backup diária para o banco relacional, restore testado e plano de resposta a incidentes documentado."),
        ("RNF006", "Disponibilidade",
         "SLA alvo de 99% para o ambiente de produção, monitorado por dashboards e alertas automatizados."),
        ("RNF007", "Compatibilidade",
         "Compatibilidade com navegadores modernos (Chrome, Edge, Firefox, Safari) nas duas últimas versões estáveis."),
        ("RNF008", "Auditoria",
         "Logs estruturados de eventos sensíveis (autenticação, pagamento, mudança de status) com retenção mínima de 12 meses."),
        ("RNF009", "Escalabilidade",
         "Arquitetura preparada para escala horizontal e vertical, com camadas desacopladas e infraestrutura cloud."),
    ]
    rows = [["Código", "Tipo", "Descrição"]]
    rows.extend([[c, t, d] for c, t, d in rnfs])
    story.append(caption("Quadro 5 - Requisitos não funcionais", styles))
    story.append(styled_table(rows, [2 * cm, 3.2 * cm, 10.8 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(PageBreak())
    return story


def prototipo_story(styles):
    story = [Paragraph("11&nbsp;&nbsp;Protótipo Visual", styles["H1Section"])]
    story.append(Paragraph(
        "O protótipo visual do FastInBox foi produzido em <b>Figma</b>, ferramenta "
        "padrão de mercado para design de interfaces colaborativas. A construção "
        "seguiu as 10 heurísticas de usabilidade de Nielsen (1994) e as "
        "diretrizes WCAG 2.1 nível AA, com foco em legibilidade, contraste e "
        "navegação por teclado. A linguagem visual escolhida foi o estilo "
        "<b>neo-brutal</b> em preto e branco, com tipografia Space Grotesk "
        "(títulos) e IBM Plex Sans (texto), cores neutras e bordas marcadas. "
        "Esse partido visual valoriza a leitura escaneável, transmite "
        "profissionalismo e mantém-se neutro o suficiente para receber a "
        "identidade white label de cada clínica parceira sem competir com ela.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "O protótipo cobre as 12 jornadas principais do produto, foi validado "
        "internamente pela equipe e revisado em sessões com nutricionistas "
        "convidados antes da implementação em código. Cada tela do protótipo "
        "tem correspondência direta a um ou mais requisitos funcionais (RF001 a "
        "RF014), garantindo rastreabilidade entre design e especificação.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "<b>Link do protótipo Figma:</b> "
        '<font color="#1F4E79">https://www.figma.com/file/fastinbox-prototype</font>',
        styles["Body"],
    ))
    story.append(Paragraph(
        "<b>Aplicação publicada (MVP demonstrável):</b> "
        '<font color="#1F4E79">https://fastinbox.vercel.app</font>',
        styles["Body"],
    ))
    story.append(Paragraph(
        "<b>Documentação técnica:</b> "
        '<font color="#1F4E79">https://fastinbox-repo.github.io/docs/</font>',
        styles["Body"],
    ))
    story.append(Paragraph(
        "Sequência das telas em uso padrão:",
        styles["Body"],
    ))
    flow = [
        "<b>1.</b> Home institucional - apresentação da proposta de valor.",
        "<b>2.</b> Login multi-perfil - seleção do perfil e autenticação.",
        "<b>3.</b> Dashboard do nutricionista - visão consolidada de pacientes, pedidos e status.",
        "<b>4.</b> Cadastro/edição de paciente - formulário com validação em linha.",
        "<b>5.</b> Builder de pedido - composição das marmitas, embalagem e comissão com geração de código único.",
        "<b>6.</b> Configurações da clínica - upload de logotipo e identidade visual.",
        "<b>7.</b> Landing do paciente - entrada por código único do pedido.",
        "<b>8.</b> Revisão e confirmação do pedido - itens, observações nutricionais e total.",
        "<b>9.</b> Checkout integrado - pagamento sem redirecionamento externo.",
        "<b>10.</b> Acompanhamento do paciente - status de produção e entrega.",
        "<b>11.</b> Painel kanban da cozinha - pedidos pagos por estágio operacional.",
        "<b>12.</b> Dashboard administrativo - gestão global, comissões e auditoria.",
    ]
    story.extend(bullet_list(flow, styles))
    story.append(Paragraph(
        "<i>As capturas de tela das jornadas estão disponíveis na pasta /docs/documents/ "
        "do repositório do projeto e nas evidências de cada sprint.</i>",
        styles["Body"],
    ))
    story.extend(figure_block(
        ROOT / "tmp" / "pi_iii_assets" / "proto-montage.png",
        "Figura 2 - Telas do protótipo de alta fidelidade (Figma)",
        styles, max_w=16 * cm, max_h=20 * cm,
    ))
    story.append(PageBreak())
    return story


def mvp_story(styles):
    story = [Paragraph("12&nbsp;&nbsp;Requisito dos MVPs", styles["H1Section"])]
    story.append(Paragraph(
        "O conceito de Produto Mínimo Viável (MVP), originário de Ries (2011), é "
        "operacionalizado no FastInBox via MVP Canvas de Caroli (2018), permitindo "
        "validar hipóteses de produto e mercado com o menor esforço de "
        "implementação. A estratégia adotada divide o produto em duas frentes "
        "(móvel e web) com escopo dimensionado para cada ciclo do Projeto "
        "Integrador.",
        styles["Body"],
    ))

    story.append(Paragraph("12.1&nbsp;&nbsp;Aplicativo Móvel", styles["H2Section"]))
    story.append(Paragraph(
        "Para o MVP do Projeto Integrador III, o aplicativo móvel nativo não está "
        "no escopo. A experiência mobile é integralmente atendida pelo Web "
        "Application responsivo, construído com abordagem mobile-first (layouts "
        "primeiramente otimizados para telas de 360 a 414px, depois adaptados a "
        "tablet e desktop). Essa decisão reduz o custo de manutenção em três "
        "plataformas (iOS, Android, web) durante a validação de hipóteses, "
        "permite ciclos de release diários sem submissão a app stores e mantém "
        "uma única base de código TypeScript. O aplicativo móvel nativo está "
        "previsto para fases posteriores como evolução da plataforma, conforme "
        "registrado na ERS (item 4.2 - Fora de escopo) e no Documento de Visão "
        "(item 6 - Não objetivos desta fase).",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Requisitos previstos para a evolução mobile (PI IV ou superior), com "
        "implementação em React Native ou Flutter para reaproveitar a base "
        "TypeScript:",
        styles["Body"],
    ))
    mobile_reqs = [
        "Acesso por código do pedido com leitura de QR Code via câmera.",
        "Notificações push para mudança de status do pedido (em produção, pronto, em entrega, entregue).",
        "Perfil do paciente com histórico de pedidos e novo pedido com um toque.",
        "Pagamento integrado com biometria do dispositivo (Face ID, Touch ID, biometria Android).",
        "Modo offline para visualização de pedidos já confirmados, com sincronização ao reconectar.",
        "Integração com calendário e lembretes para janelas de entrega.",
    ]
    story.extend(bullet_list(mobile_reqs, styles))

    story.append(Paragraph("12.2&nbsp;&nbsp;Web Application", styles["H2Section"]))
    story.append(Paragraph(
        "O Web Application FastInBox é o entregável principal do MVP do Projeto "
        "Integrador III e foi construído sobre uma stack moderna e production-"
        "ready. O <b>front-end</b> utiliza Next.js 15 (App Router e Server "
        "Components), React 19, TypeScript estrito, Tailwind CSS 4 e bibliotecas "
        "de apoio como Lucide (ícones), Recharts (gráficos administrativos) e "
        "Sonner (toasts). O <b>back-end</b> é construído em NestJS 11 sobre "
        "Node.js 24, com módulos organizados por domínio (auth, users, patients, "
        "orders, kitchen, admin), persistência em PostgreSQL 17 (Neon em "
        "produção) e Redis para cache. A comunicação front-end ↔ back-end é "
        "realizada por API REST com contratos OpenAPI/Swagger documentados. "
        "Pipelines de CI/CD em GitHub Actions executam build, lint, testes "
        "unitários e deploy automatizado para Vercel (front) e Railway/Render "
        "(back) a cada push em branches monitoradas.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "As capacidades mínimas obrigatórias para o MVP são:",
        styles["Body"],
    ))
    web_reqs = [
        "Autenticação multi-perfil (nutricionista, paciente, cozinha, administrador) com rotas protegidas via guards do NestJS e middleware do Next.js.",
        "Cadastro e gestão de pacientes vinculados ao nutricionista, com validação em linha e prevenção de duplicidade por e-mail/CPF.",
        "Builder de pedido com múltiplas marmitas, embalagem, observações nutricionais, comissão progressiva e geração de código único de 8 dígitos para acesso do paciente.",
        "Configuração da identidade visual da clínica (logotipo, cores, nome) - operação white label aplicada em runtime.",
        "Landing do paciente com acesso por código, revisão detalhada do pedido, possibilidade de edição controlada e confirmação obrigatória antes do pagamento.",
        "Checkout integrado com simulação de gateway no MVP (Sprint 1 a 3) e plano de integração real com Pagar.me ou Mercado Pago no Sprint 4 do PI IV.",
        "Painel kanban da cozinha com drag-and-drop de status (em produção → pronto → em entrega → entregue), trilha de auditoria por movimento.",
        "Dashboard administrativo com filtros temporais, indicadores de comissões, conciliação financeira preliminar e exportação CSV.",
        "Layout responsivo com tema neo-brutal preto e branco em modo padrão, identidade white label aplicada por clínica em runtime via CSS variables.",
        "Trilha de auditoria persistida (audit_log) para eventos sensíveis: login, pagamento, mudança de status, alteração de regra de comissão.",
        "Conformidade com LGPD: consentimento explícito do paciente para tratamento de dados, política de privacidade publicada, direito de exclusão suportado.",
    ]
    story.extend(bullet_list(web_reqs, styles))
    story.append(PageBreak())
    return story


def modelo_dados_story(styles):
    story = [Paragraph("13&nbsp;&nbsp;Modelo de Dados (Web Application)", styles["H1Section"])]
    story.append(Paragraph(
        "A modelagem de dados do FastInBox segue o paradigma relacional sobre "
        "PostgreSQL 17, escolhido pela maturidade, suporte robusto a integridade "
        "referencial, transações ACID e conformidade SQL. O modelo lógico foi "
        "derivado do diagrama UML de classes, normalizado até a 3FN para "
        "minimizar redundância e maximizar consistência. As entidades principais "
        "estão organizadas em três camadas conceituais: <b>identidade</b> "
        "(users, clinics, patients), <b>operação comercial</b> (orders, "
        "order_items, payments, commissions) e <b>operação física e auditoria</b> "
        "(production_events, audit_log). O diagrama abaixo apresenta as 9 "
        "tabelas e os principais relacionamentos.",
        styles["Body"],
    ))
    story.append(caption("Figura 3 - Diagrama entidade-relacionamento do banco de dados", styles))
    story.append(DBSchemaDiagram(available_width=CONTENT_W, height=14.4 * cm))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "<b>Relacionamentos principais:</b> users 1:N clinics (um usuário "
        "administrador pode ter várias clínicas no white label); users "
        "(nutricionista) 1:N patients (cada nutricionista mantém sua carteira); "
        "patients 1:N orders (um paciente pode ter vários pedidos ao longo do "
        "tempo); orders 1:N order_items (pedido com múltiplas marmitas); orders "
        "1:N payments (suporta tentativas de pagamento e estornos); orders 1:N "
        "production_events (trilha do status produtivo); orders 1:1 commissions "
        "(uma comissão calculada por pedido). A tabela <b>audit_log</b> "
        "centraliza eventos sensíveis em formato JSONB, com retenção mínima de "
        "12 meses, atendendo aos RNF008 (Auditoria) e RF014.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Decisões arquiteturais relevantes: <b>UUID v4</b> como chave primária "
        "(em vez de IDs sequenciais) para evitar enumeração e facilitar "
        "sincronização entre ambientes; <b>soft delete</b> nas tabelas "
        "principais via campo <i>deleted_at</i> para suportar exclusão lógica "
        "exigida pela LGPD; <b>índices compostos</b> em colunas de filtro "
        "frequente (clinic_id + created_at em orders, status + created_at em "
        "production_events); e <b>triggers</b> para popular automaticamente o "
        "audit_log em INSERT/UPDATE/DELETE de tabelas sensíveis.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def testes_story(styles):
    story = [Paragraph("14&nbsp;&nbsp;Resultados de Teste", styles["H1Section"])]
    story.append(Paragraph(
        "A estratégia de testes do FastInBox é estruturada em três camadas, "
        "seguindo a pirâmide de testes de Cohn (2009). Na base, <b>testes "
        "unitários</b> em Jest cobrem regras de negócio e pure functions do "
        "back-end e do front-end. No meio, <b>testes de integração</b> "
        "verificam a comunicação entre módulos do NestJS e a integração com o "
        "banco PostgreSQL via supertest sobre uma instância dockerizada. No "
        "topo, <b>testes end-to-end (E2E)</b> em Playwright simulam jornadas "
        "completas de usuário no ambiente publicado, validando a experiência "
        "real. Toda a execução é gerenciada na plataforma <b>QASE.IO</b>, com "
        "casos de teste rastreáveis aos requisitos funcionais (RF001 a RF014) "
        "e relatórios consolidados disponíveis em "
        "<i>app.qase.io/project/FASTINBOX</i>.",
        styles["Body"],
    ))
    story.extend(figure_block(
        ROOT / "tmp" / "pi_iii_assets" / "fluxo-montage.png",
        "Figura 4 - Capturas do sistema funcional em execução (evidências das sprints)",
        styles, max_w=16 * cm, max_h=20.5 * cm,
    ))

    story.append(Paragraph("14.1&nbsp;&nbsp;Testes Internos (equipe de desenvolvimento)", styles["H2Section"]))
    story.append(Paragraph(
        "Os testes internos foram conduzidos pela equipe de desenvolvimento "
        "sobre o MVP web durante a Sprint 1 e a Sprint 2, totalizando 75 casos "
        "planejados distribuídos pelos sete módulos principais do sistema. A "
        "execução seguiu protocolo de checklist com critérios de aceite "
        "explícitos e evidências (prints e logs) anexadas a cada caso. O "
        "quadro abaixo resume os resultados consolidados.",
        styles["Body"],
    ))
    rows = [
        ["Módulo", "Casos planejados", "Executados", "Aprovados", "Reprovados", "Cobertura"],
        ["Autenticação", "12", "12", "12", "0", "100%"],
        ["Pacientes", "10", "10", "9", "1", "100%"],
        ["Pedido / Builder", "18", "18", "16", "2", "100%"],
        ["Landing Paciente", "9", "9", "9", "0", "100%"],
        ["Checkout (mock)", "8", "8", "8", "0", "100%"],
        ["Painel Cozinha", "11", "11", "10", "1", "100%"],
        ["Dashboard Admin", "7", "7", "7", "0", "100%"],
        ["<b>Total</b>", "<b>75</b>", "<b>75</b>", "<b>71</b>", "<b>4</b>", "<b>100%</b>"],
    ]
    story.append(caption("Tabela 1 - Resultados consolidados dos testes internos", styles))
    story.append(styled_table(rows, [3.2 * cm, 2.4 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.0 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "<b>Defeitos encontrados:</b> 4 reprovações corrigidas no próprio ciclo "
        "(validação de CPF, ajuste de comissão com desconto, transição de status "
        "no kanban e responsividade em tablet). Reteste com sucesso.",
        styles["Body"],
    ))

    story.append(Paragraph(
        '14.2&nbsp;&nbsp;Testes Fechados (Equipe de Teste, Convidados Acadêmicos e Orientador) '
        '(PI IV)',
        styles["H2Section"],
    ))
    story.append(Paragraph(
        "Etapa prevista para o Projeto Integrador IV. Plano de execução: rodada "
        "guiada com a professora orientadora e convidados acadêmicos, com casos "
        "de teste exploratórios sobre as jornadas do nutricionista, paciente e "
        "cozinha; relatório será consolidado em QASE.IO e anexado a esta seção "
        "no PI IV.",
        styles["Body"],
    ))

    story.append(Paragraph(
        '14.3&nbsp;&nbsp;Testes Beta (Stakeholders) '
        '(PI IV)',
        styles["H2Section"],
    ))
    story.append(Paragraph(
        "Etapa prevista para o Projeto Integrador IV. Piloto com 1 a 2 clínicas "
        "parceiras reais, mensurando taxa de criação de pedido, conversão de "
        "pagamento, lead time da cozinha e satisfação qualitativa (CSAT). O "
        "relatório será anexado a esta seção no PI IV.",
        styles["Body"],
    ))

    story.append(Paragraph("14.4&nbsp;&nbsp;Matriz de Teste e Devolutiva", styles["H2Section"]))
    story.append(Paragraph(
        "Em aderência à competência C19 (Garantia de Qualidade) e ao framework "
        "Fases_ACE, a fase de <b>Intervenção</b> (execução técnica) culmina "
        "obrigatoriamente em uma <b>Devolutiva</b> (resultados validados). Mais "
        "do que reportar defeitos, a equipe aplica o conceito <i>\"So What?\"</i>: "
        "para cada achado pergunta-se qual o impacto real sobre a integridade do "
        "produto e sobre o parceiro atendido. Os defeitos são corrigidos "
        "imediatamente após o feedback, evitando o acúmulo de dívida técnica. O "
        "quadro a seguir exemplifica a auditoria de funcionalidades críticas.",
        styles["Body"],
    ))
    rows = [["Funcionalidade auditada", "Tipo de teste", "Resultado esperado", "Devolutiva (feedback) / impacto"]]
    matriz = [
        ("Validação de CPF do paciente", "Regra de negócio", "Impedir cadastro com CPF inválido", "<b>Falha inicial:</b> aceitava sequências genéricas como válidas. <b>Impacto (So What?):</b> risco de inconsistência dos dados do parceiro; corrigido no mesmo ciclo, com reteste aprovado."),
        ("Autenticação multi-perfil", "Critério de aceitação", "Login seguro segregado por perfil", "<b>Sucesso:</b> validado conforme a HU-005 / CA-005, sem ocorrência de falhas."),
        ("Segregação de acesso (RBAC admin)", "Critério de aceitação", "Nutricionista recebe 403 em /admin/*", "<b>Sucesso:</b> TC-020 aprovado; o audit_log registra a tentativa negada (TC-021)."),
        ("Webhook de pagamento (HMAC)", "Regra de negócio", "Processar o webhook de forma idempotente", "<b>Sucesso:</b> validação <i>timing-safe</i> e janela anti-replay de +/- 5 min impedem o reprocessamento."),
        ("Cálculo de comissão progressiva", "Regra de negócio", "Calcular comissão e repasse corretos", "<b>Falha inicial:</b> divergência no ajuste com desconto. <b>Impacto (So What?):</b> repasse incorreto ao nutricionista; corrigido e reteste aprovado."),
    ]
    for m in matriz:
        rows.append(list(m))
    story.append(caption("Quadro 6 - Matriz de teste e devolutiva", styles))
    story.append(styled_table(rows, [3.6 * cm, 2.6 * cm, 3.4 * cm, 6.4 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))

    story.append(PageBreak())
    return story


# ----------------------------------------------------------------------------
# Agile charts (custom flowables) - Velocity, Burndown, WIP, Scrum cadence
# ----------------------------------------------------------------------------


class VelocityChart(Flowable):
    """Grouped bar chart: planned vs delivered story points per sprint."""

    def __init__(self, planned, delivered, labels, width=None, height=7.4 * cm, ymax=60):
        super().__init__()
        self.planned = planned
        self.delivered = delivered
        self.labels = labels
        self.width = width or (CONTENT_W)
        self.height = height
        self.ymax = ymax

    def wrap(self, aw, ah):
        self.width = aw
        return self.width, self.height

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        left, right, top, bottom = 1.25 * cm, 0.4 * cm, 1.35 * cm, 1.0 * cm
        plot_w = W - left - right
        plot_h = H - top - bottom
        x0, y0 = left, bottom
        ymax = self.ymax
        steps = 4
        c.setFont("Helvetica", 7.5)
        for i in range(steps + 1):
            val = ymax * i / steps
            yy = y0 + plot_h * i / steps
            c.setStrokeColor(colors.HexColor("#DDDDDD"))
            c.setLineWidth(0.4)
            c.line(x0, yy, x0 + plot_w, yy)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawRightString(x0 - 0.12 * cm, yy - 2.4, f"{int(val)}")
        c.setStrokeColor(BLACK)
        c.setLineWidth(0.8)
        c.line(x0, y0, x0, y0 + plot_h)
        c.line(x0, y0, x0 + plot_w, y0)
        n = len(self.labels)
        group_w = plot_w / n
        bar_w = group_w * 0.26
        for i in range(n):
            cx = x0 + group_w * i + group_w / 2
            ph = plot_h * self.planned[i] / ymax
            c.setFillColor(colors.HexColor("#B5B5B5"))
            c.rect(cx - bar_w - 0.07 * cm, y0, bar_w, ph, fill=1, stroke=0)
            dh = plot_h * self.delivered[i] / ymax
            c.setFillColor(BLACK)
            c.rect(cx + 0.07 * cm, y0, bar_w, dh, fill=1, stroke=0)
            c.setFont("Helvetica", 7)
            c.setFillColor(colors.HexColor("#555555"))
            c.drawCentredString(cx - bar_w / 2 - 0.07 * cm, y0 + ph + 2.5, str(self.planned[i]))
            c.setFillColor(BLACK)
            c.drawCentredString(cx + bar_w / 2 + 0.07 * cm, y0 + dh + 2.5, str(self.delivered[i]))
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(cx, y0 - 0.42 * cm, self.labels[i])
        # legend (top, centered)
        ly = y0 + plot_h + 0.55 * cm
        sw = 0.34 * cm
        lx = x0 + plot_w / 2 - 3.4 * cm
        c.setFillColor(colors.HexColor("#B5B5B5"))
        c.rect(lx, ly, sw, 0.22 * cm, fill=1, stroke=0)
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 8)
        c.drawString(lx + 0.44 * cm, ly, "Pontos planejados")
        c.setFillColor(BLACK)
        c.rect(lx + 3.7 * cm, ly, sw, 0.22 * cm, fill=1, stroke=0)
        c.drawString(lx + 3.7 * cm + 0.44 * cm, ly, "Pontos entregues")


class BurndownChart(Flowable):
    """Sprint burndown: ideal line vs actual remaining story points."""

    def __init__(self, total, actual, day_labels, width=None, height=7.0 * cm):
        super().__init__()
        self.total = total
        self.actual = actual
        self.day_labels = day_labels
        self.width = width or (CONTENT_W)
        self.height = height

    def wrap(self, aw, ah):
        self.width = aw
        return self.width, self.height

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        left, right, top, bottom = 1.25 * cm, 0.5 * cm, 1.25 * cm, 1.0 * cm
        plot_w = W - left - right
        plot_h = H - top - bottom
        x0, y0 = left, bottom
        ymax = self.total
        steps = 4
        c.setFont("Helvetica", 7.5)
        for i in range(steps + 1):
            val = ymax * i / steps
            yy = y0 + plot_h * i / steps
            c.setStrokeColor(colors.HexColor("#DDDDDD"))
            c.setLineWidth(0.4)
            c.line(x0, yy, x0 + plot_w, yy)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawRightString(x0 - 0.12 * cm, yy - 2.4, f"{int(val)}")
        c.setStrokeColor(BLACK)
        c.setLineWidth(0.8)
        c.line(x0, y0, x0, y0 + plot_h)
        c.line(x0, y0, x0 + plot_w, y0)
        n = len(self.actual)
        def px(i):
            return x0 + plot_w * i / (n - 1)
        def py(v):
            return y0 + plot_h * v / ymax
        # ideal line (dashed grey)
        c.setStrokeColor(colors.HexColor("#9A9A9A"))
        c.setLineWidth(1.0)
        c.setDash(3, 2)
        c.line(px(0), py(self.total), px(n - 1), py(0))
        c.setDash()
        # actual polyline (black)
        c.setStrokeColor(BLACK)
        c.setLineWidth(1.6)
        for i in range(n - 1):
            c.line(px(i), py(self.actual[i]), px(i + 1), py(self.actual[i + 1]))
        for i in range(n):
            c.setFillColor(BLACK)
            c.circle(px(i), py(self.actual[i]), 0.055 * cm, fill=1, stroke=0)
        # x labels
        c.setFont("Helvetica", 7.5)
        c.setFillColor(BLACK)
        for i, lb in enumerate(self.day_labels):
            c.drawCentredString(px(i), y0 - 0.4 * cm, lb)
        # legend
        ly = y0 + plot_h + 0.5 * cm
        lx = x0 + plot_w / 2 - 3.3 * cm
        c.setStrokeColor(colors.HexColor("#9A9A9A"))
        c.setLineWidth(1.0)
        c.setDash(3, 2)
        c.line(lx, ly + 0.08 * cm, lx + 0.7 * cm, ly + 0.08 * cm)
        c.setDash()
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 8)
        c.drawString(lx + 0.85 * cm, ly, "Linha ideal")
        c.setStrokeColor(BLACK)
        c.setLineWidth(1.6)
        c.line(lx + 3.3 * cm, ly + 0.08 * cm, lx + 4.0 * cm, ly + 0.08 * cm)
        c.drawString(lx + 4.15 * cm, ly, "Pontos restantes (real)")


class WipChart(Flowable):
    """Horizontal bars: WIP limit vs observed average per Kanban column."""

    def __init__(self, rows, xmax=15, width=None, height=None):
        super().__init__()
        self.rows = rows  # list of (label, limit, observed)
        self.xmax = xmax
        self.width = width or (CONTENT_W)
        self.height = height or (1.0 * cm + 1.25 * cm * len(rows))

    def wrap(self, aw, ah):
        self.width = aw
        return self.width, self.height

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        left, right, top, bottom = 3.0 * cm, 1.6 * cm, 0.7 * cm, 0.5 * cm
        plot_w = W - left - right
        x0 = left
        n = len(self.rows)
        row_h = (H - top - bottom) / n
        bar_h = row_h * 0.34
        for idx, (label, limit, observed) in enumerate(self.rows):
            cy = bottom + row_h * (n - 1 - idx) + row_h / 2
            # limit bar (light)
            lw = plot_w * min(limit, self.xmax) / self.xmax
            c.setFillColor(colors.HexColor("#D9D9D9"))
            c.rect(x0, cy, lw, bar_h, fill=1, stroke=0)
            # observed bar (black) just below
            ow = plot_w * observed / self.xmax
            c.setFillColor(BLACK)
            c.rect(x0, cy - bar_h - 0.06 * cm, ow, bar_h, fill=1, stroke=0)
            # column label
            c.setFillColor(BLACK)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawRightString(x0 - 0.2 * cm, cy - bar_h / 2 - 0.05 * cm, label)
            # value labels
            c.setFont("Helvetica", 7.5)
            c.setFillColor(colors.HexColor("#555555"))
            c.drawString(x0 + lw + 0.1 * cm, cy + 0.02 * cm, f"limite {limit}")
            c.setFillColor(BLACK)
            obs_txt = str(observed).replace(".", ",")
            c.drawString(x0 + ow + 0.1 * cm, cy - bar_h - 0.04 * cm, f"WIP {obs_txt}")


class ScrumCadenceDiagram(Flowable):
    """Horizontal cadence: Planning -> Daily (loop) -> Review -> Retrospectiva."""

    def __init__(self, width=None, height=2.6 * cm):
        super().__init__()
        self.width = width or (CONTENT_W)
        self.height = height

    def wrap(self, aw, ah):
        self.width = aw
        return self.width, self.height

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        boxes = ["Sprint\nPlanning", "Daily Scrum\n(diária)", "Sprint\nReview", "Sprint\nRetrospectiva"]
        n = len(boxes)
        gap = 0.9 * cm
        bw = (W - gap * (n - 1)) / n
        bh = 1.5 * cm
        by = H - bh - 0.55 * cm
        for i, label in enumerate(boxes):
            bx = i * (bw + gap)
            c.setFillColor(colors.HexColor("#1F4E79"))
            c.setStrokeColor(colors.HexColor("#1F4E79"))
            c.roundRect(bx, by, bw, bh, 0.18 * cm, fill=1, stroke=1)
            c.setFillColor(WHITE)
            lines = label.split("\n")
            c.setFont("Helvetica-Bold", 9)
            ty = by + bh / 2 + (len(lines) - 1) * 5.5
            for ln in lines:
                c.drawCentredString(bx + bw / 2, ty - 4, ln)
                ty -= 11
            if i < n - 1:
                ax = bx + bw + 0.1 * cm
                ay = by + bh / 2
                c.setStrokeColor(BLACK)
                c.setLineWidth(1.2)
                c.line(ax, ay, ax + gap - 0.2 * cm, ay)
                c.setFillColor(BLACK)
                tipx = ax + gap - 0.2 * cm
                c.line(tipx, ay, tipx - 0.14 * cm, ay + 0.1 * cm)
                c.line(tipx, ay, tipx - 0.14 * cm, ay - 0.1 * cm)
        c.setFillColor(colors.HexColor("#555555"))
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(W / 2, 0.12 * cm, "Cadência por Sprint de 2 a 3 semanas - cerimônias Scrum-like sincronizadas no GitHub Projects")


# ----------------------------------------------------------------------------
# New sections - Sprint #05, artefacts and agile metrics
# ----------------------------------------------------------------------------


def historias_criterios_story(styles):
    story = [Paragraph(
        "15&nbsp;&nbsp;Histórias de Usuário e Critérios de Aceitação",
        styles["H1Section"],
    )]
    story.append(Paragraph(
        "As funcionalidades do FastInBox foram elicitadas e descritas como "
        "histórias de usuário, no formato preconizado por Cohn (2005) - "
        "<i>\"Como &lt;perfil&gt;, quero &lt;ação&gt;, para &lt;benefício&gt;\"</i> - "
        "e priorizadas por sprint (S1 a S5) na coluna de prioridade. Cada "
        "história é rastreável a um ou mais requisitos funcionais (RF) e às "
        "regras de negócio da Seção 16, garantindo continuidade entre a "
        "elicitação, o backlog mantido no GitHub Projects e os critérios de "
        "aceitação que orientam o teste de cada entrega.",
        styles["Body"],
    ))

    story.append(Paragraph("15.1&nbsp;&nbsp;Histórias de Usuário", styles["H2Section"]))
    rows = [["ID", "Perfil", "História", "Prior.", "RF"]]
    hus = [
        ("HU-001", "Visitante", "Como visitante, quero ver a landing pública para entender o produto.", "S1", "RF019"),
        ("HU-002", "Visitante", "Como visitante, quero consultar o status do meu pedido pelo código único, sem login.", "S1", "RF005"),
        ("HU-003", "Visitante", "Como visitante, quero criar uma conta como paciente para receber pedidos.", "S1", "RF002"),
        ("HU-004", "Usuário", "Como usuário, quero recuperar minha senha por e-mail para retomar o acesso.", "S2", "RF001"),
        ("HU-005", "Nutricionista", "Como nutricionista, quero autenticar com e-mail e senha para acessar minha área.", "S1", "RF001"),
        ("HU-006", "Nutricionista", "Como nutricionista, quero cadastrar pacientes com restrições alimentares para personalizar pedidos.", "S1", "RF002"),
        ("HU-007", "Nutricionista", "Como nutricionista, quero editar dados de paciente existente para manter o cadastro atualizado.", "S2", "RF002"),
        ("HU-008", "Nutricionista", "Como nutricionista, quero criar pedido com múltiplas marmitas para atender o plano alimentar semanal.", "S1", "RF003"),
        ("HU-009", "Nutricionista", "Como nutricionista, quero ver o código único do pedido gerado para enviar ao paciente.", "S1", "RF003"),
        ("HU-010", "Nutricionista", "Como nutricionista, quero ver o resumo financeiro do pedido (valor, comissão, repasse) para conferir antes de enviar.", "S1", "RF013"),
        ("HU-011", "Nutricionista", "Como nutricionista, quero acompanhar o status de cada pedido criado para responder ao paciente.", "S2", "RF008"),
        ("HU-012", "Nutricionista", "Como nutricionista, quero configurar a identidade visual da clínica para aplicar o white label.", "S2", "RF004"),
        ("HU-013", "Paciente", "Como paciente, quero acessar o pedido informando o código único para ver os detalhes.", "S1", "RF005"),
        ("HU-014", "Paciente", "Como paciente, quero revisar itens, observações e valor antes de confirmar para garantir que está correto.", "S1", "RF006"),
        ("HU-015", "Paciente", "Como paciente, quero confirmar o pedido para liberar o pagamento sem voltar à etapa de edição.", "S1", "RF006"),
        ("HU-016", "Paciente", "Como paciente, quero pagar diretamente na plataforma para não depender de canal externo.", "S2", "RF007"),
        ("HU-017", "Paciente", "Como paciente, quero ver o histórico de status do pedido em <i>timeline</i> para saber o que está acontecendo.", "S2", "RF008"),
        ("HU-018", "Paciente", "Como paciente, quero receber notificação de mudança crítica de status para não consultar manualmente.", "S5", "RF010"),
        ("HU-019", "Cozinha", "Como cozinha, quero autenticar com credencial dedicada para acessar o painel operacional.", "S1", "RF001"),
        ("HU-020", "Cozinha", "Como cozinha, quero ver o kanban com pedidos pagos para priorizar a produção.", "S1", "RF009"),
        ("HU-021", "Cozinha", "Como cozinha, quero arrastar o pedido entre colunas para atualizar o status com trilha de auditoria.", "S1", "RF010"),
        ("HU-022", "Cozinha", "Como cozinha, quero abrir o detalhe de cada pedido para conferir restrições e observações.", "S2", "RF009"),
        ("HU-023", "Administrador", "Como admin, quero ver dashboard consolidado com volume, receita e status para monitorar a operação.", "S2", "RF011"),
        ("HU-024", "Administrador", "Como admin, quero listar e filtrar usuários por perfil para gerir contas.", "S2", "RF011"),
        ("HU-025", "Administrador", "Como admin, quero ver a auditoria de eventos sensíveis para responder a incidentes.", "S2", "RF014"),
        ("HU-026", "Administrador", "Como admin, quero ver o diagnóstico de saúde da plataforma (banco, fila, gateway) para detectar problemas.", "S5", "RF011"),
        ("HU-027", "Administrador", "Como admin, quero exportar relatório de comissões por período para repasse contábil.", "S5", "RF013"),
        ("HU-028", "Sistema", "Como sistema, quero gerar código único de pedido não colidente para garantir o acesso seguro do paciente.", "S3", "RF003"),
    ]
    for hu in hus:
        rows.append(list(hu))
    story.append(caption("Quadro 7 - Histórias de usuário", styles))
    story.append(styled_table(rows, [1.55 * cm, 2.35 * cm, 9.45 * cm, 1.25 * cm, 1.4 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("15.2&nbsp;&nbsp;Critérios de Aceitação", styles["H2Section"]))
    story.append(Paragraph(
        "Os critérios de aceitação são especificados no formato Gherkin "
        "(Dado / Quando / Então), conforme a prática de <i>Behavior Driven "
        "Development</i>, tornando cada história verificável de forma objetiva. "
        "Reproduzem-se a seguir os critérios das histórias prioritárias, que "
        "deram origem aos casos de teste apresentados nas Seções 14 e 17.",
        styles["Body"],
    ))

    blocks = [
        ("HU-002 - Rastreio do pedido por código", [
            ("CA-002.1", ["Dado que informo o código FIB-2026-001 no atalho de rastreio",
                          "Quando confirmo a busca",
                          "Então sou redirecionado para a página de status do pedido",
                          "E vejo a <i>timeline</i> atual do pedido"]),
        ]),
        ("HU-005 - Autenticação do nutricionista", [
            ("CA-005.1", ["Dado credenciais válidas",
                          "Quando faço login como nutricionista",
                          "Então sou redirecionado para a área /nutricionista"]),
            ("CA-005.2", ["Dado credenciais inválidas",
                          "Quando tento o login",
                          "Então permaneço em /login com mensagem de erro"]),
        ]),
        ("HU-006 - Cadastro de paciente", [
            ("CA-006.1", ["Dado que estou em /nutricionista/pacientes",
                          "Quando preencho nome, contato, plano, objetivo e restrições e clico em Salvar",
                          "Então o paciente aparece na lista e fica disponível para criar pedido"]),
        ]),
        ("HU-008 - Criação de pedido", [
            ("CA-008.1", ["Dado um paciente selecionado",
                          "Quando adiciono uma ou mais marmitas com itens e observações e confirmo",
                          "Então o pedido é criado com status Aguardando_Confirmacao",
                          "E o código único FIB-AAAA-NNN é exibido"]),
            ("CA-008.2", ["Dado um pedido com itens",
                          "Quando tento confirmar sem janela de entrega",
                          "Então recebo erro de validação e o pedido não é salvo"]),
        ]),
        ("HU-010 - Resumo financeiro e comissão", [
            ("CA-010.1", ["Dado um pedido em construção",
                          "Quando adiciono itens com preços",
                          "Então vejo valor base, comissão FastInBox e repasse ao nutricionista",
                          "E os valores são atualizados em tempo real conforme edito o pedido"]),
        ]),
        ("HU-015 - Confirmação do pedido", [
            ("CA-015.1", ["Dado um pedido em status Aguardando_Confirmacao",
                          "Quando reviso e clico em Confirmar",
                          "Então o status muda para Aguardando_Pagamento e o botão Pagar é habilitado"]),
        ]),
        ("HU-016 - Pagamento integrado", [
            ("CA-016.1", ["Dado um pedido em Aguardando_Pagamento",
                          "Quando seleciono o meio de pagamento e confirmo (gateway simulado)",
                          "Então o status muda para Pago e o webhook é validado por HMAC de forma idempotente"]),
            ("CA-016.2", ["Dado um pagamento que falha",
                          "Quando o gateway recusa",
                          "Então o status retorna para Aguardando_Pagamento e o paciente pode tentar novamente"]),
        ]),
        ("HU-020 / HU-021 - Painel kanban da cozinha", [
            ("CA-020.1", ["Dada a cozinha autenticada",
                          "Quando acesso /cozinha",
                          "Então vejo as colunas Recebido, Em preparo, Pronto e Entregue",
                          "E apenas pedidos com status Pago em diante são exibidos"]),
            ("CA-021.1", ["Dado um pedido na coluna Recebido",
                          "Quando o arrasto para Em preparo",
                          "Então o status é persistido no servidor",
                          "E o evento é registrado em production_events com data/hora e usuário"]),
        ]),
        ("HU-025 - Auditoria de eventos", [
            ("CA-025.1", ["Dado o admin em /admin/auditoria",
                          "Quando consulto os eventos das últimas 24 horas",
                          "Então vejo registros de login, criação de pedido, mudança de status e pagamento",
                          "E cada evento mostra ator, IP e data/hora"]),
        ]),
        ("HU-027 - Exportação de relatório de comissões (Sprint 5)", [
            ("CA-027.1", ["Dado o admin em /admin/relatorios",
                          "Quando filtro por período e clico em Exportar",
                          "Então é gerado um arquivo CSV com clinicId, nutritionistId, ordersCount, subtotal, comissão e repasse",
                          "E o cabeçalho e as linhas são consistentes com os totais exibidos em tela"]),
        ]),
    ]
    story.extend(_criterios_render(blocks, styles))
    story.append(PageBreak())
    return story


def _criterios_render(blocks, styles):
    flow = []
    head = ParagraphStyle(
        name="CAHead", parent=styles["Body"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, spaceBefore=6, spaceAfter=1, alignment=TA_LEFT,
    )
    cid = ParagraphStyle(
        name="CAId", parent=styles["Body"], fontName="Helvetica-Bold",
        fontSize=9.5, leading=12, leftIndent=10, spaceBefore=3, spaceAfter=0,
        textColor=colors.HexColor("#1F4E79"),
    )
    line = ParagraphStyle(
        name="CALine", parent=styles["Body"], fontSize=9.5, leading=12.5,
        leftIndent=24, alignment=TA_LEFT, spaceAfter=0,
    )
    for header, cas in blocks:
        flow.append(Paragraph(header, head))
        for ca, lines in cas:
            flow.append(Paragraph(ca, cid))
            for ln in lines:
                flow.append(Paragraph(f"&bull;&nbsp;&nbsp;{ln}", line))
    return flow


def regras_negocio_story(styles):
    story = [Paragraph("16&nbsp;&nbsp;Regras de Negócio", styles["H1Section"])]
    story.append(Paragraph(
        "As regras de negócio (RNB) consolidam as restrições e políticas do "
        "domínio que governam o comportamento do FastInBox, independentemente "
        "da tecnologia de implementação. Foram extraídas da Especificação de "
        "Requisitos de Software (ERS) e mapeadas aos requisitos funcionais que "
        "as concretizam, fechando a cadeia de rastreabilidade história de "
        "usuário &rarr; requisito funcional &rarr; regra de negócio &rarr; caso "
        "de teste.",
        styles["Body"],
    ))
    rows = [["Código", "Regra de Negócio", "RF relacionados"]]
    rnbs = [
        ("RNB-001", "Todos os pedidos, embalagens e experiências voltadas ao cliente final devem priorizar a identidade visual da clínica do nutricionista (logotipo, nome e marca); a marca FastInBox atua como fornecedora em segundo plano.", "RF004"),
        ("RNB-002", "O paciente somente pode confirmar e pagar o pedido após revisar as informações obrigatórias. Edições são permitidas apenas antes da confirmação final e do pagamento.", "RF006, RF007"),
        ("RNB-003", "Cada pedido possui valor base e valor final configurável, permitindo ao nutricionista ampliar a margem; o sistema deve calcular, registrar e disponibilizar relatórios da comissão de cada pedido.", "RF003, RF013, RF014"),
        ("RNB-004", "Pedidos devem ser consolidados em dias ou janelas de entrega definidas pela operação, com possibilidade de concentração em dias específicos e expansão futura conforme a demanda.", "RF003, RF010"),
        ("RNB-005", "Todo acesso e transação deve ocorrer em ambiente seguro, com armazenamento protegido de credenciais e dados sensíveis, criptografia adequada e tráfego sob HTTPS.", "RF001, RF002, RF008"),
        ("RNB-006", "A plataforma deve utilizar checkout integrado, aceitando diferentes meios de pagamento sem redirecionar o usuário para domínio externo.", "RF007"),
        ("RNB-007", "O sistema deve garantir segregação de acesso por perfil, liberando apenas as funcionalidades e dados autorizados para nutricionistas, pacientes, cozinhas e administradores.", "RF001, RF005, RF009, RF010, RF011, RF014"),
    ]
    for r in rnbs:
        rows.append(list(r))
    story.append(caption("Quadro 8 - Regras de negócio", styles))
    story.append(styled_table(rows, [2.2 * cm, 11.4 * cm, 2.4 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026), com base na ERS.", styles))
    story.append(PageBreak())
    return story


def sprint5_story(styles):
    story = [Paragraph("17&nbsp;&nbsp;Governança Ágil e Sprint #05", styles["H1Section"])]
    story.append(Paragraph(
        "A condução do FastInBox segue um processo ágil <i>Scrum-like</i> "
        "(Schwaber &amp; Sutherland, 2020) adaptado ao contexto acadêmico do "
        "Projeto Integrador, com sprints de duas a três semanas e cerimônias "
        "sincronizadas no GitHub Projects. Esta seção documenta a quinta "
        "sprint - dedicada à camada administrativa, observabilidade e "
        "endurecimento de segurança - incluindo o registro das reuniões "
        "diárias, o backlog executado, os impedimentos com seu plano de "
        "contingência e a validação funcional da entrega.",
        styles["Body"],
    ))
    story.append(Paragraph("17.1&nbsp;&nbsp;Cerimônias e Cadência", styles["H2Section"]))
    story.append(caption("Figura 5 - Cadência das cerimônias Scrum", styles))
    story.append(ScrumCadenceDiagram(width=CONTENT_W))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Spacer(1, 0.15 * cm))
    story.append(Paragraph(
        "Cada sprint inicia com o <b>Sprint Planning</b> (definição do objetivo "
        "e seleção do backlog estimado em pontos de história), mantém "
        "<b>Daily Scrums</b> assíncronas e síncronas para alinhamento diário, "
        "encerra com a <b>Sprint Review</b> (demonstração do incremento e "
        "validação dos critérios de aceitação) e a <b>Retrospectiva</b> "
        "(melhoria contínua do processo). O refinamento do backlog ocorre 48 "
        "horas antes do planning, prática adotada após a retrospectiva das "
        "Sprints 1 a 3.",
        styles["Body"],
    ))

    story.append(Paragraph("17.2&nbsp;&nbsp;Objetivo e Sprint Backlog #05", styles["H2Section"]))
    story.append(Paragraph(
        "<b>Objetivo da Sprint 5:</b> entregar a camada administrativa da "
        "plataforma e elevar a maturidade operacional com observabilidade, "
        "segurança e relatórios financeiros exportáveis. O quadro abaixo "
        "consolida os itens do Sprint Backlog #05 e seu status de fechamento "
        "(7 de 7 itens concluídos).",
        styles["Body"],
    ))
    rows = [["Item / Tarefa", "Responsável", "Pts", "Status"]]
    backlog = [
        ("[Infra] Logs centralizados, métricas e alertas por <i>threshold</i>", "João Vitor (DevOps)", "8", "Concluído"),
        ("[Infra] Rate limiting, MFA do admin e hardening transacional", "João Vitor (DevOps)", "8", "Concluído"),
        ("[Back] APIs administrativas (usuários, cozinhas e pedidos)", "Thiago Lucas", "13", "Concluído"),
        ("[Back] Gestão de cozinhas parceiras (cadastro e vínculo)", "Thiago Lucas", "8", "Concluído"),
        ("[Back] Relatórios de comissão exportáveis (período, fábrica, status)", "Thiago Lucas", "13", "Concluído"),
        ("[Front] Telas de comissão e conciliação financeira (exportação CSV)", "João Vitor (Front)", "8", "Concluído"),
        ("[QA] Cobertura de RBAC admin e validação de relatórios (TC-016 a TC-021)", "Gabriel Pahl", "5", "Concluído"),
    ]
    for b in backlog:
        rows.append(list(b))
    rows.append(["<b>Total da Sprint 5</b>", "", "<b>45</b>", "<b>42 entregues</b>"])
    story.append(caption("Quadro 9 - Sprint Backlog #05", styles))
    story.append(styled_table(rows, [9.6 * cm, 3.4 * cm, 1.0 * cm, 2.5 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))

    story.append(Paragraph("17.3&nbsp;&nbsp;Reunião Diária (Daily Scrum)", styles["H2Section"]))
    story.append(Paragraph(
        "As reuniões diárias foram registradas no ALM (GitHub Projects) "
        "respondendo às três perguntas clássicas. Apresentam-se a seguir os "
        "registros representativos do período.",
        styles["Body"],
    ))
    rows = [["Data", "Feito", "A fazer", "Impedimentos"]]
    dailies = [
        ("15/05", "ReportsService criado; endpoints /admin/reports/operations e /commissions em desenvolvimento", "Finalizar exportação CSV; iniciar telas admin", "Nenhum"),
        ("17/05", "/admin/diagnostics com health profundo (orders, payments, audit); AdminRelatoriosPage com KPIs e gráfico", "Integrar menu Relatórios ao AdminLayout; testes de RBAC", "Nenhum"),
        ("19/05", "RBAC consolidado com matriz auditável; @Roles('admin') em todos os endpoints; audit_log de acessos negados", "QA: cobrir cenários críticos TC-016 a TC-021", "Nenhum"),
        ("21/05", "Hardening: CORS restrito, rawBody, HMAC <i>timing-safe</i> em webhooks e janela anti-replay (+/- 5 min)", "Revisão final de segurança; validar alertas em produção", "Nenhum"),
        ("22/05", "Sprint fechada com 7/7 itens em Done; evidências consolidadas e parecer assinado", "Preparar Sprint 6 (autoatendimento do paciente)", "Nenhum"),
    ]
    for d in dailies:
        rows.append(list(d))
    story.append(caption("Quadro 10 - Registros das reuniões diárias (Daily Scrum)", styles))
    story.append(styled_table(rows, [1.3 * cm, 6.6 * cm, 5.2 * cm, 3.4 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))

    story.append(Paragraph("17.4&nbsp;&nbsp;Impedimentos e Plano de Contingência", styles["H2Section"]))
    rows = [["Impedimento (risco)", "Impacto", "Plano de contingência", "Status"]]
    imps = [
        ("Divergência de valores nos relatórios financeiros", "Perda de confiança da gestão", "Cálculo de referência documentado e testes por caso conhecido", "Resolvido"),
        ("MFA causando bloqueio (lockout) do admin", "Bloqueio operacional", "Procedimento de recuperação de MFA documentado antes do rollout", "Resolvido"),
        ("Alertas ruidosos (fadiga de alerta)", "Baixa resposta a incidentes reais", "Revisão de thresholds no meio da sprint e silenciamento de não acionáveis", "Resolvido"),
        ("Hardening bloqueando clientes legítimos", "Impacto no usuário final", "Rate limit por perfil com whitelists temporárias monitoradas", "Resolvido"),
        ("Instabilidade em API/serviço externo", "Atraso de até 3 dias na integração; sem impacto na entrega do MVP (So What?)", "Implementação de mock do serviço para mitigar e desbloquear o desenvolvimento", "Resolvido"),
        ("Ausência de membro-chave da equipe", "Impacto nulo no cronograma (So What?)", "Redistribuição de tarefas via ALM, com cobertura por pares", "Resolvido"),
    ]
    for r in imps:
        rows.append(list(r))
    story.append(caption("Quadro 11 - Impedimentos e plano de contingência", styles))
    story.append(styled_table(rows, [4.4 * cm, 3.4 * cm, 6.6 * cm, 2.1 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))

    story.append(Paragraph("17.5&nbsp;&nbsp;Testes e Validação da Sprint #05", styles["H2Section"]))
    story.append(Paragraph(
        "A entrega foi validada por seis casos de teste (TC-016 a TC-021) "
        "cobrindo diagnóstico, agregação de relatórios, exportação CSV e "
        "segregação de acesso, com 100% de aprovação. Destacam-se: TC-016 "
        "(GET /admin/diagnostics retorna 200 OK), TC-019 (CSV com cabeçalho "
        "válido e linhas alinhadas), TC-020 (perfil nutricionista recebe 403 "
        "em /admin/reports/*) e TC-021 (audit_log registra a tentativa negada). "
        "As evidências - coleção de requisições autenticadas, capturas do "
        "endpoint de diagnóstico (orders: 30, payments aprovados: 24, "
        "audit: 184 entradas), telas do módulo de relatórios e os commits em "
        "<i>main</i> (reports.service.ts, auth.guard.ts, AdminRelatoriosPage.tsx) "
        "- foram anexadas ao registro da sprint no ALM.",
        styles["Body"],
    ))
    story.extend(figure_block(
        ROOT / "tmp" / "pi_iii_assets" / "admin-montage.png",
        "Figura 6 - Painéis administrativos (Sprint #05): dashboard "
        "administrativo e auditoria operacional.",
        styles, max_w=16 * cm, max_h=21 * cm,
    ))

    story.append(Paragraph("17.6&nbsp;&nbsp;Comparativo de Evidências de Entrega", styles["H2Section"]))
    story.append(Paragraph(
        "A maturidade técnica entre as sprints é evidenciada pela evolução do "
        "tipo de prova entregue: na concepção (Sprint #02), as evidências são de "
        "intenção e design; na fase de maturidade (Sprints #04 e #05), são de "
        "software funcional em ambiente web, conforme o quadro a seguir.",
        styles["Body"],
    ))
    rows = [["Tipo de evidência", "Sprint #02 (Concepção/Inicial)", "Sprints #04-#05 (Maturidade Técnica)"]]
    comp = [
        ("Vídeos demonstrativos", "Navegação em protótipos e apresentação dos fluxos iniciais do sistema.", "Demonstração das funcionalidades implementadas e operacionais em ambiente web."),
        ("Prints de tela", "Wireframes, mockups e representações preliminares da interface.", "Capturas do sistema funcional (Figura 4), evidenciando a execução e os registros de sucesso."),
        ("Registros de devolutiva", "Documentação de reuniões e alinhamentos de escopo.", "Feedbacks de validação, homologação das entregas e encerramento formal da sprint."),
    ]
    for c in comp:
        rows.append(list(c))
    story.append(caption("Quadro 12 - Comparativo de evidências de entrega por sprint", styles))
    story.append(styled_table(rows, [3.2 * cm, 6.0 * cm, 6.8 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))

    story.append(PageBreak())
    return story


def figure_block(path, caption, styles, max_w=16.0 * cm, max_h=9.0 * cm):
    flow = []
    cap_style = ParagraphStyle(
        name="FigCap", parent=styles["Body"], fontName="Helvetica",
        fontSize=9, leading=12, alignment=TA_CENTER,
        textColor=colors.HexColor("#333333"), spaceBefore=4, spaceAfter=2,
    )
    src_style = ParagraphStyle(
        name="FigSrc", parent=cap_style, fontName="Helvetica-Oblique", fontSize=8,
        textColor=colors.HexColor("#666666"), spaceBefore=0, spaceAfter=6,
    )
    if path.exists():
        flow.append(Paragraph(caption, cap_style))
        img = Image(str(path), width=max_w, height=max_h, kind="proportional")
        img.hAlign = "CENTER"
        flow.append(img)
        flow.append(Paragraph("Fonte: elaborado pela equipe FastInBox (2026).", src_style))
    return [KeepTogether(flow)] if flow else []


def metricas_story(styles):
    story = [Paragraph("18&nbsp;&nbsp;Métricas Ágeis", styles["H1Section"])]
    story.append(Paragraph(
        "A produtividade e a qualidade do projeto são acompanhadas por um "
        "conjunto de métricas ágeis configuradas no ALM (GitHub Projects para "
        "fluxo e estimativas; QASE.IO e a suíte automatizada para qualidade). "
        "As cinco métricas exigidas - velocidade da equipe, tempo de ciclo, "
        "taxa de defeitos, NPS e WIP - são definidas a seguir com sua forma de "
        "medição e os valores observados nas Sprints 1 a 5.",
        styles["Body"],
    ))

    story.append(Paragraph("18.1&nbsp;&nbsp;Velocidade da Equipe (Velocity)", styles["H2Section"]))
    story.append(Paragraph(
        "<b>Definição:</b> quantidade de trabalho concluído por sprint, medida "
        "em pontos de história entregues (Cohn, 2005). Serve de <i>baseline</i> "
        "para o planejamento. <b>Medição:</b> soma dos pontos dos itens que "
        "atingem o status <i>Done</i> ao fechamento da sprint, no GitHub "
        "Projects.",
        styles["Body"],
    ))
    rows = [["Sprint", "Pts planejados", "Pts entregues", "Itens", "Observação"]]
    vel = [
        ("Sprint 1", "60", "54", "26", "Fundação e MVP navegável"),
        ("Sprint 2", "25", "21", "8", "Sprint curta"),
        ("Sprint 3", "50", "48", "20", "Persistência e API"),
        ("Sprint 4", "55", "52", "18", "Pagamento e fila"),
        ("Sprint 5", "45", "42", "7", "Admin, observabilidade, hardening"),
    ]
    for v in vel:
        rows.append(list(v))
    rows.append(["<b>Total</b>", "<b>235</b>", "<b>217</b>", "<b>79</b>", "<b>Aderência de 92,3%</b>"])
    story.append(caption("Tabela 2 - Velocidade planejada e entregue por sprint", styles))
    story.append(styled_table(rows, [2.1 * cm, 2.9 * cm, 2.9 * cm, 1.5 * cm, 6.6 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Spacer(1, 0.25 * cm))
    story.append(caption("Figura 7 - Velocidade da equipe por sprint", styles))
    story.append(VelocityChart(
        planned=[60, 25, 50, 55, 45],
        delivered=[54, 21, 48, 52, 42],
        labels=["S1", "S2", "S3", "S4", "S5"],
        width=CONTENT_W,
    ))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Paragraph(
        "Velocidade média de <b>43,4 pontos por sprint</b>; desconsiderando a "
        "Sprint 2 (curta), a equipe estabiliza entre 47 e 54 pontos, indicando "
        "previsibilidade adequada para o planejamento do PI IV.",
        styles["Body"],
    ))
    story.append(PageBreak())

    story.append(Paragraph("18.2&nbsp;&nbsp;Tempo de Ciclo (Cycle Time)", styles["H2Section"]))
    story.append(Paragraph(
        "<b>Definição:</b> tempo decorrido entre o início do trabalho em um "
        "item (<i>In Progress</i>) e sua conclusão (merge em <i>main</i> com "
        "CI/CD verde). O <i>lead time</i> agrega ainda o tempo de fila anterior "
        "(Reinertsen, 2009). <b>Medição:</b> diferença entre os carimbos de "
        "tempo das transições registradas nas issues do GitHub.",
        styles["Body"],
    ))
    rows = [["Sprint", "Ciclo médio (dias)", "Mínimo", "Máximo"]]
    cyc = [
        ("Sprint 1", "2,8", "0,5", "4,2"),
        ("Sprint 2", "3,2", "1,1", "5,5"),
        ("Sprint 3", "2,4", "0,8", "4,8"),
        ("Sprint 4", "2,2", "0,6", "3,9"),
        ("Sprint 5", "2,1", "0,5", "3,5"),
    ]
    for cc in cyc:
        rows.append(list(cc))
    rows.append(["<b>Média geral</b>", "<b>2,5</b>", "-", "-"])
    story.append(caption("Tabela 3 - Tempo de ciclo por sprint", styles))
    story.append(styled_table(rows, [3.0 * cm, 4.0 * cm, 3.0 * cm, 3.0 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Paragraph(
        "O tempo de ciclo médio de <b>2,5 dias</b> (lead time ponta a ponta de "
        "3,5 a 4 dias) é sustentado por <i>Trunk-Based Development</i> com "
        "<i>main</i> protegida, CI/CD ativo desde a Sprint 1 e pair programming "
        "nas rotas críticas (autenticação e pagamento). O gráfico de burndown a "
        "seguir ilustra o consumo de pontos ao longo da Sprint 5.",
        styles["Body"],
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "<b>Burndown da Sprint 5</b> (45 pontos)", styles["H2Section"],
    ))
    story.append(caption("Figura 8 - Burndown da Sprint 5", styles))
    story.append(BurndownChart(
        total=45,
        actual=[45, 45, 38, 30, 30, 21, 13, 5, 0],
        day_labels=["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"],
        width=CONTENT_W,
    ))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(PageBreak())

    story.append(Paragraph("18.3&nbsp;&nbsp;Taxa de Defeitos (Defect Rate)", styles["H2Section"]))
    story.append(Paragraph(
        "<b>Definição:</b> razão entre defeitos identificados e volume de "
        "testes executados; a <i>Defect Removal Efficiency</i> (DRE) mede o "
        "percentual de defeitos corrigidos no mesmo ciclo (Kan, 2002; ISO/IEC "
        "25010). <b>Medição:</b> defeitos triados em GitHub Issues com rótulo "
        "<i>bug</i> e severidade, frente às camadas de teste. A tabela "
        "reconcilia as duas camadas de validação do projeto.",
        styles["Body"],
    ))
    rows = [["Camada de teste", "Casos", "Defeitos", "Taxa", "DRE"]]
    defs = [
        ("Testes internos de módulo (S1-S2)", "75", "4", "5,3%", "100%"),
        ("Cenários consolidados de aceitação / E2E (S1-S5)", "21", "0*", "0,0%", "100%"),
    ]
    for d in defs:
        rows.append(list(d))
    rows.append(["<b>Total consolidado</b>", "<b>96</b>", "<b>4</b>", "<b>4,2%</b>", "<b>100%</b>"])
    story.append(caption("Tabela 4 - Taxa de defeitos por camada de teste", styles))
    story.append(styled_table(rows, [7.4 * cm, 1.8 * cm, 2.2 * cm, 1.9 * cm, 1.7 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Paragraph(
        "* As duas ocorrências registradas na camada de aceitação (OC-001 - "
        "formatação de payload no roteiro; OC-002 - retorno 403 correto por "
        "regra de RBAC) foram reclassificadas como ajuste de ambiente e "
        "validação de regra, e não como defeitos de produto. A densidade de "
        "defeitos resultante (cerca de 0,2 defeito por KLOC) situa-se "
        "confortavelmente abaixo do <i>baseline</i> industrial de 1 a 3 por "
        "KLOC, e não há defeitos bloqueantes em aberto.",
        styles["Body"],
    ))

    story.append(Paragraph("18.4&nbsp;&nbsp;NPS (Net Promoter Score)", styles["H2Section"]))
    story.append(Paragraph(
        "<b>Definição:</b> NPS = (% de promotores) - (% de detratores), em "
        "escala de 0 a 10, onde 9-10 são promotores, 7-8 passivos e 0-6 "
        "detratores (Reichheld, 2003). <b>Medição:</b> formulário pós-teste "
        "aplicado na sessão de validação guiada (teste alfa), com a pergunta "
        "\"Qual a probabilidade de você recomendar o FastInBox a um colega?\". "
        "Amostra inicial de 3 respondentes (1 nutricionista convidada e 2 "
        "docentes): 2 promotores (notas 9), 1 passivo (nota 8), 0 detratores, "
        "resultando em <b>NPS = 66,7</b> (faixa de excelência). A amostra será "
        "ampliada no teste Beta do PI IV, com 10 a 15 clínicas parceiras.",
        styles["Body"],
    ))

    story.append(Paragraph("18.5&nbsp;&nbsp;WIP (Work in Progress)", styles["H2Section"]))
    story.append(Paragraph(
        "<b>Definição:</b> limite máximo de itens simultâneos por coluna do "
        "Kanban, que reduz gargalos e o tempo de ciclo (Anderson, 2010). "
        "<b>Medição:</b> contagem de itens por coluna no quadro do GitHub "
        "Projects (Backlog &rarr; Todo &rarr; In Progress &rarr; In Review "
        "&rarr; Done). Os limites foram definidos na retrospectiva das Sprints "
        "1 a 3. O gráfico compara o limite e o WIP médio observado no período "
        "de estabilidade (Sprints 4 e 5).",
        styles["Body"],
    ))
    story.append(caption("Figura 9 - WIP médio versus limite por coluna", styles))
    story.append(WipChart(
        rows=[("Todo", 15, 8.5), ("In Progress", 3, 2.1), ("In Review", 5, 2.8)],
        xmax=15,
        width=CONTENT_W,
    ))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Paragraph(
        "O WIP médio de 2,1 itens em <i>In Progress</i> (limite 3, equivalente "
        "a um item por desenvolvedor) revela fluxo saudável com margem de "
        "segurança, sem situações de bloqueio. O <i>throughput</i> de 6,2 "
        "pontos por dia mantém o tempo de espera em revisão abaixo do alvo de "
        "3 dias.",
        styles["Body"],
    ))

    story.append(Paragraph("18.6&nbsp;&nbsp;Quadro-resumo dos Indicadores", styles["H2Section"]))
    rows = [["Métrica", "Valor atual", "Meta", "Status"]]
    resumo = [
        ("Velocidade média", "43,4 pts/sprint", "&ge; 40 pts/sprint", "Atingida"),
        ("Tempo de ciclo médio", "2,5 dias", "&lt; 3 dias", "Atingida"),
        ("Taxa de aprovação (cenários)", "100% (21/21)", "&ge; 98%", "Atingida"),
        ("Taxa de defeitos", "4,2% (4/96)", "&lt; 10%", "Atingida"),
        ("Defect Removal Efficiency", "100%", "100%", "Atingida"),
        ("NPS", "66,7", "&ge; 50", "Atingida"),
        ("WIP (In Progress)", "2,1 itens", "&le; 3 itens", "Atingida"),
        ("Cobertura de RF (MVP)", "14/14", "100%", "Atingida"),
        ("Taxa de sucesso de build (CI)", "98%", "&ge; 99%", "Parcial"),
    ]
    for r in resumo:
        rows.append(list(r))
    story.append(caption("Quadro 13 - Quadro-resumo dos indicadores ágeis", styles))
    story.append(styled_table(rows, [5.6 * cm, 3.8 * cm, 3.4 * cm, 2.2 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Paragraph(
        "<b>Parecer de consolidação:</b> o FastInBox encerra as Sprints 1 a 5 "
        "com qualidade robusta (zero defeitos bloqueantes, DRE de 100%, "
        "aprovação de 100% nos cenários), velocidade previsível (43,4 "
        "pontos/sprint, ciclo de 2,5 dias), fluxo Kanban eficiente (WIP de 2,1) "
        "e satisfação de stakeholders validada (NPS de 66,7), constituindo "
        "base sólida para a continuidade no Projeto Integrador IV.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def rastreabilidade_story(styles):
    story = [Paragraph("19&nbsp;&nbsp;Rastreabilidade dos Requisitos", styles["H1Section"])]
    story.append(Paragraph(
        "O Documento de Visão e o Backlog do Produto, estabelecidos no início do "
        "ciclo e priorizados em seguida por valor para o parceiro e viabilidade "
        "técnica, constituem a <b>âncora de verdade</b> do projeto: cada linha de "
        "código possui justificativa originada no plano inicial. A hierarquia de "
        "desdobramento - <b>Visão &rarr; Backlog priorizado &rarr; História de "
        "Usuário &rarr; Regra de Negócio &rarr; Critério de Aceitação &rarr; "
        "tarefa/commit &rarr; entrega</b> - é mantida no ALM (GitHub Projects), "
        "que atua como fonte da verdade com commits, histórico de branches e "
        "status das tarefas. O alinhamento dessa cadeia evita o <i>risco de "
        "produto</i> (entregar funcionalidades tecnicamente estáveis, porém "
        "desprovidas de valor para o parceiro atendido). O quadro a seguir "
        "consolida a rastreabilidade das funcionalidades centrais do MVP.",
        styles["Body"],
    ))
    rows = [["Funcionalidade (origem na Visão)", "RF", "HU", "RNB", "CA", "Entrega (Sprint)"]]
    rastro = [
        ("Pedido white label de marmitas", "RF003, RF004", "HU-008", "RNB-001, RNB-003", "CA-008.1", "Entregue (S1, S3)"),
        ("Acesso do paciente por código único", "RF005", "HU-013", "RNB-002", "CA-002.1", "Entregue (S1)"),
        ("Revisão e confirmação do pedido", "RF006", "HU-014, HU-015", "RNB-002", "CA-015.1", "Entregue (S2)"),
        ("Checkout integrado", "RF007", "HU-016", "RNB-006", "CA-016.1", "Entregue (S3)"),
        ("Painel kanban da cozinha", "RF009, RF010", "HU-020, HU-021", "RNB-007", "CA-021.1", "Entregue (S2, S4)"),
        ("Comissão e relatórios exportáveis", "RF013", "HU-010, HU-027", "RNB-003", "CA-027.1", "Entregue (S5)"),
        ("Dashboard administrativo", "RF011", "HU-023, HU-026", "RNB-007", "CA-023.1", "Entregue (S5)"),
        ("Trilha de auditoria de eventos", "RF014", "HU-025", "RNB-005", "CA-025.1", "Entregue (S3, S5)"),
    ]
    for r in rastro:
        rows.append(list(r))
    story.append(caption("Quadro 14 - Matriz de rastreabilidade dos requisitos", styles))
    story.append(styled_table(rows, [4.0 * cm, 1.7 * cm, 1.7 * cm, 2.0 * cm, 2.0 * cm, 4.6 * cm], styles))
    story.append(fonte("elaborado pela equipe FastInBox (2026).", styles))
    story.append(Paragraph(
        "Além das funcionalidades acima, o ambiente de ALM mantém o vínculo "
        "fino entre tarefas, <i>commits</i> e <i>pull requests</i> em "
        "<i>main</i> protegida, de modo que cada entrega seja auditável da "
        "necessidade do parceiro até o artefato publicado em produção.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def conclusao_story(styles):
    story = [Paragraph("21&nbsp;&nbsp;Conclusão e Próximos Passos", styles["H1Section"])]
    story.append(Paragraph(
        "Neste marco de controle, o FastInBox apresenta maturidade técnica "
        "compatível com a fase de <b>Avaliação (todos envolvidos)</b> do "
        "framework Fases_ACE: o ciclo de desenvolvimento web encontra-se "
        "consolidado e a rastreabilidade integral - da Visão ao código em "
        "produção - é o que separa um projeto profissional de uma "
        "implementação amadora. A entrega reúne MVP web funcional e publicado, "
        "100% de aprovação nos cenários de teste, governança ágil mantida por "
        "Daily Scrums e ALM, e indicadores de qualidade e produtividade dentro "
        "das metas (Seção 18), atendendo às competências C19 (Garantia de "
        "Qualidade) e C21 (Gerenciamento de Projetos).",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Com o encerramento das Sprints #06 e #07, o ciclo do MVP foi "
        "concluído e levado a produção, conforme detalhado a seguir:",
        styles["Body"],
    ))
    story.extend(bullet_list([
        "<b>O quê:</b> escala comercial na Sprint #06 (autoatendimento do "
        "paciente por código, assinaturas recorrentes e previsão de demanda) e "
        "go-live na Sprint #07.",
        "<b>Como:</b> hardening final (security headers, rate limiting), "
        "readiness e smoke de release verde, com runbooks e checklist de "
        "go-live assinados.",
        "<b>Quem:</b> execução conforme o Sprint Backlog no ALM, com o quadro "
        "da equipe definido por perfil (produto, back, front e "
        "arquitetura/QA).",
    ], styles))
    story.append(Paragraph(
        "Com a cadeia de evidências preservada - da Visão ao código em "
        "produção - a 3ª Avaliação Parcial (26/06), que representa 50% da "
        "menção final, é sustentada por artefatos rastreáveis. A diretriz "
        "mantida foi o rigor técnico e a governança via ALM, garantindo a "
        "integridade do produto entregue ao parceiro e a base para a evolução "
        "pós-go-live.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def marketing_story(styles):
    story = [Paragraph(
        '20&nbsp;&nbsp;Marketing Digital '
        '(PI IV)',
        styles["H1Section"],
    )]
    story.append(Paragraph(
        "Esta seção consolida o plano de marketing digital previsto para a etapa "
        "do Projeto Integrador IV, na qual o produto entrará em fase de "
        "validação comercial com clínicas reais. O plano combina a abordagem "
        "tradicional dos 4 Ps de McCarthy (1960) - Produto, Preço, Praça, "
        "Promoção - com a leitura contemporânea dos 4 Cs de Lauterborn (1990) - "
        "Cliente, Custo, Conveniência, Comunicação - de modo a centrar a "
        "mensagem nas dores percebidas pelas personas-alvo. Os artefatos "
        "abaixo serão executados com base no MVP entregue no PI III, "
        "alimentando o ciclo Build-Measure-Learn de Ries (2011) com métricas "
        "objetivas de aquisição, ativação e retenção.",
        styles["Body"],
    ))

    story.append(Paragraph("20.1&nbsp;&nbsp;Plano de Marketing", styles["H2Section"]))
    plano = [
        "<b>Estratégia de Monetização:</b> comissão progressiva por pedido + "
        "plano de assinatura para clínicas com volume superior a 100 pedidos/mês "
        "+ serviços premium de analytics.",
        "<b>Estratégia de Divulgação do Produto:</b> conteúdo de SEO orientado a "
        "nutricionistas (palavras-chave: 'plataforma nutricionista', 'venda de "
        "marmitas personalizadas'), Instagram da FastInBox com cases de clínicas, "
        "presença em comunidades de profissionais de nutrição e webinars.",
        "<b>Estratégia de Aquisição de Clientes:</b> programa de indicação para "
        "nutricionistas, parcerias com associações profissionais e onboarding "
        "guiado gratuito nos primeiros 30 dias.",
        "<b>Estratégia de Formação de Preços:</b> taxa de comissão de 5 a 10% "
        "por pedido conforme volume; plano mensal a partir de R$ 199 com "
        "pedidos ilimitados; preço pacote para grandes clínicas.",
        "<b>Desdobramento dos 4 Ps para os 4 Cs:</b> Produto -> Cliente "
        "(plataforma white label que resolve a operação manual do "
        "nutricionista); Preço -> Custo total (redução de retrabalho e tempo); "
        "Praça -> Conveniência (web responsivo, código único, checkout no "
        "fluxo); Promoção -> Comunicação (conteúdo educativo e cases reais).",
    ]
    story.extend(bullet_list(plano, styles))

    story.append(Paragraph("20.2&nbsp;&nbsp;Vídeo Promocional", styles["H2Section"]))
    story.append(Paragraph(
        "Vídeo institucional de 60 a 90 segundos, apresentando o problema "
        "(operação fragmentada da clínica), a proposta de valor (plataforma "
        "white label) e os três perfis em ação. Produção prevista no PI IV "
        "com edição em ferramenta de vídeo aberta.",
        styles["Body"],
    ))

    story.append(Paragraph("20.3&nbsp;&nbsp;Vídeo de Instrução de Uso do Produto", styles["H2Section"]))
    story.append(Paragraph(
        "Série curta de tutoriais (1 a 3 minutos cada) cobrindo: cadastro de "
        "paciente, criação de pedido, configuração da clínica white label, "
        "fluxo do paciente e operação da cozinha. Hospedagem prevista em canal "
        "próprio do FastInBox no YouTube.",
        styles["Body"],
    ))

    story.append(Paragraph("20.4&nbsp;&nbsp;Insights de Mercado (Google Looker)", styles["H2Section"]))
    story.append(Paragraph(
        "Painel de Looker Studio (Google) consolidando volume de pedidos por "
        "clínica, taxa de conversão do paciente, ticket médio, lead time da "
        "cozinha e indicadores de comissão. Indicadores abastecidos por carga "
        "ETL a partir do banco relacional.",
        styles["Body"],
    ))
    story.append(PageBreak())
    return story


def bibliografia_story(styles):
    story = [Paragraph("22&nbsp;&nbsp;Referências", styles["H1Section"])]
    story.append(Paragraph(
        "As referências são apresentadas em ordem alfabética e formatadas "
        "segundo a ABNT NBR 6023:2018, com alinhamento à esquerda, "
        "espaçamento simples interno e o título do documento em destaque.",
        styles["Body"],
    ))
    refs = [
        "ANDERSON, D. J. <b>Kanban</b>: successful evolutionary change for your "
        "technology business. Sequim: Blue Hole Press, 2010.",
        "ASSOCIAÇÃO BRASILEIRA DAS INDÚSTRIAS DA ALIMENTAÇÃO (ABIA). <b>Relatório "
        "anual da indústria da alimentação 2024</b>. São Paulo: ABIA, 2024.",
        "CAROLI, P. <b>Lean Inception</b>: como alinhar pessoas e construir o "
        "produto certo. São Paulo: Caroli.org, 2018.",
        "CENTRO UNIVERSITÁRIO DE BRASÍLIA (CEUB). <b>Plano de ensino</b>: "
        "Projeto Integrador III - Ciência da Computação. Brasília: CEUB, 2026.",
        "COHN, M. <b>Agile estimating and planning</b>. Upper Saddle River: "
        "Prentice Hall, 2005.",
        "COHN, M. <b>Succeeding with agile</b>: software development using Scrum. "
        "Upper Saddle River: Addison-Wesley, 2009.",
        "COMITÊ GESTOR DA INTERNET NO BRASIL (CGI.br). <b>TIC e-commerce "
        "2024</b>: pesquisa sobre o uso das tecnologias de informação e "
        "comunicação nas empresas brasileiras. São Paulo: NIC.br, 2024.",
        "CONSELHO FEDERAL DE NUTRICIONISTAS (CFN). <b>Estatísticas de "
        "profissionais inscritos no Sistema CFN/CRN</b>. Brasília: CFN, 2024.",
        "DATAFOLHA. <b>Hábitos alimentares e saúde no Brasil</b>. São Paulo: "
        "Datafolha, 2024.",
        "GARTNER. <b>Hype cycle for digital commerce</b>. Stamford: Gartner "
        "Inc., 2025.",
        "INSTITUTE OF ELECTRICAL AND ELECTRONICS ENGINEERS (IEEE). <b>IEEE Std "
        "829-2008</b>: standard for software and system test documentation. New "
        "York: IEEE, 2008.",
        "INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). <b>Índice "
        "Nacional de Preços ao Consumidor Amplo (IPCA)</b>. Rio de Janeiro: "
        "IBGE, 2024.",
        "INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. <b>ISO/IEC 25010</b>: "
        "systems and software engineering - systems and software quality "
        "requirements and evaluation (SQuaRE) - system and software quality "
        "models. Geneva: ISO, 2011.",
        "KAN, S. H. <b>Metrics and models in software quality engineering</b>. "
        "2. ed. Boston: Addison-Wesley, 2002.",
        "NIELSEN, J. <b>Usability engineering</b>. San Francisco: Morgan "
        "Kaufmann, 1994.",
        "OLIVEIRA, K. V. R. <b>Guia orientativo - Unidade 2</b>: "
        "desenvolvimento da aplicação web. Material da disciplina Projeto "
        "Integrador III. Brasília: CEUB, 2026.",
        "OSTERWALDER, A.; PIGNEUR, Y. <b>Business model generation</b>: a "
        "handbook for visionaries, game changers, and challengers. Hoboken: "
        "Wiley, 2010.",
        "PRESSMAN, R. S.; MAXIM, B. R. <b>Engenharia de software</b>: uma "
        "abordagem profissional. 9. ed. Porto Alegre: AMGH, 2021.",
        "PROJECT MANAGEMENT INSTITUTE (PMI). <b>A guide to the Project "
        "Management Body of Knowledge (PMBOK Guide)</b>. 7. ed. Newtown Square: "
        "PMI, 2021.",
        "REICHHELD, F. F. The one number you need to grow. <b>Harvard Business "
        "Review</b>, [s. l.], v. 81, n. 12, p. 46-54, 2003.",
        "REINERTSEN, D. G. <b>The principles of product development flow</b>: "
        "second generation lean product development. Redondo Beach: Celeritas, "
        "2009.",
        "RIES, E. <b>A startup enxuta</b>: como os empreendedores atuais "
        "utilizam a inovação contínua. São Paulo: Lua de Papel, 2011.",
        "SCHWABER, K.; SUTHERLAND, J. <b>The Scrum Guide</b>: o guia definitivo "
        "para o Scrum - as regras do jogo. [S. l.]: Scrum.org, 2020.",
        "SEBRAE. <b>Pequenos negócios em números</b>: setor de alimentação fora "
        "do lar. Brasília: Sebrae, 2023.",
        "SOMMERVILLE, I. <b>Engenharia de software</b>. 10. ed. São Paulo: "
        "Pearson, 2019.",
        "W3C - WORLD WIDE WEB CONSORTIUM. <b>Web Content Accessibility "
        "Guidelines (WCAG) 2.1</b>. [S. l.]: W3C, 2018.",
    ]
    ref_style = ParagraphStyle(
        name="ref",
        parent=styles["Body"],
        alignment=TA_LEFT,
        firstLineIndent=0,
        leftIndent=0,
        leading=14,
        spaceAfter=12,
    )
    for r in refs:
        story.append(Paragraph(r, ref_style))
    story.append(PageBreak())
    return story


def apendice_story(styles):
    story = [Paragraph("APÊNDICE A - TECNOLOGIAS UTILIZADAS", styles["H1Section"])]
    story.append(Paragraph(
        "Este apêndice consolida o conjunto completo de tecnologias, "
        "ferramentas e serviços empregados no desenvolvimento, gestão, teste, "
        "publicação e operação do FastInBox. As escolhas seguem três critérios "
        "principais: (i) maturidade e suporte ativo da comunidade, (ii) "
        "aderência ao modelo de operação SaaS multi-perfil, (iii) "
        "compatibilidade com pipelines CI/CD em GitHub Actions. Acesso "
        "completo das ferramentas concedido para "
        '<font color="#1F4E79">kadidja.oliveira@ceub.edu.br</font>.',
        styles["Body"],
    ))

    sections = [
        ("Gestão", [
            "Gestão do Projeto: Trello + GitHub Projects (https://github.com/orgs/fastinbox-repo/projects)",
            "Gestão da Configuração: GitHub (https://github.com/fastinbox-repo) + Google Drive (compartilhado com a equipe)",
        ]),
        ("Desenvolvimento Front-End", [
            "Prototipação: Figma (https://www.figma.com/file/fastinbox-prototype)",
            "Frontend - Aplicativo: não se aplica neste MVP (web responsivo)",
            "Frontend - Aplicação Web: Next.js 15 + React 19 + TypeScript + Tailwind CSS (https://github.com/fastinbox-repo/front)",
        ]),
        ("Desenvolvimento Backend", [
            "API Management: NestJS 10 (Node.js) com OpenAPI/Swagger (https://github.com/fastinbox-repo/back)",
            "Servidor de Aplicação: Railway (https://railway.app) e/ou Heroku (https://www.heroku.com)",
            "Sistema Gerenciador de Banco de Dados: PostgreSQL gerenciado (Neon / Railway)",
        ]),
        ("Testes e Gestão de Demandas", [
            "Automação de Testes: QASE.IO (https://app.qase.io/project/FASTINBOX) + Playwright para E2E",
            "Bug Tracking: GitHub Issues (https://github.com/fastinbox-repo) + GitLab espelho",
        ]),
        ("Analítica", [
            "Extração, Transformação e Carga (ETL): scripts Node.js no Google Drive da equipe",
            "Visualização de Dados: Google Looker Studio (painel da operação FastInBox)",
        ]),
        ("Marketing", [
            "Editoração de Vídeo: CapCut + DaVinci Resolve",
            "Publicação: GitHub Pages (https://fastinbox-repo.github.io/docs/) + Vercel (https://fastinbox.vercel.app)",
            "Redes Sociais: Instagram @fastinbox.app + LinkedIn corporativo",
        ]),
        ("Tecnologias Habilitadoras Digitais", [
            "Inteligência Artificial: assistentes de código (Claude, GitHub Copilot) na fase de desenvolvimento",
            "Business Intelligence: Looker Studio para indicadores operacionais e financeiros",
            "Demais habilitadoras (IoT, 5G, Blockchain, AR/VR, RPA, ML, Deep Learning, Big Data) não aplicadas neste MVP",
        ]),
    ]

    item_style = ParagraphStyle(
        name="ApendiceItem",
        parent=styles["Body"],
        alignment=TA_LEFT,
        leftIndent=18,
        firstLineIndent=-12,
        spaceAfter=4,
    )
    head_style = ParagraphStyle(
        name="ApendiceHead",
        parent=styles["Body"],
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=4,
    )
    for title, items in sections:
        story.append(Paragraph(f"<b>&#10070; {title}</b>", head_style))
        for it in items:
            story.append(Paragraph(f"&#10070;&nbsp;&nbsp;{it}", item_style))
        story.append(Spacer(1, 0.1 * cm))
    return story


# ----------------------------------------------------------------------------
# Document template
# ----------------------------------------------------------------------------


class PiDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        # ABNT pagination is handled in footer_canvas via doc.first_textual_page.

        # Cover (portrait, no pagination) - capa is not counted
        cover_frame = Frame(
            2.5 * cm, 1.5 * cm,
            PAGE_W - 5 * cm, PAGE_H - 3 * cm,
            id="cover",
        )
        # Body (portrait): ABNT margins left/top 3 cm, right/bottom 2 cm
        body_frame = Frame(
            3 * cm, 2 * cm,
            CONTENT_W, PAGE_H - 5 * cm,
            id="body",
        )
        # EAP (landscape): left/top 3 cm, right/bottom 2 cm
        eap_frame = Frame(
            2 * cm, 2 * cm,
            LAND_W - 4 * cm, LAND_H - 4 * cm,
            id="eap",
        )

        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame], onPage=cover_canvas, pagesize=A4),
            PageTemplate(id="body", frames=[body_frame], onPage=footer_canvas, pagesize=A4),
            PageTemplate(id="eap_landscape", frames=[eap_frame], onPage=footer_canvas, pagesize=landscape(A4)),
        ])


def main():
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = PiDoc(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=3 * cm,
        rightMargin=2 * cm,
        topMargin=3 * cm,
        bottomMargin=2 * cm,
        title="FastInBox - Projeto Integrador III",
        author="Equipe FastInBox",
    )
    doc.first_textual_page = 10  # ABNT: numbers shown from the first textual page

    story = []
    story.extend(cover_story(styles))
    story.extend(folha_rosto_story(styles))
    story.extend(resumo_story(styles))
    story.extend(lista_figuras_story(styles))
    story.extend(lista_quadros_story(styles))
    story.extend(lista_tabelas_story(styles))
    story.extend(glossary_story(styles))
    story.extend(toc_story(styles))
    story.extend(descricao_story(styles))
    story.extend(eap_story(styles))
    story.extend(problema_story(styles))
    story.extend(bmc_story(styles))
    story.extend(cenarios_beneficios_publico_story(styles))
    story.extend(cronograma_story(styles))
    story.extend(requisitos_funcionais_story(styles))
    story.extend(requisitos_nao_funcionais_story(styles))
    story.extend(prototipo_story(styles))
    story.extend(mvp_story(styles))
    story.extend(modelo_dados_story(styles))
    story.extend(testes_story(styles))
    story.extend(historias_criterios_story(styles))
    story.extend(regras_negocio_story(styles))
    story.extend(sprint5_story(styles))
    story.extend(metricas_story(styles))
    story.extend(rastreabilidade_story(styles))
    story.extend(marketing_story(styles))
    story.extend(conclusao_story(styles))
    story.extend(bibliografia_story(styles))
    story.extend(apendice_story(styles))

    doc.build(story)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
