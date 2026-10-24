
import re


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[*_`#]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def has_negated_phrase(answer: str, phrase: str) -> bool:
    """Detect common negation immediately before an expected phrase."""
    answer = normalize(answer)
    phrase = normalize(phrase)

    pattern = (
        r"\b(?:not|never|no|doesn't|does not|"
        r"do not|don't|did not|isn't|is not|"
        r"cannot|can't)\s+(?:\w+\s+){0,3}"
        + re.escape(phrase)
    )

    return re.search(pattern, answer) is not None


def check_criteria(answer: str, required_criteria: list) -> dict:
    normalized_answer = normalize(answer)
    results = []

    for alternatives in required_criteria:
        matched = any(
            normalize(phrase) in normalized_answer
            and not has_negated_phrase(answer, phrase)
            for phrase in alternatives
        )
        results.append(matched)

    return {
        "passed": bool(results) and all(results),
        "criteria_passed": sum(results),
        "criteria_total": len(results),
        "criteria_results": results,
    }
