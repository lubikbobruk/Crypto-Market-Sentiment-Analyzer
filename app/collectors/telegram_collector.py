"""
Telegram data collector for Crypto Market Sentiment Analyzer.

Fetches messages from selected public Telegram crypto channels
and saves them into data/raw/telegram/telegram_<period>_<keyword>_<date>.csv
"""

from telethon.sync import TelegramClient
from datetime import timezone
from app.collectors import utils_collectors as utls

def collect_channel(client, name, keyword, since_time, limit):
    msgs = []
    for m in client.iter_messages(name):
        if not m.text or m.date < since_time:
            break
        if keyword and keyword.lower() not in m.text.lower():
            continue
        if not utls.is_valid_post(m.text):
            continue
        msgs.append({
            "channel": name,
            "id": m.id,
            "datetime": m.date.astimezone(timezone.utc).isoformat(),
            "text": m.text.strip(),
            "views": m.views,
        })
        if len(msgs) >= limit:
            break
    return msgs

def collect_telegram(keyword, chans, limit, period, creds):
    """Collect messages from all Telegram channels."""
    since_time = utls.get_since_time(period)
    all_msgs = []

    with TelegramClient("crypto_session", int(creds["api_id"]), creds["api_hash"]) as client:
        for ch in chans["channels"]:
            all_msgs.extend(collect_channel(client, ch, keyword, since_time, limit))

    print(f"Collected {len(all_msgs)} messages")
    return all_msgs


def main():
    chans, limit, period = utls.load_defaults("telegram")
    creds = utls.load_api("telegram")
    keyword = input("Your query: ").strip() or None

    all_msgs = collect_telegram(keyword, chans, limit, period, creds)
    utls.save_to_csv(all_msgs, "telegram", f"telegram_{period}")


if __name__ == "__main__":
    main()
