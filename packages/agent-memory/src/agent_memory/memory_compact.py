MAX_COMPACT_CHARS = 1200


def compact(text: str) -> str:
    """
    Reduces text length to fit within semantic memory constraints.
    Uses a robust truncation strategy attempting to preserve semantic boundaries.
    """
    if not text:
        return ""

    if len(text) <= MAX_COMPACT_CHARS:
        return text

    # We want to leave some space for the "..." suffix
    target_length = MAX_COMPACT_CHARS - 3

    # 1. Try sentence boundaries (. ! ?) starting from target_length downwards
    sentence_endings = {".", "!", "?"}
    for i in range(target_length, -1, -1):
        if i < len(text) and text[i] in sentence_endings:
            return text[: i + 1]

    # 2. Try word boundaries (space) starting from target_length downwards
    for i in range(target_length, -1, -1):
        if i < len(text) and text[i] == " ":
            return text[:i].rstrip() + "..."

    # 3. Fallback: Hard truncation at target length
    return text[:target_length].rstrip() + "..."
