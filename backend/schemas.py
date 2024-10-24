from pydantic import BaseModel, Field
from typing import List, Union
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: MessageRole
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[Message] = Field(default_factory=list)

class SearchResult(BaseModel):
    title: str
    url: str
    content: str

class StreamEvent(str, Enum):
    SEARCH_QUERY = "search_query"
    SEARCH_RESULTS = "search_results"
    TEXT_CHUNK = "text_chunk"
    RELATED_QUERIES = "related_queries"
    STREAM_END = "stream_end"

class ChatObject(BaseModel):
    event_type: StreamEvent

class SearchQueryStream(ChatObject):
    event_type: StreamEvent = StreamEvent.SEARCH_QUERY
    query: str
class SearchResultStream(ChatObject):
    event_type: StreamEvent = StreamEvent.SEARCH_RESULTS
    results: List[SearchResult] = Field(default_factory=list)
class TextChunkStream(ChatObject):
    event_type: StreamEvent = StreamEvent.TEXT_CHUNK
    text: str
class RelatedQueriesStream(ChatObject):
    event_type: StreamEvent = StreamEvent.RELATED_QUERIES
    related_queries: List[str] = Field(default_factory=list)
class StreamEndStream(ChatObject):
    event_type: StreamEvent = StreamEvent.STREAM_END
class ChatResponseEvent(BaseModel):
    event: StreamEvent
    data: Union[
        SearchQueryStream,
        SearchResultStream,
        TextChunkStream,
        RelatedQueriesStream,
        StreamEndStream,
    ]