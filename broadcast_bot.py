"""Telegram broadcast bot.

The bot sends a configurable message to every group chat it has been added
to, at a fixed interval (default 3 minutes). Groups are discovered
automatically the moment the bot is added, so no manual registration is
required.

Runtime configuration is read from environment variables:

* ``BOT_TOKEN``    - Telegram bot token from @BotFather (required).
* ``OWNER_ID``     - Telegram user id allowed to control the bot
  (required). Can be a comma separated list for multiple owners.
* ``INTERVAL``     - Seconds between broadcasts. Defaults to ``180``.
* ``DB_PATH``      - Path to the SQLite database. Defaults to
  ``broadcast.db`` next to this file.
* ``DEFAULT_MSG``  - Optional default message used before the owner sets
  one with ``/setmsg``.

Owner commands (send privately to the bot):

* ``/setmsg <text>``  - Set the broadcast message (or reply to a message
  with ``/setmsg`` to reuse its text).
* ``/start``          - Start automatic broadcasting.
* ``/stop``           - Stop automatic broadcasting.
* ``/status``         - Show current message, interval and number of
  registered groups.
* ``/groups``         - List chat ids the bot is currently broadcasting
  to.
* ``/sendnow``        - Send the message immediately to all groups
  without waiting for the next tick.

Important: disable the bot's "privacy mode" in @BotFather
(``/setprivacy`` -> ``Disable``) so it can reliably see the events it
needs. Even with privacy mode on, ``my_chat_member`` updates still fire,
so auto-registration on join will work either way.
"""

from __future__ import annotations

import logging
import os
import sqlite3
import sys
import threading
import time
from typing import Iterable

import telebot
from telebot import types

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("broadcast_bot")


def _read_owner_ids(raw: str) -> list[int]:
    ids: list[int] = []
    for piece in raw.split(","):
        piece = piece.strip()
        if not piece:
            continue
        try:
            ids.append(int(piece))
        except ValueError:
            logger.warning("Ignoring invalid OWNER_ID entry: %r", piece)
    return ids


BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
OWNER_IDS = _read_owner_ids(os.environ.get("OWNER_ID", ""))
INTERVAL = max(30, int(os.environ.get("INTERVAL", "180")))
DB_PATH = os.environ.get(
    "DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "broadcast.db"),
)
DEFAULT_MSG = os.environ.get("DEFAULT_MSG", "")

if not BOT_TOKEN:
    print("BOT_TOKEN environment variable is required.", file=sys.stderr)
    sys.exit(1)
