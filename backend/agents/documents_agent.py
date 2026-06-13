import os
import uuid
from datetime import datetime
from fpdf import FPDF

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "generated_docs")


def _ensure_docs_dir():
    os.makedirs(DOCS_DIR, exist_ok=True)


class _PDF(FPDF):
    def __init__(self, doc_title: str):
        super().__init__()
        self._doc_title = doc_title
        self.set_margins(20, 30, 20)
        self.add_page()
        self.set_auto_page_break(auto=True, margin=25)
        self._draw_header()

    def _draw_header(self):
        # Blue banner
        self.set_fill_color(0, 82, 165)
        self.rect(0, 0, 210, 28, "F")
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 5)
        self.cell(190, 8, "ECOLE NATIONALE DE L'INTELLIGENCE ARTIFICIELLE ET DU DIGITAL", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_x(10)
        self.cell(190, 6, "ENIAD - Berkane, Maroc", align="C", new_x="LMARGIN", new_y="NEXT")
        # Title
        self.set_text_color(0, 0, 0)
        self.ln(8)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, self._doc_title.upper(), align="C", new_x="LMARGIN", new_y="NEXT")
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
        self.cell(90, 8, f"Berkane, le {datetime.now().strftime('%d/%m/%Y')}", new_x="RIGHT", new_y="TMARGIN")
        self.cell(90, 8, "", new_x="LMARGIN", new_y="NEXT")
        self.cell(90, 8, "", new_x="RIGHT", new_y="TMARGIN")
        self.set_font("Helvetica", "B", 11)
        self.cell(90, 8, "Le Directeur", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(130, 130, 130)
        self.cell(90, 6, "", new_x="RIGHT", new_y="TMARGIN")
        self.cell(90, 6, "(Signature et cachet)", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)


class DocumentsAgent:

    def generate(self, doc_type: str, user_data: dict) -> tuple:
        """Generate PDF. Returns (doc_id, pdf_bytes)."""
        _ensure_docs_dir()
        doc_id = str(uuid.uuid4())

        generators = {
            "Attestation de scolarite": self._attestation_scolarite,
            "Releve de notes": self._releve_notes,
            "Convention de stage": self._convention_stage,
            "Certificat de stage": self._certificat_stage,
            "Demande de redoublement": self._demande_generique,
            "Equivalence / Transfert": self._demande_generique,
            "Autre": self._demande_generique,
        }
        gen_fn = generators.get(doc_type, self._demande_generique)
        pdf_bytes = gen_fn(doc_type, user_data)

        path = os.path.join(DOCS_DIR, f"{doc_id}.pdf")
        with open(path, "wb") as f:
            f.write(pdf_bytes)

        return doc_id, pdf_bytes

    def get_path(self, doc_id: str):
        path = os.path.join(DOCS_DIR, f"{doc_id}.pdf")
        return path if os.path.exists(path) else None

    def _attestation_scolarite(self, _, user_data: dict) -> bytes:
        pdf = _PDF("Attestation de Scolarite")
        first_name = user_data.get("first_name") or (user_data.get("full_name", "").split()[0] if user_data.get("full_name") else "")
        last_name  = user_data.get("last_name")  or (" ".join(user_data.get("full_name", "").split()[1:]) or "")
        full_name  = user_data.get("full_name") or f"{first_name} {last_name}".strip() or "L'etudiant(e)"
        year_level = user_data.get("year", 3)
        major = user_data.get("major", "Genie Informatique")
        card_id = user_data.get("student_card_id") or user_data.get("student_id", "")
        email = user_data.get("email", "")
        description = user_data.get("description", "")

        level_map = {1: "Premiere annee", 2: "Deuxieme annee", 3: "Troisieme annee"}
        level_label = level_map.get(int(year_level) if year_level else 3, "Troisieme annee")

        pdf.set_font("Helvetica", "", 11)
        pdf.ln(2)
        for label, value in [
            ("Nom :",        last_name.upper() if last_name else full_name.upper()),
            ("Prenom :",     first_name.capitalize() if first_name else ""),
            ("N° Carte :",   card_id or "-"),
            ("Email :",      email or "-"),
            ("Filiere :",    f"{major} - {level_label}"),
            ("Annee univ. :", "2025-2026"),
        ]:
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(40, 8, label, new_x="RIGHT", new_y="TMARGIN")
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, value, new_x="LMARGIN", new_y="NEXT")

        pdf.ln(6)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 12)
        id_part = f", portant le numero de carte etudiant {card_id}," if card_id else ""
        pdf.multi_cell(
            0, 9,
            f"Le Directeur de l'Ecole Nationale de l'Intelligence Artificielle et du Digital "
            f"(ENIAD) certifie que l'etudiant(e) {full_name}{id_part} est regulierement "
            f"inscrit(e) en {level_label}, filiere {major}, pour l'annee universitaire 2025-2026.",
            align="J",
        )
        pdf.ln(6)
        pdf.multi_cell(
            0, 9,
            "Cette attestation lui est delivree a sa demande pour servir et valoir ce que de droit.",
            align="J",
        )
        if description:
            pdf.ln(4)
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 8, f"Motif : {description}", align="J")

        pdf.signature_block()
        return bytes(pdf.output())

    def _releve_notes(self, _, user_data: dict) -> bytes:
        pdf = _PDF("Releve de Notes")
        first_name = user_data.get("first_name") or (user_data.get("full_name", "").split()[0] if user_data.get("full_name") else "")
        last_name  = user_data.get("last_name")  or (" ".join(user_data.get("full_name", "").split()[1:]) or "")
        full_name  = user_data.get("full_name") or f"{first_name} {last_name}".strip() or "L'etudiant(e)"
        major = user_data.get("major", "Genie Informatique")
        card_id = user_data.get("student_card_id") or user_data.get("student_id", "")
        year_level = user_data.get("year", 3)
        grades = user_data.get("grades", [])

        level_map = {1: "L1", 2: "L2", 3: "L3"}
        level_label = level_map.get(int(year_level) if year_level else 3, "L3")

        pdf.set_font("Helvetica", "", 12)
        pdf.ln(2)
        for label, value in [
            ("Nom :",         last_name.upper() if last_name else full_name.upper()),
            ("Prenom :",      first_name.capitalize() if first_name else ""),
            ("N° Carte :",    card_id or "-"),
            ("Filiere :",     f"{major} - {level_label}"),
            ("Annee univ. :", "2025-2026"),
        ]:
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(45, 8, label, new_x="RIGHT", new_y="TMARGIN")
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, value, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        # Table header
        pdf.set_fill_color(0, 82, 165)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10)
        for (w, label) in [(90, "Matiere"), (25, "Coef."), (25, "Note/20"), (40, "Appreciation")]:
            pdf.cell(w, 9, label, border=1, fill=True, align="C", new_x="RIGHT", new_y="TMARGIN")
        pdf.ln(9)

        def _appreciation(note):
            if note is None:
                return "-"
            if note >= 16:
                return "Tres Bien"
            if note >= 14:
                return "Bien"
            if note >= 12:
                return "Assez Bien"
            if note >= 10:
                return "Passable"
            return "Insuffisant"

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)

        if grades:
            rows = grades
        else:
            rows = [{"matiere": "Aucune note disponible", "coefficient": "-", "note": None}]

        total_coef = 0
        total_weighted = 0.0

        for i, g in enumerate(rows):
            fill = i % 2 == 0
            bg = (235, 242, 252) if fill else (255, 255, 255)
            pdf.set_fill_color(*bg)
            note = g.get("note")
            coef = g.get("coefficient", 3)
            note_str = f"{note:.2f}" if isinstance(note, (int, float)) else "-"
            appr = _appreciation(note)
            for (w, val, align) in [
                (90, str(g.get("matiere", "-")), "L"),
                (25, str(coef), "C"),
                (25, note_str, "C"),
                (40, appr, "C"),
            ]:
                pdf.cell(w, 8, val, border=1, fill=fill, align=align,
                         new_x="RIGHT", new_y="TMARGIN")
            pdf.ln(8)
            if isinstance(note, (int, float)) and isinstance(coef, (int, float)):
                total_coef += coef
                total_weighted += note * coef

        # Moyenne generale
        if total_coef > 0:
            moyenne = total_weighted / total_coef
            pdf.ln(2)
            pdf.set_fill_color(0, 82, 165)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 10)
            for (w, val, align) in [
                (90, "Moyenne Generale", "L"),
                (25, "", "C"),
                (25, f"{moyenne:.2f}", "C"),
                (40, _appreciation(moyenne), "C"),
            ]:
                pdf.cell(w, 9, val, border=1, fill=True, align=align,
                         new_x="RIGHT", new_y="TMARGIN")
            pdf.ln(9)
            pdf.set_text_color(0, 0, 0)

        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(160, 60, 60)
        note_text = (
            "Note : Ce releve contient les notes des examens enregistres dans le systeme SmartStudent."
            if grades
            else "Note : Aucune note enregistree. Contactez le secretariat pedagogique."
        )
        pdf.multi_cell(0, 7, note_text, align="J")
        pdf.set_text_color(0, 0, 0)
        pdf.signature_block()
        return bytes(pdf.output())

    def _convention_stage(self, _, user_data: dict) -> bytes:
        pdf = _PDF("Convention de Stage")
        first_name = user_data.get("first_name") or (user_data.get("full_name", "").split()[0] if user_data.get("full_name") else "")
        last_name  = user_data.get("last_name")  or (" ".join(user_data.get("full_name", "").split()[1:]) or "")
        full_name  = user_data.get("full_name") or f"{first_name} {last_name}".strip() or "L'etudiant(e)"
        major = user_data.get("major", "Genie Informatique")
        card_id = user_data.get("student_card_id") or user_data.get("student_id", "")
        year_level = user_data.get("year", 3)
        email = user_data.get("email", "")
        phone = user_data.get("phone", "")
        # Company info
        entreprise = user_data.get("entreprise", "________________")
        adresse_entreprise = user_data.get("adresse_entreprise", "________________")
        tuteur = user_data.get("tuteur", "________________")
        poste = user_data.get("poste", "Stage de fin d'etudes")
        date_debut = user_data.get("date_debut", "________________")
        date_fin = user_data.get("date_fin", "________________")

        level_map = {1: "1ere annee", 2: "2eme annee", 3: "3eme annee"}
        level_label = level_map.get(int(year_level) if year_level else 3, "3eme annee")

        def _section(title):
            pdf.ln(6)
            pdf.set_fill_color(0, 82, 165)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)

        def _row(label, value):
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(55, 7, label, new_x="RIGHT", new_y="TMARGIN")
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 7, str(value), new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.ln(2)
        pdf.multi_cell(
            0, 8,
            "La presente convention est conclue entre l'Ecole Nationale de l'Intelligence "
            "Artificielle et du Digital (ENIAD) de Berkane et l'organisme d'accueil designe "
            "ci-apres, en vue de definir les conditions du stage de l'etudiant(e).",
            align="J",
        )

        _section("PARTIE 1 - L'ETUDIANT(E)")
        _row("Nom :", last_name.upper() if last_name else full_name.upper())
        _row("Prenom :", first_name.capitalize() if first_name else "")
        _row("N° Carte etudiant :", card_id or "-")
        _row("Filiere :", f"{major} - {level_label}")
        _row("Email :", email or "-")
        _row("Telephone :", phone or "-")

        _section("PARTIE 2 - L'ETABLISSEMENT D'ACCUEIL")
        _row("Entreprise / Organisme :", entreprise)
        _row("Adresse :", adresse_entreprise)
        _row("Tuteur de stage :", tuteur)

        _section("PARTIE 3 - LE STAGE")
        _row("Sujet / Poste :", poste)
        _row("Date de debut :", date_debut)
        _row("Date de fin :", date_fin)
        _row("Annee universitaire :", "2025-2026")

        _section("PARTIE 4 - CONDITIONS")
        pdf.set_font("Helvetica", "", 10)
        conditions = [
            "L'etudiant(e) est soumis(e) au reglement interieur de l'organisme d'accueil.",
            "L'organisme d'accueil s'engage a encadrer l'etudiant(e) et a fournir les moyens necessaires.",
            "L'ENIAD assurera le suivi pedagogique de l'etudiant(e) pendant la duree du stage.",
            "Un rapport de stage devra etre remis a l'ENIAD a la fin du stage.",
        ]
        for cond in conditions:
            pdf.set_x(25)
            pdf.multi_cell(0, 7, f"- {cond}", align="J")

        # Signatures
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(63, 8, "L'Etudiant(e)", align="C", new_x="RIGHT", new_y="TMARGIN")
        pdf.cell(63, 8, "Le Directeur ENIAD", align="C", new_x="RIGHT", new_y="TMARGIN")
        pdf.cell(64, 8, "L'Organisme d'Accueil", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(130, 130, 130)
        pdf.cell(63, 6, "(Signature)", align="C", new_x="RIGHT", new_y="TMARGIN")
        pdf.cell(63, 6, "(Signature et cachet)", align="C", new_x="RIGHT", new_y="TMARGIN")
        pdf.cell(64, 6, "(Signature et cachet)", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)

        return bytes(pdf.output())

    def _certificat_stage(self, _, user_data: dict) -> bytes:
        pdf = _PDF("Certificat de Stage")
        full_name = user_data.get("full_name", "L'etudiant(e)")
        major = user_data.get("major", "Genie Informatique")
        description = user_data.get("description", "")

        pdf.set_font("Helvetica", "", 12)
        pdf.ln(4)
        pdf.multi_cell(
            0, 9,
            f"Le Directeur de l'ENIAD certifie que l'etudiant(e) {full_name}, "
            f"inscrit(e) en filiere {major}, est autorise(e) a effectuer un stage de fin "
            f"d'etudes conformement aux exigences du programme d'enseignement.",
            align="J",
        )
        if description:
            pdf.ln(4)
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 8, f"Precisions : {description}", align="J")

        pdf.ln(6)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(
            0, 9,
            "Ce certificat est delivre pour permettre a l'etudiant(e) de faire valoir ses droits "
            "aupres des organismes d'accueil.",
            align="J",
        )
        pdf.signature_block()
        return bytes(pdf.output())

    def _demande_generique(self, doc_type: str, user_data: dict) -> bytes:
        pdf = _PDF(doc_type)
        full_name = user_data.get("full_name", "L'etudiant(e)")
        major = user_data.get("major", "Genie Informatique")
        year_level = user_data.get("year", 3)
        description = user_data.get("description", "")

        level_map = {1: "1ere annee", 2: "2eme annee", 3: "3eme annee"}
        level_label = level_map.get(int(year_level) if year_level else 3, "3eme annee")

        pdf.set_font("Helvetica", "", 12)
        pdf.ln(4)
        for label, value in [
            ("Etudiant(e) :", full_name),
            ("Filiere :", f"{major} - {level_label}"),
            ("Date :", datetime.now().strftime("%d/%m/%Y")),
        ]:
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(40, 8, label, new_x="RIGHT", new_y="TMARGIN")
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, value, new_x="LMARGIN", new_y="NEXT")

        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Objet : {doc_type}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(
            0, 9,
            f"Je soussigne(e) {full_name}, etudiant(e) en {level_label} filiere {major}, "
            f"sollicite respectueusement l'etablissement du document suivant : {doc_type}.",
            align="J",
        )
        if description:
            pdf.ln(6)
            pdf.multi_cell(0, 9, f"Motif / Details :\n{description}", align="J")

        pdf.ln(10)
        pdf.multi_cell(
            0, 9,
            "Dans l'attente d'une suite favorable, veuillez agreer, Monsieur le Directeur, "
            "l'expression de mes salutations les plus respectueuses.",
            align="J",
        )
        pdf.signature_block()
        return bytes(pdf.output())


_agent = DocumentsAgent()


def get_documents_agent() -> DocumentsAgent:
    return _agent
