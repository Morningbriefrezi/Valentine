import datetime


def format_message(news_text: str, mode: str) -> str:
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%B %d, %Y")

    if mode == "morning":
        header = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 AI NEWS — Morning Briefing\n"
            f"📅 {date_str}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        footer = (
            "\n━━━━━━━━━━━━━━━━━━━━\n"
            "🌅 Start your day informed. Evening recap coming at 19:00."
        )
    else:
        header = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 AI NEWS — Evening Recap\n"
            f"📅 {date_str}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        footer = (
            "\n━━━━━━━━━━━━━━━━━━━━\n"
            "🌙 That's your AI world for today. See you tomorrow morning."
        )

    return header + news_text + footer


def split_message(text: str, limit: int = 4000) -> list:
    """Split long messages to stay within Telegram's 4096 char limit."""
    if len(text) <= limit:
        return [text]

    parts = []
    while len(text) > limit:
        split_at = text.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit
        parts.append(text[:split_at])
        text = text[split_at:].lstrip()

    if text:
        parts.append(text)

    return parts
