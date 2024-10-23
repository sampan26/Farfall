from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
async def search(query: str):
    return {"message": f"for: {query}!"}
