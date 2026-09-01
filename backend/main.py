from fastapi import FastAPI

app = FastAPI(
    title="Emergency Response Intelligence System",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "system": "Emergency Response Intelligence System",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }