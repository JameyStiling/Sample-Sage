
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from ..models import IndexResponse, QueryRequest, QueryResponse, QueryMatch, Sample
from ..config import settings
from ..indexer import scan_directory
from ..llm import LLMClient
from ..cache import TTLCache

router = APIRouter(prefix="/samples", tags=["samples"])

# in-memory state (indexed samples)
SAMPLES: Dict[str, Sample] = {}
CACHE = TTLCache(ttl_seconds=settings.cache_ttl_seconds)
LLM = LLMClient(provider=settings.llm_provider)

@router.post("/index", response_model=IndexResponse)
def index_samples():
    # use cache to avoid re-scan within TTL
    cached = CACHE.get("samples")
    if cached is not None:
        return IndexResponse(count=len(cached))

    scanned: List[Sample] = scan_directory(settings.sample_dir)
    global SAMPLES
    SAMPLES = {s.id: s for s in scanned}
    CACHE.set("samples", SAMPLES)
    return IndexResponse(count=len(SAMPLES))

@router.post("/query", response_model=QueryResponse)
def query_samples(req: QueryRequest):
    if not SAMPLES:
        # attempt auto index if empty
        scanned: List[Sample] = scan_directory(settings.sample_dir)
        global SAMPLES
        SAMPLES = {s.id: s for s in scanned}

    matches: List[QueryMatch] = LLM.match_query(req, list(SAMPLES.values()))
    return QueryResponse(matches=matches)

@router.get("/{sample_id}", response_model=Sample)
def get_sample(sample_id: str):
    s = SAMPLES.get(sample_id)
    if not s:
        raise HTTPException(status_code=404, detail="Sample not found")
    return s
