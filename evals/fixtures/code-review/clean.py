def first_matches(items: list[str], prefix: str, limit: int) -> list[str]:
    """Return up to limit matching items from the full input in input order."""
    if limit <= 0:
        return []

    matches = []
    for item in items:
        if not item.startswith(prefix):
            continue
        matches.append(item)
        if len(matches) == limit:
            break
    return matches
