import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
MODE = os.environ.get("MODE", "morning")  # "morning" or "evening"
