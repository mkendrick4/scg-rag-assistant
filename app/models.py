from typing import Literal

from pydantic import BaseModel


ClassificationLevel = Literal[
    "UNCLASSIFIED",
    "CONFIDENTIAL",
    "SECRET",
    "TOP SECRET",
]


class PortionAnalysis(BaseModel):
    text: str
    marking: ClassificationLevel
    explanation: str
    source_section: str


class ClassificationResult(BaseModel):
    overall_classification: ClassificationLevel
    portions: list[PortionAnalysis]


class SCGSection(BaseModel):
    section: str
    text: str