# telegram-bot

This repo contains two independent Telegram bot scripts:

1. `bot.py` - the original premium/payments bot (untouched).
2. `broadcast_bot.py` - a lightweight broadcast bot that sends a configurable
   message (e.g. a link) to every group it is added to, on a fixed schedule.

## broadcast_bot.py

### What it does

- Auto-registers any group the moment the bot is added to it.
- Every `INTERVAL` seconds (default **180 = 3 minutes**) it sends the configured
  message to every registered group.
- Auto-removes groups where the bot has been kicked or blocked.
- Owner-only commands are honoured only in private chat with the bot.

### Setup

1. Create the bot with [@BotFather](https://t.me/BotFather) and copy the token.
   Recommended BotFather settings:
   - `/setprivacy` -> **Disable** (so the bot can always read group events).
   - `/setjoingroups` -> **Enable**.
2. Find your own Telegram user id (for example via
   [@userinfobot](https://t.me/userinfobot)).
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Export the required environment variables and run the bot:

   ```bash
   export BOT_TOKEN="123456:ABC..."       # from BotFather
   export OWNER_ID="123456789"             # your Telegram user id
   export INTERVAL="180"                   # seconds between broadcasts (optional)
   export DEFAULT_MSG="https://example.com"  # optional starter message
   python broadcast_bot.py
   ```

5. Add the bot to any group. It registers automatically and starts broadcasting
   once `/start` has been issued (broadcasting is enabled by default on first
   run).

### Owner commands (send privately to the bot)

| Command | Description |
| --- | --- |
| `/setmsg <text>` | Set the broadcast message. You can also reply to a message with `/setmsg` to reuse that text. |
| `/start` | Start/resume broadcasting. |
| `/stop` | Pause broadcasting. |
| `/status` | Show whether broadcasting is on, the interval, the group count, and the current message. |
| `/groups` | List every group chat id the bot is broadcasting to. |
| `/sendnow` | Send the message to every group immediately, without waiting for the next tick. |

### Notes

- Telegram rate-limits bots to ~20 group messages per minute. If you plan to
  broadcast to many groups, keep `INTERVAL` at 180s or higher.
- The bot persists groups and settings to a SQLite database (`broadcast.db` by
  default). Delete it to start fresh.
- Never commit your bot token. Always pass it through `BOT_TOKEN`.
