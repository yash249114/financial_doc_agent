# api/services/reasoning_service.py
from typing import Dict, List

def explain_reasoning(text: str, predicted_label: str, keywords: Dict[str, List[str]]) -> str:
    """
    Explains why a document was classified into a specific category.
    Detects which indicative keywords influenced the classification.
    """
    if not text or predicted_label not in keywords:
        return (
            "No reasoning could be generated because the document text "
            "is empty or the classification label is unrecognized."
        )

    text_lower = text.lower()
    matched_keywords = [kw for kw in keywords[predicted_label] if kw in text_lower]

    if not matched_keywords:
        return (
            f"The document was classified as '{predicted_label}' based on general text context "
            "and semantic similarity with financial documents."
        )

    reasoning = (
        f"The document was classified as **{predicted_label}** because it contains "
        f"key indicative terms like: {', '.join(matched_keywords[:6])}."
    )

    if len(matched_keywords) > 6:
        reasoning += " ...and more."

    return reasoning


def get_metrics(start_time):
    """
    Measures runtime and system CPU usage.
    """
    import time, psutil
    latency = round(time.time() - start_time, 3)
    cpu_percent = psutil.cpu_percent(interval=0.1)
    return {"latency_s": latency, "cpu_percent": cpu_percent}
