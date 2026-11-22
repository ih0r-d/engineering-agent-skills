def add_tag(tag: str, tags: list[str] = []) -> list[str]:
    tags.append(tag)
    return tags


def add_to_explicit_list(tag: str, tags: list[str]) -> None:
    """Append a tag to the supplied list in place."""
    tags.append(tag)