if not OWNER_IDS:
    print(
        "OWNER_ID environment variable is required (your Telegram user id).",
        file=sys.stderr,
    )
    sys.exit(1)


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                title TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )"""
        )
        conn.commit()


def get_setting(key: str, default: str = "") -> str:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
    return row[0] if row else default


def set_setting(key: str, value: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        conn.commit()


def add_group(chat_id: int, title: str | None) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO groups (chat_id, title) VALUES (?, ?)",
            (chat_id, title or ""),
        )
        conn.commit()


def remove_group(chat_id: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM groups WHERE chat_id = ?", (chat_id,))
        conn.commit()


def list_groups() -> list[tuple[int, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        return [
            (row[0], row[1] or "")
            for row in conn.execute(
                "SELECT chat_id, title FROM groups ORDER BY added_at"
            ).fetchall()
        ]


bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


def is_owner(user_id: int) -> bool:
    return user_id in OWNER_IDS


def owner_only(handler):
    def wrapper(message: types.Message):
        if not message.from_user or not is_owner(message.from_user.id):
            return
        return handler(message)

    wrapper.__name__ = handler.__name__
    return wrapper


@bot.my_chat_member_handler()
def on_my_chat_member(update: types.ChatMemberUpdated) -> None:
    chat = update.chat
    new_status = update.new_chat_member.status
    if chat.type in ("group", "supergroup"):
        if new_status in ("member", "administrator"):
            add_group(chat.id, chat.title)
            logger.info(
                "Registered group %s (%s) via chat member update",
                chat.id,
                chat.title,
            )
        elif new_status in ("left", "kicked"):
            remove_group(chat.id)
            logger.info(
                "Removed group %s (%s) via chat member update", chat.id, chat.title
            )


@bot.message_handler(content_types=["new_chat_members"])
def on_new_chat_members(message: types.Message) -> None:
    me = bot.get_me()
    for member in message.new_chat_members or []:
        if member.id == me.id and message.chat.type in ("group", "supergroup"):
            add_group(message.chat.id, message.chat.title)
            logger.info(
                "Registered group %s (%s) via new_chat_members",
                message.chat.id,
                message.chat.title,
            )


@bot.message_handler(content_types=["left_chat_member"])
def on_left_chat_member(message: types.Message) -> None:
    left = message.left_chat_member
    if left is None:
        return
    me = bot.get_me()
    if left.id == me.id:
        remove_group(message.chat.id)
        logger.info("Removed group %s (%s)", message.chat.id, message.chat.title)


@bot.message_handler(commands=["start", "help"], chat_types=["private"])
@owner_only
def cmd_start(message: types.Message) -> None:
    set_setting("enabled", "1")
    bot.reply_to(
        message,
        "Broadcasting is ON.\n\n"
        "Commands:\n"
        "/setmsg <text> - set the broadcast message\n"
        "/stop - pause broadcasting\n"
        "/start - resume broadcasting\n"
        "/status - show current settings\n"
        "/groups - list registered groups\n"
        "/sendnow - send the message immediately",
    )


@bot.message_handler(commands=["stop"], chat_types=["private"])
@owner_only
def cmd_stop(message: types.Message) -> None:
    set_setting("enabled", "0")
    bot.reply_to(message, "Broadcasting paused. Send /start to resume.")


@bot.message_handler(commands=["setmsg"], chat_types=["private"])
@owner_only
def cmd_setmsg(message: types.Message) -> None:
    text: str | None = None
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    else:
        parts = message.text.split(None, 1) if message.text else []
        if len(parts) == 2:
            text = parts[1]
    if not text:
        bot.reply_to(
            message,
            "Usage: /setmsg <text>\nOr reply to a message with /setmsg "
            "to use that message's text.",
        )
        return
    set_setting("message", text)
    bot.reply_to(message, f"Broadcast message updated ({len(text)} chars).")


@bot.message_handler(commands=["status"], chat_types=["private"])
@owner_only
def cmd_status(message: types.Message) -> None:
    enabled = get_setting("enabled", "0") == "1"
    msg = get_setting("message", DEFAULT_MSG)
    groups = list_groups()
    preview = (msg[:200] + "...") if len(msg) > 200 else msg
    bot.reply_to(
        message,
        "Status:\n"
        f"- Enabled: {'yes' if enabled else 'no'}\n"
        f"- Interval: {INTERVAL}s\n"
        f"- Groups: {len(groups)}\n"
        f"- Message:\n{preview or '(not set)'}",
    )


@bot.message_handler(commands=["groups"], chat_types=["private"])
@owner_only
def cmd_groups(message: types.Message) -> None:
    groups = list_groups()
    if not groups:
        bot.reply_to(message, "No groups registered yet. Add the bot to a group.")
        return
    lines = [f"{chat_id} - {title or '(no title)'}" for chat_id, title in groups]
    bot.reply_to(message, "Groups:\n" + "\n".join(lines))


@bot.message_handler(commands=["sendnow"], chat_types=["private"])
@owner_only
def cmd_sendnow(message: types.Message) -> None:
    sent, failed = broadcast_once()
    bot.reply_to(message, f"Sent to {sent} group(s), {failed} failed.")


def _send_to_group(chat_id: int, text: str) -> bool:
    try:
        bot.send_message(chat_id, text, disable_web_page_preview=False)
        return True
    except telebot.apihelper.ApiTelegramException as exc:
        if exc.error_code in (400, 403):
            logger.info(
                "Dropping group %s after API error %s: %s",
                chat_id,
                exc.error_code,
                exc.description,
            )
            remove_group(chat_id)
        else:
            logger.warning("Failed sending to %s: %s", chat_id, exc)
        return False
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Unexpected error sending to %s: %s", chat_id, exc)
        return False


def broadcast_once() -> tuple[int, int]:
    msg = get_setting("message", DEFAULT_MSG)
    if not msg:
        logger.info("Skipping broadcast: no message configured")
        return 0, 0
    sent = failed = 0
    for chat_id, _title in list_groups():
        if _send_to_group(chat_id, msg):
            sent += 1
        else:
            failed += 1
    if sent or failed:
        logger.info("Broadcast done: sent=%s failed=%s", sent, failed)
    return sent, failed


def broadcast_loop(stop_event: threading.Event) -> None:
    logger.info("Broadcast loop started (interval=%ss)", INTERVAL)
    while not stop_event.is_set():
        try:
            if get_setting("enabled", "0") == "1":
                broadcast_once()
        except Exception:  # pragma: no cover - defensive
            logger.exception("Error during broadcast tick")
        stop_event.wait(INTERVAL)


def notify_owners(text: str) -> None:
    for owner_id in OWNER_IDS:
        try:
            bot.send_message(owner_id, text)
        except Exception as exc:
            logger.info("Could not DM owner %s: %s", owner_id, exc)


def main() -> None:
    init_db()
    if DEFAULT_MSG and not get_setting("message", ""):
        set_setting("message", DEFAULT_MSG)
    if get_setting("enabled", "") == "":
        set_setting("enabled", "1")

    me = bot.get_me()
    logger.info("Logged in as @%s (%s)", me.username, me.id)
    notify_owners(
        f"Broadcast bot started as @{me.username}. "
        f"Interval: {INTERVAL}s. Send /status for details."
    )

    stop_event = threading.Event()
    thread = threading.Thread(
        target=broadcast_loop, args=(stop_event,), daemon=True
    )
    thread.start()

    try:
        bot.infinity_polling(
            timeout=30, long_polling_timeout=30, allowed_updates=None
        )
    finally:
        stop_event.set()


if __name__ == "__main__":
    main()
