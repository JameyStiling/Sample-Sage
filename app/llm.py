
from __future__ import annotations
from typing import List
from .models import QueryRequest, QueryMatch, Sample

class LLMClient:
    """Stubbed reasoning client.
    Replace match_query with real LLM or embedding search.
    """
    def __init__(self, provider: str = "none", api_key: str | None = None):
        self.provider = provider
        self.api_key = api_key

    def match_query(self, req: QueryRequest, candidates: List[Sample]) -> List[QueryMatch]:
        # Naive heuristic: score by simple keyword overlaps in filename/tags.
        q = req.query.lower()
        scored: List[QueryMatch] = []
        for s in candidates:
            text = f"{s.name} {' '.join(s.tags)} {s.key or ''} {s.bpm or ''}".lower()
            overlap = sum(int(tok in text) for tok in q.split())
            score = min(1.0, 0.1 * overlap)
            scored.append(QueryMatch(sample=s, score=score))
        # sort by score desc and trim
        scored.sort(key=lambda m: m.score, reverse=True)
        return scored[: req.limit]
