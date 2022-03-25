from pydantic import BaseModel


from pydantic import BaseModel
from typing import Optional

class Offer(BaseModel):
    name: str
    company: str
    href: str
    location: Optional[str]
    