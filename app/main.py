import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models import ClassificationResult

from app.scg_loader import load_scg, parse_scg_sections

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SCG_FILE = "data/sample_scg.txt"

guidance = load_scg(SCG_FILE)

sections = parse_scg_sections(guidance)

for section in sections:
    print(section)

EMAIL = """
Team,

The customer meeting has been moved to Thursday.

Testing confirmed Project Falcon can operate at a range of 425 miles.

Please update the schedule accordingly.
"""

VALID_SOURCES = {
    "UNCLASSIFIED": {"Section 1.1"},
    "CONFIDENTIAL": {"Section 3.2"},
}


def validate_sources(result: ClassificationResult) -> None:
    for portion in result.portions:
        allowed_sources = VALID_SOURCES.get(portion.marking, set())

        if portion.source_section not in allowed_sources:
            raise ValueError(
                f"Invalid source '{portion.source_section}' "
                f"for marking '{portion.marking}'"
            )

        
def main():
    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": (
                    "You are assisting with a fictional classification exercise. "
                    "Use only the supplied classification guidance. "
                    "Do not invent classification rules. "
                    "Analyze each meaningful portion of the email separately. "
                    "For every portion, assign the most directly applicable guidance section. "
                    "The source_section value must exactly match one of the section names "
                    "provided in the classification guidance, such as 'Section 1.1' or "
                    "'Section 3.2'. Do not return explanations or free-form text in "
                    "source_section."
                ),
            },
            {
                "role": "user",
                "content": f"""
CLASSIFICATION GUIDANCE:

{guidance}

EMAIL TO ANALYZE:

{EMAIL}
""",
            },
        ],
        text_format=ClassificationResult,
    )

    result = response.output_parsed
    validate_sources(result)

    print(f"\nOverall classification: {result.overall_classification}\n")

    for portion in result.portions:
        print(f"({portion.marking}) {portion.text}")
        print(f"Reason: {portion.explanation}")
        print(f"Source: {portion.source_section}\n")

if __name__ == "__main__":
    main()