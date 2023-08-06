from pydantic import BaseModel

class Code(BaseModel):
    code: str
    date: str
    time: str
    id: int