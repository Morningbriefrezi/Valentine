import json
import urllib.request
import urllib.parse

from config import ANTHROPIC_API_KEY

MORNING_PROMPT = """You are an AI news researcher. Search the web RIGHT NOW and find the most important AI news from the last 24 hours.

Focus ONLY on these topics:
- New AI models released or announced (LLMs, multimodal, etc.)
- Video generation AI models and updates (Sora, Runway, Kling, etc.)
- AI for data / data models / analytics AI tools
- AGI research, breakthroughs, and discussions
- Major AI company updates (OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, xAI, etc.)
- AI regulation and policy that affects the industry

For each news item provide:
1. A clear headline
2. 2-3 sentence summary of what happened
3. Why it matters

Find 5-7 of the most significant stories. Be specific with names, numbers, and dates. Only include real, verified news from today or yesterday."""

EVENING_PROMPT = """You are an AI news researcher. Search the web RIGHT NOW and find AI news and analysis from the last 24 hours.

Focus ONLY on these topics:
- Deep dives: new AI model benchmarks, performance comparisons, technical details
- Video AI and image generation model updates and new releases
- AI tools and products launched today for developers or consumers
- AGI timeline discussions, safety research, alignment news
- AI investment, funding rounds, and business news
- Interesting AI research papers published today

For each news item provide:
1. A clear headline
2. 2-3 sentence summary
3. Why it matters for AI's future

Find 5-7 of the most significant stories. Be specific with names, numbers, and dates. Only include real news from today or yesterday."""


def fetch_ai_news(mode: str) -> str:
    """Call Claude API with web search to get real-time AI news."""

    prompt = MORNING_PROMPT if mode == "morning" else EVENING_PROMPT

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search"
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
