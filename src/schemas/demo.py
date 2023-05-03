from pydantic import BaseModel
from typing import Optional, List


class Demo(BaseModel):
    id: int
    name: str
    short_name: str
    exec_path: str
    description: Optional[str] = None
    authors: Optional[List[str]] = None
    