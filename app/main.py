import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models import ClassificationResult
from app.embedding_retriever import retrieve_sections_by_embedding
from app.scg_loader import load_scg, parse_scg_sections


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


VALID_SOURCES = {
    "UNCLASSIFIED": {"Section 1.1"},
    "CONFIDENTIAL": {"Section 3.2"},
}


def validate_sources(result: ClassificationResult) -> None:
    for portion in portions:
        retrieved = retrieve_sections_by_embedding(
            client,
            portion,
            sections,
            top_k=1,
        )

    print(f"\nPORTION: {portion}")

    for score, section in retrieved:
        print(
            f"  {section.section} "
            f"(similarity: {score:.3f})"
        )
        print(f"  {section.text}")


def split_email_into_portions(email: str) -> list[str]:
    return [
        line.strip()
        for line in email.splitlines()
        if line.strip()
    ]


def main():
    guidance = load_scg(SCG_FILE)
    sections = parse_scg_sections(guidance)

    portions = split_email_into_portions(EMAIL)

    print("\nPer-portion retrieval:")

    for portion in portions:
        retrieved = retrieve_sections_by_embedding(
            client,
            portion,
            sections,
            top_k=1,
        )

        print(f"\nPORTION: {portion}")

        if not retrieved:
            print("  No matching guidance found.")
            continue

        for score, section in retrieved:
            print(
                f"  {section.section} "
                f"(similarity: {score:.3f})"
            )
            print(f"  {section.text}")


if __name__ == "__main__":
    main()