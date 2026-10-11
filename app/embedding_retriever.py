import math

from openai import OpenAI

from app.models import SCGSection


EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(
    client: OpenAI,
    text: str,
) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_sections_by_embedding(
    client: OpenAI,
    query: str,
    sections: list[SCGSection],
    top_k: int = 1,
) -> list[tuple[float, SCGSection]]:
    query_embedding = get_embedding(
        client,
        query,
    )

    scored_sections = []

    for section in sections:
        section_embedding = get_embedding(
            client,
            section.text,
        )

        score = cosine_similarity(
            query_embedding,
            section_embedding,
        )

        scored_sections.append(
            (score, section)
        )

    scored_sections.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return scored_sections[:top_k]