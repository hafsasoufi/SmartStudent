"""
Service RAG — ChromaDB + Sentence Transformers
Stockage local, aucune clé API requise pour les embeddings.
"""

import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

_rag_instance: Optional["RAGService"] = None


def get_rag_service() -> "RAGService":
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGService()
    return _rag_instance


class RAGService:
    def __init__(self):
        self._ready = False
        self._collection = None
        self._model = None
        self._init()

    def _init(self):
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer

            db_path = Path(__file__).parent.parent / "chroma_db"
            db_path.mkdir(exist_ok=True)

            client = chromadb.PersistentClient(path=str(db_path))
            self._collection = client.get_or_create_collection(
                name="eniad_docs",
                metadata={"hnsw:space": "cosine"},
            )
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._ready = True
            logger.info(f"RAG prêt — {self._collection.count()} documents indexés")
        except ImportError as e:
            logger.warning(f"RAG non disponible (package manquant: {e}). Installe: pip install chromadb sentence-transformers")
        except Exception as e:
            logger.error(f"RAG init error: {e}")

    @property
    def is_ready(self) -> bool:
        return self._ready and self._collection is not None

    @property
    def document_count(self) -> int:
        if not self.is_ready:
            return 0
        return self._collection.count()

    def add_document(
        self,
        text: str,
        metadata: Dict[str, Any],
        doc_id: Optional[str] = None,
    ) -> bool:
        if not self.is_ready or not text.strip():
            return False
        try:
            embedding = self._model.encode([text])[0].tolist()
            self._collection.add(
                ids=[doc_id or str(uuid.uuid4())],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{k: str(v) for k, v in metadata.items()}],
            )
            return True
        except Exception as e:
            logger.error(f"Erreur ajout document: {e}")
            return False

    def add_documents_batch(self, documents: List[Dict[str, Any]]) -> int:
        """Ajoute une liste de {text, metadata, id?} en batch."""
        if not self.is_ready:
            return 0
        added = 0
        ids, embeddings, texts, metadatas = [], [], [], []
        for doc in documents:
            text = doc.get("text", "").strip()
            if not text:
                continue
            ids.append(doc.get("id", str(uuid.uuid4())))
            embeddings.append(self._model.encode([text])[0].tolist())
            texts.append(text)
            metadatas.append({k: str(v) for k, v in doc.get("metadata", {}).items()})
            added += 1

        if ids:
            try:
                self._collection.add(
                    ids=ids, embeddings=embeddings,
                    documents=texts, metadatas=metadatas,
                )
            except Exception as e:
                logger.error(f"Batch add error: {e}")
                return 0
        return added

    def query(
        self,
        question: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Retourne les n_results documents les plus pertinents."""
        if not self.is_ready:
            return []
        try:
            embedding = self._model.encode([question])[0].tolist()
            kwargs: Dict[str, Any] = {
                "query_embeddings": [embedding],
                "n_results": min(n_results, max(1, self._collection.count())),
                "include": ["documents", "metadatas", "distances"],
            }
            if filter_metadata:
                kwargs["where"] = {k: {"$eq": v} for k, v in filter_metadata.items()}

            results = self._collection.query(**kwargs)
            output = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                output.append({
                    "content": doc,
                    "metadata": meta,
                    "score": round(1 - dist, 4),  # cosine similarity
                })
            return output
        except Exception as e:
            logger.error(f"Erreur requête RAG: {e}")
            return []

    def build_context(self, question: str, n_results: int = 4) -> str:
        """Retourne un contexte formaté pour injection dans le prompt LLM."""
        docs = self.query(question, n_results=n_results)
        if not docs:
            return ""
        parts = []
        for i, doc in enumerate(docs, 1):
            meta = doc["metadata"]
            source = meta.get("description", meta.get("type", "document"))
            score = doc["score"]
            parts.append(f"[Document {i} — {source} (pertinence: {score:.0%})]\n{doc['content']}")
        return "\n\n".join(parts)

    def reset(self):
        """Vide la collection (pour re-indexer)."""
        if not self.is_ready:
            return
        try:
            import chromadb
            db_path = Path(__file__).parent.parent / "chroma_db"
            client = chromadb.PersistentClient(path=str(db_path))
            client.delete_collection("eniad_docs")
            self._collection = client.get_or_create_collection(
                name="eniad_docs",
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("Collection RAG réinitialisée")
        except Exception as e:
            logger.error(f"Reset error: {e}")
