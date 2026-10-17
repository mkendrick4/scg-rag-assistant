import os

from dotenv import load_dotenv
from openai import OpenAI

from app.embedding_retriever import (
    embed_sections,
    retrieve_sections_by_embedding,
)
from app.scg_loader import load_scg, parse_scg_sections

from app.models import PortionAnalysis

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SCG_FILE = "data/sample_scg.txt"


EMAIL = """
Team,

The customer meeting has been moved to Thursday.

Testing confirmed Project Falcon can operate at a range of 425 miles.

Please update the schedule accordingly.
"""


CLASSIFICATION_ORDER = {
    "UNCLASSIFIED": 0,
    "CONFIDENTIAL": 1,
    "SECRET": 2,
    "TOP SECRET": 3,
}

def determine_overall_classification(
    analyses: list[PortionAnalysis],
) -> str | None:
    classified_portions = [
        analysis
        for analysis in analyses
        if analysis.marking is not None
    ]

    if not classified_portions:
        return None

    highest = max(
        classified_portions,
        key=lambda analysis: CLASSIFICATION_ORDER[analysis.marking],
    )

    return highest.marking


def split_email_into_portions(email: str) -> list[str]:
    return [
        line.strip()
        for line in email.splitlines()
        if line.strip()
    ]


def classify_portion(
    portion: str,
    retrieved: list[tuple[float, object]],
) -> PortionAnalysis:
    if not retrieved:
        return PortionAnalysis(
            text=portion,
            marking=None,
            explanation="No sufficiently relevant guidance was retrieved.",
            source_section=None,
        )

    retrieved_guidance = "\n\n".join(
        f"{section.section}:\n{section.text}"
        for score, section in retrieved
    )

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": (
                    "You are assisting with a fictional classification exercise. "
                    "Use only the retrieved classification guidance provided. "
                    "Do not invent classification rules. "
                    "Determine whether any retrieved guidance actually applies to the portion. "
                    "If none applies, return null for marking and source_section. "
                    "If guidance applies, source_section must exactly match one retrieved section."
                ),
            },
            {
                "role": "user",
                "content": f"""
PORTION:

{portion}

RETRIEVED GUIDANCE:

{retrieved_guidance}
""",
            },
        ],
        text_format=PortionAnalysis,
    )

    return response.output_parsed


def validate_retrieved_source(
    analysis: PortionAnalysis,
    retrieved: list[tuple[float, object]],
) -> None:
    if analysis.source_section is None:
        return

    retrieved_section_names = {
        section.section
        for score, section in retrieved
    }

    if analysis.source_section not in retrieved_section_names:
        raise ValueError(
            "\nInvalid source returned by model:\n"
            f"  Text: {analysis.text}\n"
            f"  Source returned: {analysis.source_section}\n"
            f"  Retrieved sources: {sorted(retrieved_section_names)}"
        )

    
def main():
    guidance = load_scg(SCG_FILE)
    sections = parse_scg_sections(guidance)

    embedded_sections = embed_sections(
        client,
        sections,
    )

    portions = split_email_into_portions(EMAIL)

    print("\nPer-portion retrieval:")

    analyses = []

    for portion in portions:
        retrieved = retrieve_sections_by_embedding(
            client,
            portion,
            embedded_sections,
            top_k=3,
            min_similarity=0.20,
        )

        print(f"\nPORTION: {portion}")

        if not retrieved:
            print("  No sufficiently relevant guidance found.")
            continue

        for score, section in retrieved:
            print(
                f"  {section.section} "
                f"(similarity: {score:.3f})"
            )
            print(f"  {section.text}")

        analysis = classify_portion(
            portion,
            retrieved,
        )

        validate_retrieved_source(
            analysis,
            retrieved,
        )

        analyses.append(analysis)
        print("\nAI decision:")
        print(f"  Marking: {analysis.marking}")
        print(f"  Source: {analysis.source_section}")
        print(f"  Reason: {analysis.explanation}")  
    overall_classification = determine_overall_classification(
        analyses
    )

    print("\nDocument result:")
    print(f"  Overall classification: {overall_classification}")    


if __name__ == "__main__":
    main()