import json
import urllib.request
import urllib.parse

from config import ANTHROPIC_API_KEY

MORNING_PROMPT = """Search for the 5 most important AI news stories from the last 24 hours.

Topics: new AI models, video/image AI, AGI breakthroughs, major company updates (OpenAI, Anthropic, Google, Meta, xAI, Mistral), AI regulation.

For each story:
1. Headline
2. 2-sentence summary
3. Why it matters

Use specific names, numbers, and dates. Only real, verified news."""

EVENING_PROMPT = """Search for the 5 most significant AI news stories from the last 24 hours.

Topics: model benchmarks, video/image AI updates, new AI tools for developers or consumers, AGI/safety research, AI funding, notable research papers.

For each story:
1. Headline
2. 2-sentence summary
3. Why it matters for AI's future

Use specific names, numbers, and dates. Only real news."""


def fetch_ai_news(mode: str) -> str:
    """Call Claude API with web search to get real-time AI news."""

    prompt = MORNING_PROMPT if mode == "morning" else EVENING_PROMPT

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1200,
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "web-search-2025-03-05"
        }
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    # Extract all text blocks from the response
    text_parts = []
    for block in body.get("content", []):
        if block.get("type") == "text":
            text_parts.append(block["text"])

    return "\n".join(text_parts).strip()
