
from rag.retriever import retrieve_context


def knowledge_search(question: str) -> str:
    """Retrieve relevant evidence from local security notes."""

    context = retrieve_context(question)

    if not context:
        return "No relevant evidence found in the local security notes."

    return context
