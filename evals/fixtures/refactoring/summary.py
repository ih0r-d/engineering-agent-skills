def total_active_minutes(entries: list[str]) -> int:
    """Sum the integer minute fields of active records."""
    total = 0
    for entry in entries:
        status, minutes = entry.split(":", 1)
        if status.strip().casefold() == "active":
            total += int(minutes)
    return total


def count_active_entries(entries: list[str]) -> int:
    """Count active records without interpreting their minute fields."""
    count = 0
    for entry in entries:
        status, _minutes = entry.split(":", 1)
        if status.strip().casefold() == "active":
            count += 1
    return count
