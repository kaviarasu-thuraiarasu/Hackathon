from pydantic import BaseModel,Field
from typing import List

class Section(BaseModel):
    task: str = Field(
        description="Listing all the task of the user story",
    )

class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )
