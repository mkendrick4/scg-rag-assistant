import re
from pathlib import Path

from app.models import SCGSection


def load_scg(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"SCG file not found: {file_path}")

    return path.read_text(encoding="utf-8")


def parse_scg_sections(scg_text: str) -> list[SCGSection]:
    pattern = r"(Section\s+\d+\.\d+):\s*(.*?)(?=\nSection\s+\d+\.\d+:|\Z)"

    matches = re.findall(
        pattern,
        scg_text,
        flags=re.DOTALL,
    )

    sections = []

    for section_name, section_text in matches:
        sections.append(
            SCGSection(
                section=section_name,
                text=section_text.strip(),
            )
        )

    return sections