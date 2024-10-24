import asyncio
import json
from typing import AsyncGenerator, AsyncIterator
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
import httpx
from schemas import (
    ChatRequest,
    ChatResponseEvent,
    RelatedQueriesStream,
    SearchQueryStream,
    SearchResult,
    SearchResultStream,
    StreamEvent,
    TextChunkStream,
    StreamEndStream,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


fake_query = "Sam Pan"
fake_search_results = [
    SearchResult(
        title="Sam Pan", 
        url="https://linkedin.com/in/sam-pan-135", 
        content="Sam is a good person"
    ),
    SearchResult(
        title="Sam Pan", 
        url="https://washubears.com/sports/mens-track-and-field/roster/samuel-pan/7726", 
        content="Sam is a track athlete at WashU"
    ),
]

fake_response = "Sam Pan is a computer science student at WashU who runs track and field"

fake_related_queries = ["Sam Pan track", "Sam Pan computer science", "Sam Pan WashU"]


@app.post("/search")
async def search(request: ChatRequest) -> StreamingResponse:
    async def generator():
        async for obj in stream_qa_objects(request):
            yield json.dumps(jsonable_encoder(obj))

    return StreamingResponse(generator(), media_type="application/json")

async def stream_qa_objects(request: ChatRequest) -> AsyncIterator[ChatResponseEvent]:
    yield ChatResponseEvent(
        event=StreamEvent.SEARCH_QUERY,
        data=SearchQueryStream(query=fake_query),
    )
    await asyncio.sleep(1)
    yield ChatResponseEvent(
        event=StreamEvent.SEARCH_RESULTS,
        data=SearchResultStream(
            results=fake_search_results,
        ),
    )
    for word in fake_response.split():
        yield ChatResponseEvent(
            event=StreamEvent.TEXT_CHUNK,
            data=TextChunkStream(text=word),
        )
        await asyncio.sleep(0.1)
    
    yield ChatResponseEvent(
        event=StreamEvent.RELATED_QUERIES,
        data=RelatedQueriesStream(related_queries=fake_related_queries),
    )

    yield ChatResponseEvent(
        event=StreamEvent.STREAM_END,
        data=StreamEndStream(),
    )

async def main():
    url = "http://127.0.0.1:8000/search"
    print("Sending request")
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST", 
            url, 
            json=ChatRequest(query="Sam Pan", history=[]).model_dump(),
        ) as r:
            async for chunk in r.aiter_text():
                print(chunk)

if __name__ == "__main__":
    asyncio.run(main())