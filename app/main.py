from fastapi import FastAPI

app = FastAPI(
    title="API Visual Hackathon",
    description="API desarrollada para el hackathon",
    version="1.0.0"
)


@app.get("/")
async def read_root():
    return {"message": "¡Hola desde FastAPI!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q} 