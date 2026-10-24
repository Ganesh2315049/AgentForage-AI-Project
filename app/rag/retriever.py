
from pathlib import Path

# Find security_notes.txt in the same folder as this file
NOTES_FILE = Path(__file__).parent / "security_notes.txt"


def retrieve_context(question: str, max_results: int = 3) -> str:
    """Find security notes that are relevant to a question."""

    if not question.strip():
        return ""

    if max_results < 1:
        return ""

    if not NOTES_FILE.exists():
        raise FileNotFoundError(
            f"Security notes not found: {NOTES_FILE}"
        )

    # Read the knowledge document
    text = NOTES_FILE.read_text(encoding="utf-8")

    # Split the document into paragraphs
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    # Find paragraphs containing words from the question
    question_words = set(question.lower().split())
    scored_paragraphs = []

    for paragraph in paragraphs:
        paragraph_words = set(
            paragraph.lower().replace(":", " ").replace(",", " ").split()
        )

        score = len(question_words & paragraph_words)

        if score > 0:
            scored_paragraphs.append((score, paragraph))

    # Highest-scoring paragraphs first
    scored_paragraphs.sort(key=lambda item: item[0], reverse=True)

    return "\n\n".join(
        paragraph
        for score, paragraph in scored_paragraphs[:max_results]
    )
