from pydantic import BaseModel, Field
from typing import List, Dict


class QnABody(BaseModel):
    query: str = Field()
    context: str = Field()