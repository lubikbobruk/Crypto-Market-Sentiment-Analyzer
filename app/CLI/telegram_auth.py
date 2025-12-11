"""Handles Telegram login session."""

import yaml
from telethon.sync import TelegramClient
from telethon import TelegramClient as AsyncClient
from config.config import SESSION_FILE, SECRETS_FILE


def telegram_login():
    """CLI telegram login check with telephone, code and password."""
    with open(SECRETS_FILE, "r") as f:
        creds = yaml.safe_load(f)["telegram"]

    api_id = int(creds["api_id"])
    api_hash = creds["api_hash"]

    client = TelegramClient(str(SESSION_FILE), api_id, api_hash)

    client.start()
    client.disconnect()

    print("Telegram login completed. ✅")


def is_telegram_logged_in() -> bool:
    """
    Check whether the Telegram session file contains a valid authorization.
    """

    if not SESSION_FILE.exists():
        return False

    with open(SECRETS_FILE, "r") as f:
        creds = yaml.safe_load(f)["telegram"]

    api_id = int(creds["api_id"])
    api_hash = creds["api_hash"]

    client = AsyncClient(str(SESSION_FILE), api_id, api_hash)

    try:
        # Streamlit compatible async call runner
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def check():
            await client.connect()
            is_auth = await client.is_user_authorized()
            await client.disconnect()
            return is_auth

        return loop.run_until_complete(check())

    except Exception:
        return False
