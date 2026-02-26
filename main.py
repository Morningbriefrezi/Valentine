import sys
import urllib.parse
import urllib.request

from config import TELEGRAM_TOKEN, CHAT_ID, MODE
from fetcher import fetch_ai_news
from formatter import format_message, split_message


def send_telegram(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": "true"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            body = resp.read().decode("utf-8")
            raise RuntimeError(f"Telegram error: {resp.status} {body}")


def main():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_TOKEN or CHAT_ID", file=sys.stderr)
        sys.exit(1)

    if not __import__("config").ANTHROPIC_API_KEY:
        print("Missing ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching AI news [{MODE}]...")
    news = fetch_ai_news(MODE)

    if not news:
        print("No news returned.", file=sys.stderr)
        sys.exit(1)

    full_message = format_message(news, MODE)
    parts = split_message(full_message)

    for i, part in enumerate(parts):
        send_telegram(TELEGRAM_TOKEN, CHAT_ID, part)
        print(f"Sent part {i+1}/{len(parts)}")

    print("Done.")


if __name__ == "__main__":
    main()
