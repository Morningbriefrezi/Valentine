import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
ANTHROPIC_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODE = os.environ.get("MODE", "morning")  # "morning" or "evening"
