def first_matches(items: list[str], prefix: str, limit: int) -> list[str]:
    """Return up to limit matching items from the full input in input order."""
    return [item for item in items[:max(0, limit)] if item.startswith(prefix)]
