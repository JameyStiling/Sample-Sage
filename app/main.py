
from fastapi import FastAPI
from .routers import health, samples

app = FastAPI(title="Sample Sage", version="0.1.0")

app.include_router(health.router)
app.include_router(samples.router)

@app.get("/", include_in_schema=False)
def root():
    return {"ok": True, "service": "sample-sage"}
