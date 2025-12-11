"""
Telegram data collector (sync for CLI, async for Streamlit).
"""
from telethon import TelegramClient
from config.config import SESSION_FILE
from app.collectors.utils_collectors import is_valid, extract_features, get_since_time

# -------------------
# Sync version (CLI)
# -------------------

def collect_channel(client, ch, keyword, since, limit):
    msgs = []
    for m in client.iter_messages(ch, limit=limit):
        if not is_valid(m, keyword, since):
            continue

        msgs.append(extract_features(m, ch))

        if len(msgs) >= limit or m.date < since:
            break

    return msgs

def collect_telegram(keyword, chans, limit, period, creds):
    since = get_since_time(period)
    api_id = int(creds["api_id"])
    api_hash = creds["api_hash"]

    msgs = []

    with TelegramClient(str(SESSION_FILE), api_id, api_hash) as client:
        for ch in chans["channels"]:
            try:
                msgs.extend(collect_channel(client, ch, keyword, since, limit))
            except Exception as e:
                print(f"Channel {ch} failed: {e}")

    print(f"Collected {len(msgs)} messages (sync)")
    return msgs


# --------------------------
# Async version (Streamlit) 
# --------------------------

async def collect_channel_async(client, ch, keyword, since, limit):
    msgs = []
    async for m in client.iter_messages(ch, limit=limit):
        if not is_valid(m, keyword, since):
            continue

        msgs.append(extract_features(m, ch))

        if len(msgs) >= limit or m.date < since:
            break

    return msgs

async def telegram_collect_async(keyword, chans, limit, period, creds):
    since = get_since_time(period)
    api_id = int(creds["api_id"])
    api_hash = creds["api_hash"]

    msgs = []

    async with TelegramClient(str(SESSION_FILE), api_id, api_hash) as client:
        for ch in chans["channels"]:
            try:
                batch = await collect_channel_async(client, ch, keyword, since, limit)
                msgs.extend(batch)
            except Exception as e:
                print(f"Channel {ch} failed: {e}")

    print(f"Collected {len(msgs)} messages (async)")
    return msgs
