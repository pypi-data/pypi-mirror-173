from pydantic import BaseModel
from enum import Enum

class DuplicateStatus(str, Enum):
    DUPLICATE = "DUPLICATE"
    NOT_DUPLICATE = "NOT_DUPLICATE"

class Duplicate(BaseModel):
    code: str
    date: str
    time: str
    id: int
    status: DuplicateStatus