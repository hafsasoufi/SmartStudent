"""
Script d'initialisation du RAG — ENIAD SmartStudent
Usage : python -m backend.scripts.setup_rag

Ce script :
1. Télécharge tous les PDFs disponibles sur eniad.ump.ma
2. Extrait le texte avec pdfplumber
3. Découpe en chunks (1000 chars / 200 overlap)
4. Ajoute la base de connaissances statique
5. Indexe tout dans ChromaDB
"""

import sys
import os
import time
import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Any

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

sys.stdout.reconfigure(encoding="utf-8")


# ── Chunking ────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Découpe un texte long en chunks avec chevauchement."""
    text = " ".join(text.split())
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


# ── Téléchargement PDF ───────────────────────────────────────────────────────

def download_pdf(url: str, timeout: int = 60) -> bytes | None:
    """Télécharge un PDF depuis une URL. Retourne les bytes ou None."""
    try:
        import requests
        from urllib.parse import quote
        # Encode spaces and special chars in the path part only
        if " " in url:
            parts = url.split("://", 1)
            if len(parts) == 2:
                path_part = parts[1]
                # encode only the path, keep slashes and colons
                path_part = quote(path_part, safe="/:?=&#@")
                url = parts[0] + "://" + path_part
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/pdf,*/*",
            "Referer": "https://eniad.ump.ma/",
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            content = resp.content
            if content[:4] == b"%PDF":
                return content
            logger.warning(f"  Contenu non-PDF pour {url} (recu {len(content)} bytes)")
        else:
            logger.warning(f"  HTTP {resp.status_code} pour {url}")
    except Exception as e:
        logger.warning(f"  Erreur téléchargement {url}: {e}")
    return None


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extrait le texte d'un PDF en mémoire."""
    try:
        import pdfplumber
        import io
        text_parts = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
                # Extraire aussi les tables
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        row_text = " | ".join(str(c) for c in row if c)
                        if row_text.strip():
                            text_parts.append(row_text)
        return "\n".join(text_parts)
    except Exception as e:
        logger.warning(f"  Erreur extraction PDF: {e}")
        return ""


# ── Indexation ───────────────────────────────────────────────────────────────

def index_pdf_resources(rag) -> int:
    """Télécharge et indexe tous les PDFs ENIAD."""
    from backend.data.eniad_knowledge import PDF_RESOURCES

    total_chunks = 0
    for res in PDF_RESOURCES:
        url = res["url"]
        desc = res.get("description", res.get("filename", url))
        logger.info(f"  Téléchargement : {desc}")

        pdf_bytes = download_pdf(url)
        if not pdf_bytes:
            logger.warning(f"  IGNORÉ (téléchargement échoué) : {desc}")
            time.sleep(0.5)
            continue

        text = extract_text_from_pdf(pdf_bytes)
        if not text.strip():
            logger.warning(f"  IGNORÉ (texte vide) : {desc}")
            continue

        chunks = chunk_text(text, chunk_size=800, overlap=150)
        metadata = {
            "source": "pdf",
            "url": url,
            "description": desc,
            "type": res.get("type", "document"),
            "program": res.get("program", ""),
            "semester": res.get("semester", ""),
            "year": res.get("year", ""),
            "season": res.get("season", ""),
        }

        docs = []
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"pdf_{res['filename'].replace('.pdf','')}_chunk{i}",
                "text": f"{desc}\n\n{chunk}",
                "metadata": metadata,
            })

        added = rag.add_documents_batch(docs)
        total_chunks += added
        logger.info(f"  OK — {added} chunks indexés ({len(text)} chars)")
        time.sleep(0.3)  # politesse envers le serveur

    return total_chunks


def index_static_knowledge(rag) -> int:
    """Indexe la base de connaissances statique."""
    from backend.data.eniad_knowledge import ENIAD_KNOWLEDGE_BASE

    docs = []
    for entry in ENIAD_KNOWLEDGE_BASE:
        text = f"{entry['title']}\n\n{entry['content']}"
        chunks = chunk_text(text, chunk_size=900, overlap=100)
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"kb_{entry['id']}_chunk{i}",
                "text": chunk,
                "metadata": {
                    "source": "knowledge_base",
                    "category": entry.get("category", "general"),
                    "title": entry["title"],
                    "description": entry["title"],
                },
            })

    added = rag.add_documents_batch(docs)
    logger.info(f"  Base de connaissances : {added} chunks indexés")
    return added


def index_official_documents(rag) -> int:
    """Indexe les documents officiels ENIAD : Règlement Intérieur + Convention de Stage."""
    from backend.data.eniad_reglement import ENIAD_OFFICIAL_DOCUMENTS

    docs = []
    for entry in ENIAD_OFFICIAL_DOCUMENTS:
        text = f"[{entry['source']}]\n{entry['title']}\n\n{entry['content']}"
        chunks = chunk_text(text, chunk_size=900, overlap=150)
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"official_{entry['id']}_chunk{i}",
                "text": chunk,
                "metadata": {
                    "source": "official_document",
                    "category": entry.get("category", "reglement"),
                    "title": entry["title"],
                    "document_source": entry.get("source", "ENIAD"),
                    "description": entry["title"],
                },
            })

    added = rag.add_documents_batch(docs)
    logger.info(f"  Documents officiels (Règlement + Convention) : {added} chunks indexés")
    return added


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    logger.info("=" * 60)
    logger.info("  SETUP RAG — SmartStudent ENIAD")
    logger.info("=" * 60)

    # Vérification des dépendances
    missing = []
    for pkg in ["chromadb", "sentence_transformers", "pdfplumber"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        logger.error(f"Packages manquants : {', '.join(missing)}")
        logger.error("Installe avec : pip install " + " ".join(missing))
        sys.exit(1)

    from backend.services.rag_service import RAGService

    logger.info("\n[1/4] Initialisation ChromaDB + Sentence Transformers...")
    rag = RAGService()
    if not rag.is_ready:
        logger.error("Impossible d'initialiser le RAG. Vérifier les logs.")
        sys.exit(1)

    logger.info(f"  Documents actuels : {rag.document_count}")

    # Reset si re-indexation complète
    if "--reset" in sys.argv:
        logger.info("  Reset de la collection...")
        rag.reset()

    if rag.document_count > 0 and "--reset" not in sys.argv:
        logger.info(f"  Collection déjà peuplée ({rag.document_count} docs). Utilise --reset pour re-indexer.")
    else:
        logger.info("\n[2/5] Indexation de la base de connaissances statique...")
        kb_count = index_static_knowledge(rag)

        logger.info("\n[3/5] Indexation des documents officiels (Règlement Intérieur + Convention de Stage)...")
        official_count = index_official_documents(rag)

        logger.info("\n[4/5] Téléchargement et indexation des PDFs ENIAD...")
        pdf_count = index_pdf_resources(rag)

        logger.info(f"\n[5/5] Terminé !")
        logger.info(f"  Base de connaissances       : {kb_count} chunks")
        logger.info(f"  Documents officiels ENIAD   : {official_count} chunks")
        logger.info(f"  PDFs ENIAD (web)             : {pdf_count} chunks")
        logger.info(f"  TOTAL                        : {rag.document_count} documents indexés")

    # Test de requête
    logger.info("\n[TEST] Requête de test : 'emploi du temps IA semestre 5'")
    results = rag.query("emploi du temps IA semestre 5", n_results=2)
    for r in results:
        logger.info(f"  Score {r['score']:.2f} — {r['metadata'].get('description', '?')[:80]}")

    logger.info("\n  RAG opérationnel ! Lance le backend normalement.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
