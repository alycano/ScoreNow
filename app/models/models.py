from pydantic import BaseModel
from typing import Optional

class Team(BaseModel):
    id: Optional[int] = None
    name: str
    country: str