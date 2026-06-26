import logging
import os
import unicodedata
import uuid
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pypdf import PdfReader, PdfWriter

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "generated_docs")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

_jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)

_LOGO_PATH        = os.path.join(TEMPLATES_DIR, "eniad_logo.png")
_BANNER_ATT_PATH  = os.path.join(TEMPLATES_DIR, "eniad_header_banner.png")
_BANNER_CONV_PATH = os.path.join(TEMPLATES_DIR, "logo-convention-stage.png")
_BANNER_REGL_PATH = os.path.join(TEMPLATES_DIR, "logo_reglement.png")
_REGLEMENT_PDF_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "data", "reglement interieure.pdf")
)
_CONVENTION_PDF_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "data", "convention de stage.pdf")
)
_log = logging.getLogger(__name__)


def _img_b64(path: str) -> str:
    """Return any PNG as a base64 data URI for embedding in xhtml2pdf."""
    import base64
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def _logo_url() -> str:
    """Return the diamond logo as a base64 data URI."""
    return _img_b64(_ensure_logo())


def _banner_url(path: str) -> str:
    """Return the header banner image for the given path as a base64 data URI."""
    return _img_b64(path)


def _generate_banner():
    """Create the official ENIAD header banner PNG using Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import arabic_reshaper
        from bidi.algorithm import get_display

        def ar(text):
            return get_display(arabic_reshaper.reshape(text))

        W, H = 1050, 130
        img = Image.new("RGB", (W, H), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        MAROON   = (135, 50, 50)
        D_MAROON = ( 90, 25, 25)
        GOLD     = (175, 140, 70)
        CREAM    = (245, 235, 200)
        BLACK    = (  0,   0,  0)

        draw.rectangle([0, 0, W-1, H-1], outline=MAROON, width=3)

        cx, cy = W // 2, H // 2
        for half, fill, outline in [
            (58, MAROON,   MAROON),
            (52, D_MAROON, GOLD),
            (46, MAROON,   MAROON),
            (40, D_MAROON, GOLD),
            (34, MAROON,   MAROON),
            (28, D_MAROON, GOLD),
            (22, MAROON,   MAROON),
            (16, D_MAROON, GOLD),
            (10, CREAM,    CREAM),
            ( 6, D_MAROON, D_MAROON),
        ]:
            pts = [(cx, cy-half), (cx+half, cy), (cx, cy+half), (cx-half, cy)]
            draw.polygon(pts, fill=fill, outline=outline)

        for sign in (-1, 1):
            base_x = cx + sign * 75
            for i, sz in enumerate([18, 13, 8]):
                ox = base_x + sign * i * 5
                pts = [(ox, cy - sz), (ox + sign * sz, cy), (ox, cy + sz)]
                draw.polygon(pts, fill=MAROON)

        for x_off in [-130, 130]:
            draw.line([(cx + x_off, 8), (cx + x_off, H - 8)], fill=MAROON, width=1)

        def load(paths, sz):
            for p in paths:
                try:
                    return ImageFont.truetype(p, sz)
                except Exception:
                    pass
            return ImageFont.load_default()

        fn_ar_big = load(["C:/Windows/Fonts/Tahoma.ttf"], 14)
        fn_ar_sub = load(["C:/Windows/Fonts/Tahoma.ttf"], 10)
        fn_fr_big = load(["C:/Windows/Fonts/Arialbd.ttf", "C:/Windows/Fonts/arialbd.ttf"], 10)
        fn_fr_sub = load(["C:/Windows/Fonts/Arial.ttf", "C:/Windows/Fonts/arial.ttf"], 9)

        def ctext(text, font, color, center_x, y):
            bb = draw.textbbox((0, 0), text, font=font)
            w = bb[2] - bb[0]
            draw.text((center_x - w // 2, y), text, fill=color, font=font)

        left_cx  = cx - 200
        right_cx = cx + 200

        ctext(ar("جامعة محمد الأول وجدة"),   fn_ar_big, MAROON,   left_cx, cy - 32)
        ctext(ar("+nOAURt ICSACCiA AJLinOS"), fn_ar_sub, D_MAROON, left_cx, cy - 14)
        ctext("UNIVERSITE MOHAMMED PREMIER OUJDA", fn_fr_big, BLACK, left_cx, cy + 10)

        ctext(ar("المدرسة الوطنية للذكاء الاصطناعي والرقمنة بركان"), fn_ar_sub, MAROON,   right_cx, cy - 32)
        ctext(ar("تاسست 1470هـ  1747م  4054هـ ATOSIEEN"),            fn_ar_sub, D_MAROON, right_cx, cy - 16)
        ctext("Ecole Nationale de l'Intelligence",                    fn_fr_sub, BLACK,    right_cx, cy + 4)
        ctext("Artificielle et du Digital Berkane",                   fn_fr_sub, BLACK,    right_cx, cy + 18)

        os.makedirs(TEMPLATES_DIR, exist_ok=True)
        img.save(_BANNER_ATT_PATH, "PNG", dpi=(150, 150))
    except Exception as exc:
        _log.error(f"Impossible de générer le banner ENIAD: {exc}")


def _ensure_logo() -> str:
    """Return the logo absolute path, generating a placeholder if the file is missing."""
    if os.path.exists(_LOGO_PATH):
        return os.path.abspath(_LOGO_PATH)
    _log.warning(
        "Logo ENIAD introuvable — génération d'un placeholder. "
        "Placez le logo officiel dans backend/templates/eniad_logo.png"
    )
    try:
        from PIL import Image, ImageDraw, ImageFont
        size = 200
        img = Image.new("RGB", (size, size), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, 196, 196], fill=(120, 40, 40), outline=(90, 25, 25), width=3)
        draw.ellipse([18, 18, 182, 182], fill=(100, 30, 30), outline=(180, 130, 60), width=2)
        draw.ellipse([30, 30, 170, 170], fill=(120, 40, 40))
        # Concentric diamonds
        cx, cy = size // 2, size // 2
        for h, fill, outline in [
            (65, (90, 25, 25), (180, 130, 60)),
            (50, (120, 40, 40), (200, 160, 80)),
            (32, (240, 225, 195), (180, 130, 60)),
            (14, (90, 25, 25), (90, 25, 25)),
        ]:
            pts = [(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy)]
            draw.polygon(pts, fill=fill, outline=outline)
        try:
            font_big = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
            font_sm = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 11)
        except Exception:
            font_big = ImageFont.load_default()
            font_sm = font_big
        for text, y, font, color in [
            ("ENIAD", 76, font_big, (255, 255, 255)),
            ("BERKANE", 110, font_sm, (240, 210, 150)),
        ]:
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            draw.text(((size - w) // 2, y), text, fill=color, font=font)
        os.makedirs(TEMPLATES_DIR, exist_ok=True)
        img.save(_LOGO_PATH, "PNG")
        return os.path.abspath(_LOGO_PATH)
    except Exception as exc:
        _log.error(f"Impossible de générer le logo placeholder: {exc}")
        return _LOGO_PATH  # return path anyway; template will show broken img rather than nothing


# Ensure logo and attestation banner exist at import time
_ensure_logo()
if not os.path.exists(_BANNER_ATT_PATH):
    _generate_banner()


_PT_TO_MM = 25.4 / 72  # 1 PDF point → mm


def _fill_reglement_from_official(user_data: dict) -> bytes:
    """Copy pages 1-5 of the official règlement PDF unchanged, then overlay
    student data fields on page 6 (the engagement/signature page)."""
    reader = PdfReader(_REGLEMENT_PDF_PATH)
    writer = PdfWriter()

    # Copy pages 1-5 verbatim
    for i in range(min(5, len(reader.pages))):
        writer.add_page(reader.pages[i])

    if len(reader.pages) >= 6:
        page6 = reader.pages[5]

        # Build a transparent overlay with fpdf2 (A4, mm units)
        overlay = FPDF(unit="mm", format="A4")
        overlay.set_margins(0, 0, 0)
        overlay.set_auto_page_break(False)
        overlay.add_page()
        overlay.set_font("Helvetica", size=9)
        overlay.set_text_color(0, 0, 0)

        def place(x_pt: float, y_pt: float, text: str):
            overlay.set_xy(x_pt * _PT_TO_MM, y_pt * _PT_TO_MM)
            overlay.cell(0, 4, text[:80])

        full_name  = user_data.get("full_name", "")
        cin        = user_data.get("cin", "")
        annee      = str(user_data.get("annee", ""))
        is_ci      = user_data.get("is_ci", False)
        filiere    = user_data.get("filiere", "")
        date_sig   = user_data.get("date_signature",
                                    datetime.now().strftime("%d/%m/%Y"))

        # Coordinates extracted with pdfplumber from page 6 of official PDF
        place(111.3, 578.3, full_name)
        place( 65.5, 595.9, cin)
        place(100.0, 613.5, annee)
        # Tick the correct cycle checkbox
        if is_ci:
            place(189.1, 612.5, "X")
        else:
            place(225.4, 612.5, "X")
        place(280.0, 613.5, filiere)
        place(420.3, 677.9, date_sig)

        overlay_bytes  = bytes(overlay.output())
        overlay_reader = PdfReader(BytesIO(overlay_bytes))
        page6.merge_page(overlay_reader.pages[0])
        writer.add_page(page6)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _fill_convention_from_official(user_data: dict) -> bytes:
    """Copy official convention de stage PDF and overlay student/company data."""
    reader = PdfReader(_CONVENTION_PDF_PATH)
    writer = PdfWriter()

    full_name   = user_data.get("full_name", "")
    major       = user_data.get("major", "")
    annee_label = user_data.get("annee_label", "")
    entreprise  = user_data.get("entreprise", "")
    adresse     = user_data.get("adresse_entreprise", "")
    telephone   = user_data.get("telephone", "")
    fax         = user_data.get("fax", "")
    tuteur      = user_data.get("tuteur", "")
    date_debut  = user_data.get("date_debut", "")
    date_fin    = user_data.get("date_fin", "")
    date_sig    = user_data.get("date_signature", datetime.now().strftime("%d/%m/%Y"))

    def make_overlay(dot_fields=None, plain_fields=None):
        """
        dot_fields:   [(x0_pt, y0_pt, x1_pt, y1_pt, text), ...]
            Clears the dots with a white rect, writes text, redraws underline.
        plain_fields: [(x0_pt, y0_pt, x1_pt, y1_pt, text), ...]
            Writes text in blank areas (signature blocks, no dots to erase).
        """
        ov = FPDF(unit="mm", format="A4")
        ov.set_margins(0, 0, 0)
        ov.set_auto_page_break(False)
        ov.add_page()
        ov.set_text_color(0, 0, 0)

        for x0, y0, x1, y1, text in (dot_fields or []):
            if not text:
                continue
            x = x0 * _PT_TO_MM
            y = y0 * _PT_TO_MM
            w = (x1 - x0) * _PT_TO_MM
            h = (y1 - y0) * _PT_TO_MM
            # Erase dots with white rectangle
            ov.set_fill_color(255, 255, 255)
            ov.rect(x, y, w, h + 0.4, 'F')
            # Write value in matching body font
            ov.set_font("Helvetica", size=10)
            ov.set_xy(x + 1, y)
            ov.cell(w - 1, h, str(text)[:80], align='L')
            # Redraw thin underline to keep form appearance
            ov.set_draw_color(120, 120, 120)
            ov.set_line_width(0.25)
            ov.line(x, y + h, x + w, y + h)

        for x0, y0, x1, y1, text in (plain_fields or []):
            if not text:
                continue
            x = x0 * _PT_TO_MM
            y = y0 * _PT_TO_MM
            w = (x1 - x0) * _PT_TO_MM
            h = (y1 - y0) * _PT_TO_MM
            ov.set_font("Helvetica", size=10)
            ov.set_xy(x, y)
            ov.cell(w, h, str(text)[:60], align='L')

        return bytes(ov.output())

    # ── Page 1: company info + student identity + dates ──────────────────────
    # Coordinates: (x0_pt, y0_pt, x1_pt, y1_pt) from pdfplumber (top-left origin)
    page1 = reader.pages[0]
    ov1 = PdfReader(BytesIO(make_overlay(dot_fields=[
        (141.7, 224.8, 509.8, 233.8, entreprise),
        (122.4, 250.6, 511.0, 259.6, adresse),
        ( 95.3, 275.4, 293.0, 284.4, telephone),
        (356.9, 275.4, 511.4, 284.4, fax),
        (128.4, 541.4, 479.0, 551.3, major),
        (277.8, 554.9, 482.1, 564.9, full_name),
        (146.8, 569.5, 188.6, 579.4, annee_label),
        (205.0, 639.4, 380.0, 649.4, date_debut),
        (398.5, 640.9, 510.0, 648.9, date_fin),
    ])))
    page1.merge_page(ov1.pages[0])
    writer.add_page(page1)

    # ── Page 2: date signature + name blocks ─────────────────────────────────
    if len(reader.pages) >= 2:
        page2 = reader.pages[1]
        ov2 = PdfReader(BytesIO(make_overlay(
            dot_fields=[
                (441.2, 588.8, 510.0, 597.8, date_sig),
            ],
            plain_fields=[
                ( 81.1, 649.0, 270.0, 659.0, tuteur),
                (263.3, 708.0, 430.0, 718.0, full_name),
            ],
        )))
        page2.merge_page(ov2.pages[0])
        writer.add_page(page2)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _html_to_pdf(html: str) -> bytes:
    """Convert rendered HTML string to PDF bytes via xhtml2pdf."""
    from xhtml2pdf import pisa
    buf = BytesIO()
    status = pisa.CreatePDF(html, dest=buf, encoding="utf-8")
    if status.err:
        raise RuntimeError(f"xhtml2pdf error: {status.err}")
    return buf.getvalue()


def _render_template(template_name: str, context: dict) -> bytes:
    """Render a Jinja2 HTML template and convert to PDF bytes."""
    tmpl = _jinja_env.get_template(template_name)
    html = tmpl.render(**context)
    return _html_to_pdf(html)

# ── Strict whitelist ──────────────────────────────────────────────────────────
# Only these three document types may ever be generated.
# Adding a new type requires updating this list AND adding a generator method.
ALLOWED_DOC_TYPES = [
    "Convention de stage",
    "Attestation de scolarite",
    "Reglement de l'ecole",
]

# Aliases accepted from the LLM / Flutter app (normalised → canonical)
_ALIASES: dict[str, str] = {
    "convention de stage":           "Convention de stage",
    "convention stage":              "Convention de stage",
    "stage":                         "Convention de stage",
    "attestation de scolarite":      "Attestation de scolarite",
    "attestation scolarite":         "Attestation de scolarite",
    "attestation":                   "Attestation de scolarite",
    "reglement de l'ecole":          "Reglement de l'ecole",
    "reglement de lecole":           "Reglement de l'ecole",
    "reglement interieur":           "Reglement de l'ecole",
    "reglement":                     "Reglement de l'ecole",
}


def _normalize(s: str) -> str:
    """Lowercase + strip accents for fuzzy matching."""
    nfkd = unicodedata.normalize("NFKD", s.lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def resolve_doc_type(raw: str) -> str:
    """Return the canonical doc type or raise ValueError."""
    key = _normalize(raw)
    canonical = _ALIASES.get(key)
    if canonical is None:
        raise ValueError(
            f"Type de document non autorise: '{raw}'. "
            f"Types valides: {', '.join(ALLOWED_DOC_TYPES)}"
        )
    return canonical


def _ensure_docs_dir():
    os.makedirs(DOCS_DIR, exist_ok=True)


# ── PDF base class ────────────────────────────────────────────────────────────

class _PDF(FPDF):
    def __init__(self, doc_title: str):
        super().__init__()
        self._doc_title = doc_title
        self.set_margins(20, 30, 20)
        self.add_page()
        self.set_auto_page_break(auto=True, margin=25)
        self._draw_header()

    def _draw_header(self):
        self.set_fill_color(0, 82, 165)
        self.rect(0, 0, 210, 28, "F")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 5)
        self.cell(190, 8, "ECOLE NATIONALE DE L'INTELLIGENCE ARTIFICIELLE ET DU DIGITAL",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_x(10)
        self.cell(190, 6, "ENIAD - Berkane, Maroc", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(8)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, self._doc_title.upper(), align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 82, 165)
        self.set_line_width(0.8)
        y = self.get_y()
        self.line(20, y, 190, y)
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(200, 200, 200)
        self.line(20, self.get_y(), 190, self.get_y())
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0, 6,
            f"Genere par SmartStudent | ENIAD Berkane | {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            align="C",
        )

    def signature_block(self):
        self.ln(14)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.cell(90, 8, f"Berkane, le {datetime.now().strftime('%d/%m/%Y')}",
                  new_x="RIGHT", new_y="TMARGIN")
        self.cell(90, 8, "", new_x="LMARGIN", new_y="NEXT")
        self.cell(90, 8, "", new_x="RIGHT", new_y="TMARGIN")
        self.set_font("Helvetica", "B", 11)
        self.cell(90, 8, "Le Directeur", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(130, 130, 130)
        self.cell(90, 6, "", new_x="RIGHT", new_y="TMARGIN")
        self.cell(90, 6, "(Signature et cachet)", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)


# ── DocumentsAgent ────────────────────────────────────────────────────────────

class DocumentsAgent:

    def generate(self, doc_type: str, user_data: dict) -> tuple[str, bytes]:
        """Generate a PDF. Returns (doc_id, pdf_bytes).

        Raises ValueError for any doc_type not in ALLOWED_DOC_TYPES.
        Each generator receives only the keys it needs — no cross-module data.
        """
        _ensure_docs_dir()

        canonical = resolve_doc_type(doc_type)

        dispatch = {
            "Convention de stage":       self._convention_stage,
            "Attestation de scolarite":  self._attestation_scolarite,
            "Reglement de l'ecole":      self._reglement_ecole,
        }
        gen_fn = dispatch[canonical]
        pdf_bytes = gen_fn(canonical, user_data)

        doc_id = str(uuid.uuid4())
        path = os.path.join(DOCS_DIR, f"{doc_id}.pdf")
        with open(path, "wb") as f:
            f.write(pdf_bytes)

        return doc_id, pdf_bytes

    def get_path(self, doc_id: str):
        path = os.path.join(DOCS_DIR, f"{doc_id}.pdf")
        return path if os.path.exists(path) else None

    # ── Generator: Attestation poursuite d'études ────────────────────────────
    # Rendered from the official ENIAD HTML template (attestation_scolarite.html).
    # Uses: identity + enrollment fields ONLY.
    # Must NOT access: grades, company info, internship dates.

    def _attestation_scolarite(self, _, user_data: dict) -> bytes:
        full_name = user_data.get("full_name", "")
        parts     = full_name.split()
        first     = user_data.get("first_name") or (parts[0] if parts else "")
        last      = user_data.get("last_name")  or (" ".join(parts[1:]) if len(parts) > 1 else "")

        # Display name: LAST_NAME Prénom
        display_name = (
            f"{last.upper()} {first.capitalize()}"
            if (last or first) else full_name.upper()
        )

        cne           = user_data.get("cne")           or "________________"
        date_naissance = user_data.get("date_naissance") or "________________"
        major         = user_data.get("major")         or "Génie Informatique"
        year_level    = user_data.get("year")          or 1

        # Academic year — dynamic from current date, separator "/"
        now = datetime.now()
        yr  = now.year if now.month >= 9 else now.year - 1
        annee_univ = (user_data.get("annee_universitaire") or f"{yr}/{yr + 1}").replace("-", "/")

        _levels = {
            1: "Première année",  2: "Deuxième année",   3: "Troisième année",
            4: "Quatrième année", 5: "Cinquième année",
        }
        try:
            niveau = _levels.get(int(year_level), f"Année {year_level}")
        except (TypeError, ValueError):
            niveau = "Première année"

        context = {
            "header_url":         _banner_url(_BANNER_ATT_PATH),
            "nom":                display_name,
            "date_naissance":     date_naissance,
            "cne":                cne,
            "major":              major,
            "niveau":             niveau,
            "annee_universitaire": annee_univ,
            "issuance_date":      now.strftime("%d/%m/%Y"),
        }
        return _render_template("attestation_scolarite.html", context)

    # ── Generator: Convention de Stage ───────────────────────────────────────
    # Rendered from the official ENIAD Jinja2 HTML template.
    # Uses: identity + enrollment + internship fields ONLY.
    # Must NOT access: grades, exam scores, complaints, or any academic data.

    def _convention_stage(self, _, user_data: dict) -> bytes:
        full_name = user_data.get("full_name") or "L'étudiant(e)"
        major     = user_data.get("major") or "Génie Informatique"
        year_raw  = user_data.get("year", 3)

        # Internship-specific fields — never sourced from academic modules
        entreprise         = user_data.get("entreprise") or ""
        adresse_entreprise = user_data.get("adresse_entreprise") or ""
        telephone          = user_data.get("telephone") or ""
        fax                = user_data.get("fax") or ""
        tuteur             = user_data.get("tuteur") or ""
        poste              = user_data.get("poste") or "Stage de fin d'études"
        date_debut         = user_data.get("date_debut") or ""
        date_fin           = user_data.get("date_fin") or ""

        # Map year integer to ordinal label (French)
        _year_labels = {1: "1ère", 2: "2ème", 3: "3ème", 4: "4ème", 5: "5ème"}
        annee_label = _year_labels.get(int(year_raw) if year_raw else 3, "3ème")

        if os.path.exists(_CONVENTION_PDF_PATH):
            return _fill_convention_from_official({
                "full_name":          full_name,
                "major":              major,
                "annee_label":        annee_label,
                "entreprise":         entreprise,
                "adresse_entreprise": adresse_entreprise,
                "telephone":          telephone,
                "fax":                fax,
                "tuteur":             tuteur,
                "date_debut":         date_debut,
                "date_fin":           date_fin,
                "date_signature":     datetime.now().strftime("%d/%m/%Y"),
            })

        # Fallback: HTML template
        context = {
            "header_url":         _banner_url(_BANNER_CONV_PATH),
            "entreprise":         entreprise,
            "adresse_entreprise": adresse_entreprise,
            "telephone":          telephone,
            "fax":                fax,
            "nom_etudiant":       full_name,
            "specialite":         major,
            "annee_label":        annee_label,
            "tuteur":             tuteur,
            "poste":              poste,
            "date_debut":         date_debut,
            "date_fin":           date_fin,
            "date_signature":     datetime.now().strftime("%d/%m/%Y"),
        }
        return _render_template("convention_stage.html", context)

    # ── Generator: Reglement de l'Ecole ──────────────────────────────────────
    # Faithful reproduction of the official ENIAD 6-page, 31-article document.
    # Student identity is used only for the engagement signature section (last page).

    def _reglement_ecole(self, _, user_data: dict) -> bytes:
        full_name = user_data.get("full_name") or ""
        cin       = user_data.get("cin") or ""
        year_raw  = user_data.get("year", "")
        filiere   = user_data.get("major") or ""

        # Determine cycle: CP = years 1-2, CI = years 3-5
        try:
            year_int = int(year_raw)
        except (TypeError, ValueError):
            year_int = 0
        is_ci = year_int >= 3

        if os.path.exists(_REGLEMENT_PDF_PATH):
            return _fill_reglement_from_official({
                "full_name":      full_name,
                "cin":            cin,
                "annee":          str(year_raw) if year_raw else "",
                "is_ci":          is_ci,
                "filiere":        filiere,
                "date_signature": datetime.now().strftime("%d/%m/%Y"),
            })

        # Fallback: HTML template (used when official PDF is not present)
        context = {
            "header_url":     _banner_url(_BANNER_REGL_PATH),
            "nom_etudiant":   full_name,
            "cin":            cin,
            "annee":          str(year_raw) if year_raw else "",
            "is_ci":          is_ci,
            "filiere":        filiere,
            "date_signature": datetime.now().strftime("%d/%m/%Y"),
        }
        return _render_template("reglement_interieur.html", context)


_agent = DocumentsAgent()


def get_documents_agent() -> DocumentsAgent:
    return _agent
