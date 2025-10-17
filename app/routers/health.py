
from fastapi import APIRouter
from ..models import HealthResponse

router = APIRouter()

@router.get("/healthz", response_model=HealthResponse)
def health():
    return HealthResponse(ok=True, version="0.1.0")
