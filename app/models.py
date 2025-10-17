
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal

class Sample(BaseModel):
    id: str
    path: str
    name: str
    bpm: Optional[float] = None
    key: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    @field_validator('key')
    @classmethod
    def normalize_key(cls, v):
        if not v:
            return v
        return v.strip().upper().replace('M', 'M').replace('MIN', 'M')  # simple normalizer

class IndexResponse(BaseModel):
    count: int

class QueryRequest(BaseModel):
    query: str = Field(min_length=1, description="Natural language like: dreamy ambient pads around 90 bpm in A minor")
    limit: int = 20

class QueryMatch(BaseModel):
    sample: Sample
    score: float = Field(ge=0, le=1)

class QueryResponse(BaseModel):
    matches: List[QueryMatch]

class HealthResponse(BaseModel):
    ok: bool
    version: str
