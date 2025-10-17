
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    sample_dir: str = os.getenv("SAMPLE_DIR", "./samples")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "600"))
    llm_provider: str = os.getenv("LLM_PROVIDER", "none")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

settings = Settings()
