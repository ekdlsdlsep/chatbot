from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel

class RequestChat(BaseModel):
    id: str
    messages : str

@dataclass
class Usage :
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class Message :
    role: str
    content: str

@dataclass
class Choice :
    message: Message
    logprobs: Optional[object]
    finish_reason: str
    index: int

@dataclass
class ReponseOpenAI :
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]