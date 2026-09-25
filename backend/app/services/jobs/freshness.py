from datetime import datetime, timezone
from typing import Optional


def calculate_freshness_label(published_at: Optional[datetime], updated_at: Optional[datetime] = None) -> str:
    """Calculates human-readable freshness label without fabricating posting age."""
    if not published_at:
        return "Recently verified"

    now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)

    delta = now - published_at
    seconds = max(0, int(delta.total_seconds()))

    if seconds < 3600:
        minutes = max(1, seconds // 60)
        return f"Posted {minutes}m ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"Posted {hours}h ago"
    elif seconds < 172800:
        return "Posted yesterday"
    elif seconds < 604800:
        days = seconds // 86400
        return f"Posted {days} days ago"
    elif seconds < 2592000:
        weeks = max(1, seconds // 604800)
        return f"Posted {weeks} week{'s' if weeks > 1 else ''} ago"
    else:
        return "Active opportunity"
