"""One-time setup: connect your Telegram bot and store secrets in GitHub.

Run in your own Terminal (not inside a chat), from the repo folder:
    .venv/bin/python scripts/setup_secrets.py sidequestlabs-tech/m365-docs-watch

Secrets are typed hidden and go straight to GitHub via `gh secret set`. Nothing is printed or saved locally.
"""
import getpass
import subprocess
import sys
import time

import requests

API = "https://api.telegram.org/bot{token}/{method}"


def find_chat_id(updates: dict) -> str | None:
    """Chat id of the most recent private message sent to the bot."""
    for upd in reversed(updates.get("result", [])):
        chat = (upd.get("message") or {}).get("chat") or {}
        if chat.get("type") == "private":
            return str(chat["id"])
    return None


def tg(token: str, method: str, **params) -> dict:
    r = requests.post(API.format(token=token, method=method), json=params, timeout=30)
    if r.status_code != 200:
        sys.exit(f"Telegram {method} failed (HTTP {r.status_code}). Check the bot token and try again.")
    return r.json()


def gh_secret(repo: str, name: str, value: str) -> None:
    subprocess.run(["gh", "secret", "set", name, "-R", repo], input=value, text=True, check=True,
                   stdout=subprocess.DEVNULL)
    print(f"  ✓ stored {name} in GitHub")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: setup_secrets.py <owner/repo>")
    repo = sys.argv[1]

    token = getpass.getpass("Paste your Telegram bot token from @BotFather (hidden): ").strip()
    bot = tg(token, "getMe")["result"]
    print(f"Bot found: @{bot['username']}")
    input(f"Open Telegram, send any message to @{bot['username']}, then press Enter here… ")

    chat_id = None
    for _ in range(10):
        chat_id = find_chat_id(tg(token, "getUpdates"))
        if chat_id:
            break
        time.sleep(3)
    if not chat_id:
        sys.exit("No message received yet. Send the bot a message and run this again.")

    tg(token, "sendMessage", chat_id=chat_id,
       text="✅ M365 docs watcher connected. Alerts will arrive in this chat.")
    print("Test message sent — check Telegram.")

    gh_secret(repo, "TELEGRAM_BOT_TOKEN", token)
    gh_secret(repo, "TELEGRAM_CHAT_ID", chat_id)

    key = getpass.getpass("Paste your Claude API key (hidden; Enter to skip for now): ").strip()
    if key:
        gh_secret(repo, "ANTHROPIC_API_KEY", key)
    print("Done.")


if __name__ == "__main__":
    main()
