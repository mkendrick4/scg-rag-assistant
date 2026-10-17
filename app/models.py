from typing import Literal

from pydantic import BaseModel


ClassificationLevel = Literal[
    "UNCLASSIFIED",
    "CONFIDENTIAL",
    "SECRET",
    "TOP SECRET",
]


class SCGSection(BaseModel):
    section: str
    text: str


class PortionAnalysis(BaseModel):
    text: str
    marking: ClassificationLevel | None
    explanation: str
    source_section: str | None


class ClassificationResult(BaseModel):
    overall_classification: ClassificationLevel | None
    portions: list[PortionAnalysis]