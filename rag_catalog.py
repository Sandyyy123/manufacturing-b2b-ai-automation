import os
from typing import List

CHROMA_AVAILABLE = False
try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    pass

DEMO_CATALOG = [
    {"id": "CF-001", "name": "Carbon Fibre Panel Series A",
     "spec": "T300 carbon, 2mm-20mm, ISO 14125, Tg 180C"},
    {"id": "GRP-008", "name": "GRP Structural Tube",
     "spec": "E-glass winding, OD 25-200mm, fire class B1"},
    {"id": "EP-C01", "name": "Epoxy Laminate Sheet",
     "spec": "FR4-grade, 1.6mm, IPC-4101C, UL94-V0"},
    {"id": "CF-A22", "name": "Aerospace Carbon Prepreg",
     "spec": "UD 200gsm, Hex-ply, cure 125C, Vf 60%"},
    {"id": "PP-F10", "name": "PP/Glass Thermoplastic Sheet",
     "spec": "Twintex 40%, 3mm, automotive grade"},
]


class CatalogRAG:
    def __init__(self):
        self.demo_mode = not CHROMA_AVAILABLE or not os.getenv("OPENAI_API_KEY")

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        return self._keyword_search(query, top_k)

    def _keyword_search(self, query: str, top_k: int) -> List[dict]:
        q = query.lower()
        tokens = q.split()
        scored = []
        for item in DEMO_CATALOG:
            hits = sum(1 for w in tokens if w in item["spec"].lower() or w in item["name"].lower())
            if hits > 0:
                scored.append({**item, "relevance": round(hits / len(tokens), 2)})
        return sorted(scored, key=lambda x: -x["relevance"])[:top_k]
