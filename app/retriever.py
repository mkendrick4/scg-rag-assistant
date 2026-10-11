from app.models import SCGSection


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


def normalize_words(text: str) -> set[str]:
    words = text.lower().split()

    return {
        word.strip(".,:;!?()[]{}")
        for word in words
        if word.strip(".,:;!?()[]{}") not in STOP_WORDS
    }


def retrieve_sections(
    query: str,
    sections: list[SCGSection],
) -> list[SCGSection]:
    query_words = normalize_words(query)

    scored_sections = []

    for section in sections:
        section_words = normalize_words(section.text)

        score = len(query_words.intersection(section_words))

        scored_sections.append(
            (score, section)
        )

    scored_sections.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        section
        for score, section in scored_sections
        if score > 0
    ]