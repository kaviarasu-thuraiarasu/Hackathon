from pydantic import BaseModel,Field
from typing import List

class Section(BaseModel):
    task: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )
