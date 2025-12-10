"""
Telegram data collector (sync for CLI, async for Streamlit).
"""
import asyncio
from datetime import timezone
from telethon import TelegramClient
from app.collectors.utils_collectors import is_valid, extract_features

# Sync for CLI

def collect_channel(client, ch, keyword, since, limit):
    msgs = []
    for m in client.iter_messages(ch):
        if not is_valid(m, keyword, since):
            continue
        msgs.append(extract_features(m, ch))
        if len(msgs) >= limit or m.date < since:
            break
    return msgs


def collect_telegram(keyword, chans, limit, period, creds):
    since = utls.get_since_time(period)
    api_id, api_hash = int(creds["api_id"]), creds["api_hash"]
    msgs = []

    with TelegramClient("tg_cli", api_id, api_hash) as client:
        for ch in chans["channels"]:
            try:
                msgs.extend(collect_channel(client, ch, keyword, since, limit))
            except Exception as e:
                print(f"Channel {ch} failed: {e}")

    print(f"Collected {len(msgs)} messages (sync)")
    return msgs

# Async for streamlit

async def collect_channel_async(client, ch, keyword, since, limit):
    msgs = []
    async for m in client.iter_messages(ch, limit=limit * 2):  # oversample
        if not is_valid(m, keyword, since):
            continue
        msgs.append(extract_features(m, ch))
        if len(msgs) >= limit or m.date < since:
            break
    return msgs


async def telegram_collect_async(keyword, chans, limit, period, creds):
    since = utls.get_since_time(period)
    api_id, api_hash = int(creds["api_id"]), creds["api_hash"]
    msgs = []

    async with TelegramClient("tg_async", api_id, api_hash) as client:
        for ch in chans["channels"]:
            try:
                msgs.extend(await collect_channel_async(client, ch, keyword, since, limit))
            except Exception as e:
                print(f"Channel {ch} failed: {e}")

    print(f"Collected {len(msgs)} messages (async)")
    return msgs
