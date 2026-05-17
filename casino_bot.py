import telebot
from telebot import types
import time
import threading
import urllib.parse
import os

from flask import Flask

from database import (
    init_db, save_user, get_user, get_balance, update_balance,
    add_deposit, withdraw_coins, record_game, place_bet, add_winnings,
    get_language, set_language, claim_daily_bonus, get_vip_level,
    get_referral_count, get_referral_earnings_total, get_leaderboard,
    get_user_stats, get_total_users, get_admin_stats, ban_user, unban_user,
    is_banned, get_all_user_ids, escape_html, apply_cashback, VIP_LEVELS,
)
from games import (
    play_slots, create_mines_game, calculate_mines_multiplier,
    reveal_mine_cell, play_dice, play_coinflip, spin_wheel,
    generate_crash_point, check_crash_cashout, CRASH_STEPS,
    SLOT_SYMBOLS, SLOT_PAYOUTS, WHEEL_SEGMENTS, MINES_GRID_SIZE,
)
from i18n import get_string, SUPPORTED_LANGUAGES
from premium_emojis import get_emoji_tag

# ─── Configuration ────────────────────────────────────────────
TOKEN = os.environ.get("BOT_TOKEN", "8325750862:AAE6UCsHjPC8uyqozSzn2FWeCHLM10RWc48")
ADMIN_IDS = [7972155518]

COIN_PACKAGES = [
    {"stars": 50, "coins": 500, "bonus": ""},
    {"stars": 100, "coins": 1100, "bonus": "+10%"},
    {"stars": 250, "coins": 3000, "bonus": "+20%"},
    {"stars": 500, "coins": 6500, "bonus": "+30%"},
]

WITHDRAW_OPTIONS = [
    {"coins": 1000, "stars": 100},
    {"coins": 2500, "stars": 250},
    {"coins": 5000, "stars": 500},
    {"coins": 10000, "stars": 1000},
]

BET_AMOUNTS = [10, 25, 50, 100, 250, 500, 1000]
DICE_TARGETS = [10, 25, 33, 50, 67, 75, 90]
MINES_OPTIONS = [1, 3, 5, 7, 10, 15, 20, 24]

# ─── Bot & Flask ──────────────────────────────────────────────
bot = telebot.TeleBot(TOKEN)
BOT_USERNAME = None
app = Flask(__name__)

# In-memory game states
active_mines = {}
active_bets = {}
admin_states = {}


@app.route('/')
def home():
    return "Casino Bot Running!", 200


@app.route('/health')
def health():
    return "OK", 200


def run_flask():
    app.run(host='0.0.0.0', port=5000)


# ─── Premium Emojis ──────────────────────────────────────────
E_STAR = get_emoji_tag('STAR_GOLD', '\u2b50')
E_FIRE = get_emoji_tag('FIRE', '\U0001f525')
E_GIFT = get_emoji_tag('GIFT', '\U0001f381')
E_PARTY = get_emoji_tag('PARTY', '\U0001f389')
E_CROWN = get_emoji_tag('CROWN', '\U0001f451')
E_MONEY = get_emoji_tag('MONEY_BAG', '\U0001f4b0')
E_ROCKET = get_emoji_tag('ROCKET', '\U0001f680')
E_CHECK = get_emoji_tag('CHECK_MARK', '\u2705')


# ─── Helpers ──────────────────────────────────────────────────
def is_admin(user_id):
    return user_id in ADMIN_IDS


def get_bot_username():
    global BOT_USERNAME
    if not BOT_USERNAME:
        BOT_USERNAME = bot.get_me().username
    return BOT_USERNAME


def lang(user_id):
    return get_language(user_id)


def s(key, user_id, **kwargs):
    return get_string(key, lang(user_id), **kwargs)


# ─── Keyboards ────────────────────────────────────────────────
def main_menu_kb(user_id):
    l = lang(user_id)
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(get_string('games_menu', l), callback_data="menu_games"),
        types.InlineKeyboardButton(get_string('buy_coins', l), callback_data="menu_buy"),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('withdraw', l), callback_data="menu_withdraw"),
        types.InlineKeyboardButton(get_string('daily_bonus', l), callback_data="daily_bonus"),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('referral', l), callback_data="menu_referral"),
        types.InlineKeyboardButton(get_string('stats', l), callback_data="menu_stats"),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('leaderboard', l), callback_data="lb_daily"),
        types.InlineKeyboardButton(get_string('vip_info', l), callback_data="menu_vip"),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('language', l, **{}), callback_data="menu_language"),
    )
    if is_admin(user_id):
        kb.add(types.InlineKeyboardButton("\U0001f6e1\ufe0f Admin Panel", callback_data="admin_panel"))
    return kb


def games_menu_kb(user_id):
    l = lang(user_id)
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(get_string('slots', l), callback_data="game_slots"),
        types.InlineKeyboardButton(get_string('mines', l), callback_data="game_mines"),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('dice', l), callback_data="game_dice"),
        types.InlineKeyboardButton(get_string('coinflip', l), callback_data="game_coinflip"),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('wheel', l), callback_data="game_wheel"),
        types.InlineKeyboardButton(get_string('crash', l), callback_data="game_crash"),
    )
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="back_main"))
    return kb


def bet_keyboard(game_prefix, user_id, extra_row=None):
    l = lang(user_id)
    balance = get_balance(user_id)
    kb = types.InlineKeyboardMarkup(row_width=3)
    btns = []
    for amt in BET_AMOUNTS:
        if amt <= balance:
            btns.append(types.InlineKeyboardButton(
                f"{amt}", callback_data=f"{game_prefix}_bet_{amt}"
            ))
    if not btns:
        btns.append(types.InlineKeyboardButton(
            get_string('buy_coins', l), callback_data="menu_buy"
        ))
    rows = [btns[i:i+3] for i in range(0, len(btns), 3)]
    for row in rows:
        kb.add(*row)
    if extra_row:
        kb.add(*extra_row)
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="menu_games"))
    return kb


def back_main_btn(user_id):
    l = lang(user_id)
    return types.InlineKeyboardButton(get_string('back', l), callback_data="back_main")


def play_again_kb(game_prefix, bet, user_id):
    l = lang(user_id)
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(
            get_string('play_again', l), callback_data=f"{game_prefix}_bet_{bet}"
        ),
        types.InlineKeyboardButton(
            get_string('double_bet', l), callback_data=f"{game_prefix}_bet_{min(bet * 2, 10000)}"
        ),
    )
    kb.add(
        types.InlineKeyboardButton(get_string('games_menu', l), callback_data="menu_games"),
        back_main_btn(user_id),
    )
    return kb


def language_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton(name, callback_data=f"set_lang_{code}")
        for code, name in SUPPORTED_LANGUAGES.items()
    ]
    rows = [btns[i:i+2] for i in range(0, len(btns), 2)]
    for row in rows:
        kb.add(*row)
    return kb


# ─── Welcome Message ─────────────────────────────────────────
def send_welcome(chat_id, user_id):
    l = lang(user_id)
    balance = get_balance(user_id)
    vip = get_vip_level(user_id)
    text = get_string('welcome', l, balance=balance, vip=f"{vip['emoji']} {vip['name']}")
    bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=main_menu_kb(user_id))


# ─── /start Handler ──────────────────────────────────────────
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""

    if is_banned(user_id):
        bot.send_message(message.chat.id, s('banned_message', user_id))
        return

    referrer_id = None
    args = message.text.split()
    if len(args) > 1:
        try:
            ref_id = int(args[1])
            if ref_id != user_id:
                referrer_id = ref_id
        except ValueError:
            pass

    is_new = save_user(user_id, username, referrer_id=referrer_id)

    if is_new and referrer_id:
        try:
            ref_lang = lang(referrer_id)
            bot.send_message(
                referrer_id,
                f"\U0001f389 <b>New Referral!</b>\n\n"
                f"@{escape_html(username) or 'Someone'} joined via your link!",
                parse_mode='HTML'
            )
        except Exception:
            pass

    send_welcome(message.chat.id, user_id)


# ─── Back to Main Menu ───────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data == "back_main")
def handle_back_main(call):
    user_id = call.from_user.id
    if is_banned(user_id):
        return
    save_user(user_id, call.from_user.username or "")
    l = lang(user_id)
    balance = get_balance(user_id)
    vip = get_vip_level(user_id)
    text = get_string('welcome', l, balance=balance, vip=f"{vip['emoji']} {vip['name']}")
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=main_menu_kb(user_id)
        )
    except Exception:
        pass


# ─── Games Menu ───────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data == "menu_games")
def handle_games_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"\U0001f3ae <b>{get_string('games_menu', l)}</b>\n\n"
        f"\U0001f4b0 {get_string('balance_short', l, balance=balance)}\n\n"
        f"Choose a game to play!"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=games_menu_kb(user_id)
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# SLOTS
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "game_slots")
def handle_slots_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"{get_string('slots_title', l)}\n\n"
        f"{get_string('balance_short', l, balance=balance)}\n\n"
        f"{get_string('select_bet', l)}"
    )
    paytable_btn = [types.InlineKeyboardButton("\U0001f4cb Paytable", callback_data="slots_paytable")]
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=bet_keyboard("slots", user_id, extra_row=paytable_btn)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "slots_paytable")
def handle_slots_paytable(call):
    user_id = call.from_user.id
    l = lang(user_id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="game_slots"))
    try:
        bot.edit_message_text(
            get_string('slots_paytable', l),
            call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("slots_bet_"))
def handle_slots_play(call):
    user_id = call.from_user.id
    l = lang(user_id)
    try:
        bet = int(call.data.replace("slots_bet_", ""))
    except ValueError:
        return

    if not place_bet(user_id, bet):
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    result = play_slots(bet)
    record_game(user_id, 'slots', bet, result['multiplier'], result['payout'])

    emojis = result['emojis']
    r_text = get_string('slots_result', l,
        r1=emojis[0], r2=emojis[1], r3=emojis[2],
        result=""
    )

    if result['won']:
        add_winnings(user_id, result['payout'])
        outcome = get_string('game_won', l, bet=bet, multiplier=result['multiplier'], payout=result['payout'])
    else:
        cashback = apply_cashback(user_id, bet, bet)
        outcome = get_string('game_lost', l, bet=bet)
        if cashback > 0:
            outcome += f"\n{get_string('cashback_applied', l, amount=cashback)}"

    final_text = get_string('slots_result', l,
        r1=emojis[0], r2=emojis[1], r3=emojis[2],
        result=outcome
    )

    try:
        bot.edit_message_text(
            final_text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=play_again_kb("slots", bet, user_id)
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# MINES
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "game_mines")
def handle_mines_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"{get_string('mines_title', l)}\n\n"
        f"{get_string('balance_short', l, balance=balance)}\n\n"
        f"{get_string('select_bet', l)}"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=bet_keyboard("mines", user_id)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("mines_bet_"))
def handle_mines_bet(call):
    user_id = call.from_user.id
    l = lang(user_id)
    try:
        bet = int(call.data.replace("mines_bet_", ""))
    except ValueError:
        return

    active_bets[user_id] = {'game': 'mines', 'bet': bet}

    kb = types.InlineKeyboardMarkup(row_width=4)
    btns = [
        types.InlineKeyboardButton(str(n), callback_data=f"mines_count_{n}")
        for n in MINES_OPTIONS
    ]
    rows = [btns[i:i+4] for i in range(0, len(btns), 4)]
    for row in rows:
        kb.add(*row)
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="game_mines"))

    text = (
        f"{get_string('mines_select_count', l)}\n\n"
        f"\U0001f4b0 Bet: {bet} coins"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("mines_count_"))
def handle_mines_start(call):
    user_id = call.from_user.id
    l = lang(user_id)

    if user_id not in active_bets or active_bets[user_id]['game'] != 'mines':
        bot.answer_callback_query(call.id, "Session expired. Start again.", show_alert=True)
        return

    try:
        num_mines = int(call.data.replace("mines_count_", ""))
    except ValueError:
        return

    bet = active_bets[user_id]['bet']
    if not place_bet(user_id, bet):
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    game = create_mines_game(num_mines)
    game['bet'] = bet
    game['user_id'] = user_id
    game['msg_id'] = call.message.message_id
    game['chat_id'] = call.message.chat.id
    active_mines[user_id] = game

    _render_mines_grid(call.message.chat.id, call.message.message_id, user_id)


def _render_mines_grid(chat_id, msg_id, user_id):
    l = lang(user_id)
    game = active_mines.get(user_id)
    if not game:
        return

    num_revealed = len(game['revealed'])
    mult = calculate_mines_multiplier(game['num_mines'], num_revealed)
    potential = int(game['bet'] * mult)

    header = get_string('mines_grid_header', l,
        mines=game['num_mines'], bet=game['bet'], mult=mult, potential=potential
    )

    kb = types.InlineKeyboardMarkup(row_width=5)
    for row_start in range(0, 25, 5):
        row_btns = []
        for i in range(row_start, row_start + 5):
            if i in game['revealed']:
                row_btns.append(types.InlineKeyboardButton(
                    "\U0001f48e", callback_data=f"mines_noop_{i}"
                ))
            else:
                row_btns.append(types.InlineKeyboardButton(
                    "\u2b1c", callback_data=f"mines_reveal_{i}"
                ))
        kb.add(*row_btns)

    if num_revealed > 0:
        kb.add(types.InlineKeyboardButton(
            get_string('mines_cashout', l, mult=mult),
            callback_data="mines_cashout"
        ))

    try:
        bot.edit_message_text(
            header, chat_id, msg_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("mines_reveal_"))
def handle_mines_reveal(call):
    user_id = call.from_user.id
    l = lang(user_id)
    game = active_mines.get(user_id)
    if not game or not game['alive']:
        bot.answer_callback_query(call.id, "No active game!", show_alert=True)
        return

    try:
        cell = int(call.data.replace("mines_reveal_", ""))
    except ValueError:
        return

    result = reveal_mine_cell(game, cell)
    if result is None:
        return

    if result['is_mine']:
        record_game(user_id, 'mines', game['bet'], 0, 0)
        cashback = apply_cashback(user_id, game['bet'], game['bet'])

        kb = types.InlineKeyboardMarkup(row_width=5)
        for row_start in range(0, 25, 5):
            row_btns = []
            for i in range(row_start, row_start + 5):
                if i in game['mines']:
                    row_btns.append(types.InlineKeyboardButton("\U0001f4a5", callback_data=f"mines_noop_{i}"))
                elif i in game['revealed']:
                    row_btns.append(types.InlineKeyboardButton("\U0001f48e", callback_data=f"mines_noop_{i}"))
                else:
                    row_btns.append(types.InlineKeyboardButton("\u2b1c", callback_data=f"mines_noop_{i}"))
            kb.add(*row_btns)

        text = get_string('mines_hit', l, bet=game['bet'])
        if cashback > 0:
            text += f"\n{get_string('cashback_applied', l, amount=cashback)}"

        kb.add(
            types.InlineKeyboardButton(get_string('play_again', l), callback_data="game_mines"),
            back_main_btn(user_id),
        )

        del active_mines[user_id]
        try:
            bot.edit_message_text(
                text, call.message.chat.id, call.message.message_id,
                parse_mode='HTML', reply_markup=kb
            )
        except Exception:
            pass
    else:
        _render_mines_grid(call.message.chat.id, call.message.message_id, user_id)


@bot.callback_query_handler(func=lambda c: c.data == "mines_cashout")
def handle_mines_cashout(call):
    user_id = call.from_user.id
    l = lang(user_id)
    game = active_mines.get(user_id)
    if not game or not game['alive']:
        bot.answer_callback_query(call.id, "No active game!", show_alert=True)
        return

    num_revealed = len(game['revealed'])
    mult = calculate_mines_multiplier(game['num_mines'], num_revealed)
    payout = int(game['bet'] * mult)

    add_winnings(user_id, payout)
    record_game(user_id, 'mines', game['bet'], mult, payout)

    text = get_string('mines_won', l, bet=game['bet'], mult=mult, payout=payout)

    del active_mines[user_id]

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=play_again_kb("mines", game['bet'], user_id)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("mines_noop_"))
def handle_mines_noop(call):
    bot.answer_callback_query(call.id)


# ═══════════════════════════════════════════════════════════════
# DICE
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "game_dice")
def handle_dice_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"{get_string('dice_title', l)}\n\n"
        f"{get_string('balance_short', l, balance=balance)}\n\n"
        f"{get_string('select_bet', l)}"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=bet_keyboard("dice", user_id)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("dice_bet_"))
def handle_dice_bet(call):
    user_id = call.from_user.id
    l = lang(user_id)
    try:
        bet = int(call.data.replace("dice_bet_", ""))
    except ValueError:
        return

    active_bets[user_id] = {'game': 'dice', 'bet': bet}

    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("\u2b06\ufe0f Over", callback_data="dice_dir_over"),
        types.InlineKeyboardButton("\u2b07\ufe0f Under", callback_data="dice_dir_under"),
    )
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="game_dice"))

    text = (
        f"{get_string('dice_title', l)}\n\n"
        f"\U0001f4b0 Bet: {bet} coins\n\n"
        f"Choose direction:"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("dice_dir_"))
def handle_dice_direction(call):
    user_id = call.from_user.id
    l = lang(user_id)
    direction = call.data.replace("dice_dir_", "")

    if user_id not in active_bets or active_bets[user_id]['game'] != 'dice':
        bot.answer_callback_query(call.id, "Session expired.", show_alert=True)
        return

    active_bets[user_id]['direction'] = direction

    kb = types.InlineKeyboardMarkup(row_width=4)
    btns = []
    for t in DICE_TARGETS:
        win_chance = (100 - t) if direction == 'over' else t
        mult = round((1.0 / (win_chance / 100.0)) * 0.97, 2) if win_chance > 0 else 0
        btns.append(types.InlineKeyboardButton(
            f"{t} (x{mult})", callback_data=f"dice_target_{t}"
        ))
    rows = [btns[i:i+3] for i in range(0, len(btns), 3)]
    for row in rows:
        kb.add(*row)
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="game_dice"))

    dir_label = "\u2b06\ufe0f Over" if direction == "over" else "\u2b07\ufe0f Under"
    text = (
        f"{get_string('dice_title', l)}\n\n"
        f"\U0001f4b0 Bet: {active_bets[user_id]['bet']} coins\n"
        f"\U0001f3af Direction: {dir_label}\n\n"
        f"Choose target number:"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("dice_target_"))
def handle_dice_play(call):
    user_id = call.from_user.id
    l = lang(user_id)

    if user_id not in active_bets or active_bets[user_id]['game'] != 'dice':
        bot.answer_callback_query(call.id, "Session expired.", show_alert=True)
        return

    try:
        target = int(call.data.replace("dice_target_", ""))
    except ValueError:
        return

    bet_info = active_bets[user_id]
    bet = bet_info['bet']
    direction = bet_info['direction']

    if not place_bet(user_id, bet):
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    result = play_dice(bet, target, direction)
    record_game(user_id, 'dice', bet, result['multiplier'] if result['won'] else 0, result['payout'])

    if result['won']:
        add_winnings(user_id, result['payout'])
        outcome = get_string('game_won', l, bet=bet, multiplier=result['multiplier'], payout=result['payout'])
    else:
        cashback = apply_cashback(user_id, bet, bet)
        outcome = get_string('game_lost', l, bet=bet)
        if cashback > 0:
            outcome += f"\n{get_string('cashback_applied', l, amount=cashback)}"

    dir_sym = "\u2b06\ufe0f" if direction == "over" else "\u2b07\ufe0f"
    text = get_string('dice_result', l,
        roll=result['roll'], direction=dir_sym, target=target,
        chance=result['win_chance'], result=outcome
    )

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=play_again_kb("dice", bet, user_id)
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# COIN FLIP
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "game_coinflip")
def handle_coinflip_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"{get_string('coinflip_title', l)}\n\n"
        f"{get_string('balance_short', l, balance=balance)}\n\n"
        f"{get_string('select_bet', l)}"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=bet_keyboard("cf", user_id)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("cf_bet_"))
def handle_coinflip_bet(call):
    user_id = call.from_user.id
    l = lang(user_id)
    try:
        bet = int(call.data.replace("cf_bet_", ""))
    except ValueError:
        return

    active_bets[user_id] = {'game': 'coinflip', 'bet': bet}

    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(get_string('heads', l), callback_data="cf_pick_heads"),
        types.InlineKeyboardButton(get_string('tails', l), callback_data="cf_pick_tails"),
    )
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="game_coinflip"))

    text = (
        f"{get_string('coinflip_select', l)}\n\n"
        f"\U0001f4b0 Bet: {bet} coins"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("cf_pick_"))
def handle_coinflip_play(call):
    user_id = call.from_user.id
    l = lang(user_id)

    if user_id not in active_bets or active_bets[user_id]['game'] != 'coinflip':
        bot.answer_callback_query(call.id, "Session expired.", show_alert=True)
        return

    choice = call.data.replace("cf_pick_", "")
    bet = active_bets[user_id]['bet']

    if not place_bet(user_id, bet):
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    result = play_coinflip(bet, choice)
    record_game(user_id, 'coinflip', bet, result['multiplier'], result['payout'])

    result_label = get_string('heads', l) if result['result'] == 'heads' else get_string('tails', l)

    if result['won']:
        add_winnings(user_id, result['payout'])
        outcome = get_string('game_won', l, bet=bet, multiplier=result['multiplier'], payout=result['payout'])
    else:
        cashback = apply_cashback(user_id, bet, bet)
        outcome = get_string('game_lost', l, bet=bet)
        if cashback > 0:
            outcome += f"\n{get_string('cashback_applied', l, amount=cashback)}"

    text = get_string('coinflip_result', l, result=result_label, outcome=outcome)

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=play_again_kb("cf", bet, user_id)
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# WHEEL OF FORTUNE
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "game_wheel")
def handle_wheel_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"{get_string('wheel_segments', l)}\n\n"
        f"{get_string('balance_short', l, balance=balance)}\n\n"
        f"{get_string('select_bet', l)}"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=bet_keyboard("wheel", user_id)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("wheel_bet_"))
def handle_wheel_play(call):
    user_id = call.from_user.id
    l = lang(user_id)
    try:
        bet = int(call.data.replace("wheel_bet_", ""))
    except ValueError:
        return

    if not place_bet(user_id, bet):
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    result = spin_wheel(bet)
    seg = result['segment']
    record_game(user_id, 'wheel', bet, result['multiplier'], result['payout'])

    if result['won']:
        add_winnings(user_id, result['payout'])
        outcome = get_string('game_won', l, bet=bet, multiplier=result['multiplier'], payout=result['payout'])
    else:
        cashback = apply_cashback(user_id, bet, bet)
        outcome = get_string('game_lost', l, bet=bet)
        if cashback > 0:
            outcome += f"\n{get_string('cashback_applied', l, amount=cashback)}"

    text = get_string('wheel_result', l,
        color=seg['color'], name=seg['name'], mult=result['multiplier'],
        result=outcome
    )

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=play_again_kb("wheel", bet, user_id)
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# CRASH
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "game_crash")
def handle_crash_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)
    text = (
        f"{get_string('crash_title', l)}\n\n"
        f"{get_string('balance_short', l, balance=balance)}\n\n"
        f"{get_string('select_bet', l)}"
    )
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=bet_keyboard("crash", user_id)
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("crash_bet_"))
def handle_crash_bet(call):
    user_id = call.from_user.id
    l = lang(user_id)
    try:
        bet = int(call.data.replace("crash_bet_", ""))
    except ValueError:
        return

    if not place_bet(user_id, bet):
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    crash_point = generate_crash_point()
    active_bets[user_id] = {'game': 'crash', 'bet': bet, 'crash_point': crash_point}

    kb = types.InlineKeyboardMarkup(row_width=3)
    btns = []
    for step in CRASH_STEPS:
        emoji = "\U0001f7e2" if step <= 2.0 else ("\U0001f7e1" if step <= 5.0 else "\U0001f534")
        btns.append(types.InlineKeyboardButton(
            f"{emoji} x{step}", callback_data=f"crash_out_{step}"
        ))
    rows = [btns[i:i+3] for i in range(0, len(btns), 3)]
    for row in rows:
        kb.add(*row)
    kb.add(types.InlineKeyboardButton(get_string('back', l), callback_data="game_crash"))

    text = get_string('crash_select_target', l, bet=bet)

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("crash_out_"))
def handle_crash_cashout(call):
    user_id = call.from_user.id
    l = lang(user_id)

    if user_id not in active_bets or active_bets[user_id]['game'] != 'crash':
        bot.answer_callback_query(call.id, "Session expired.", show_alert=True)
        return

    try:
        target = float(call.data.replace("crash_out_", ""))
    except ValueError:
        return

    bet_info = active_bets.pop(user_id)
    bet = bet_info['bet']
    crash_point = bet_info['crash_point']

    won = check_crash_cashout(crash_point, target)

    if won:
        payout = int(bet * target)
        add_winnings(user_id, payout)
        record_game(user_id, 'crash', bet, target, payout)
        text = get_string('crash_result_win', l,
            crash=crash_point, target=target, payout=payout
        )
    else:
        record_game(user_id, 'crash', bet, 0, 0)
        cashback = apply_cashback(user_id, bet, bet)
        text = get_string('crash_result_lose', l,
            crash=crash_point, target=target, bet=bet
        )
        if cashback > 0:
            text += f"\n{get_string('cashback_applied', l, amount=cashback)}"

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=play_again_kb("crash", bet, user_id)
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# BUY COINS (Stars Payment)
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_buy")
def handle_buy_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)

    kb = types.InlineKeyboardMarkup(row_width=1)
    for pkg in COIN_PACKAGES:
        bonus_text = f" ({pkg['bonus']})" if pkg['bonus'] else ""
        kb.add(types.InlineKeyboardButton(
            f"\u2b50 {pkg['stars']} Stars \u27a1 {pkg['coins']:,} Coins{bonus_text}",
            callback_data=f"buy_pkg_{pkg['stars']}"
        ))
    kb.add(back_main_btn(user_id))

    text = get_string('buy_title', l, balance=balance)
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_pkg_"))
def handle_buy_package(call):
    user_id = call.from_user.id
    try:
        stars = int(call.data.replace("buy_pkg_", ""))
    except ValueError:
        return

    pkg = next((p for p in COIN_PACKAGES if p['stars'] == stars), None)
    if not pkg:
        return

    prices = [types.LabeledPrice(label=f"{pkg['coins']} Casino Coins", amount=pkg['stars'])]
    try:
        bot.send_invoice(
            call.message.chat.id,
            title=f"\U0001f3b0 Casino Coins ({pkg['coins']:,})",
            description=f"Get {pkg['coins']:,} casino coins to play games!",
            invoice_payload=f"buy_{user_id}_{pkg['stars']}_{pkg['coins']}",
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter="buy_coins"
        )
    except Exception as e:
        print(f"Invoice error: {e}")


@bot.pre_checkout_query_handler(func=lambda q: True)
def handle_pre_checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    user_id = message.from_user.id
    payment = message.successful_payment
    payload = payment.invoice_payload

    if payload.startswith("buy_"):
        parts = payload.split("_")
        if len(parts) >= 4:
            stars = int(parts[2])
            coins = int(parts[3])
            add_deposit(user_id, stars, coins)

            l = lang(user_id)
            balance = get_balance(user_id)
            text = get_string('purchase_success', l, stars=stars, coins=coins, balance=balance)

            kb = types.InlineKeyboardMarkup()
            kb.add(
                types.InlineKeyboardButton(get_string('games_menu', l), callback_data="menu_games"),
                back_main_btn(user_id),
            )
            bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=kb)

            for admin_id in ADMIN_IDS:
                try:
                    bot.send_message(
                        admin_id,
                        f"\U0001f4b5 <b>New Deposit!</b>\n\n"
                        f"User: <code>{user_id}</code> (@{escape_html(message.from_user.username)})\n"
                        f"Stars: {stars}\n"
                        f"Coins: {coins}",
                        parse_mode='HTML'
                    )
                except Exception:
                    pass

    elif payload.startswith("withdraw_"):
        parts = payload.split("_")
        if len(parts) >= 4:
            coins = int(parts[2])
            stars = int(parts[3])

            l = lang(user_id)
            balance = get_balance(user_id)
            text = get_string('withdraw_success', l, coins=coins, stars=stars, balance=balance)

            kb = types.InlineKeyboardMarkup()
            kb.add(back_main_btn(user_id))
            bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=kb)


# ═══════════════════════════════════════════════════════════════
# WITHDRAW
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_withdraw")
def handle_withdraw_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    balance = get_balance(user_id)

    kb = types.InlineKeyboardMarkup(row_width=1)
    for opt in WITHDRAW_OPTIONS:
        if balance >= opt['coins']:
            kb.add(types.InlineKeyboardButton(
                f"{opt['coins']:,} Coins \u27a1 {opt['stars']} \u2b50",
                callback_data=f"withdraw_{opt['coins']}_{opt['stars']}"
            ))
    kb.add(back_main_btn(user_id))

    text = get_string('withdraw_title', l, balance=balance)
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("withdraw_"))
def handle_withdraw(call):
    user_id = call.from_user.id
    l = lang(user_id)

    parts = call.data.split("_")
    if len(parts) < 3:
        return

    try:
        coins = int(parts[1])
        stars = int(parts[2])
    except ValueError:
        return

    balance = get_balance(user_id)
    if balance < coins:
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    if coins < 1000:
        bot.answer_callback_query(call.id, get_string('withdraw_min_error', l), show_alert=True)
        return

    success = withdraw_coins(user_id, coins, stars)
    if not success:
        bot.answer_callback_query(call.id, get_string('insufficient_balance', l), show_alert=True)
        return

    try:
        bot.send_invoice(
            call.message.chat.id,
            title=f"\U0001f4b8 Withdraw {stars} Stars",
            description=f"Withdraw {coins:,} coins as {stars} Telegram Stars",
            invoice_payload=f"withdraw_{coins}_{stars}",
            provider_token="",
            currency="XTR",
            prices=[types.LabeledPrice(label=f"Withdraw {stars} Stars", amount=stars)],
            start_parameter="withdraw"
        )
    except Exception as e:
        update_balance(user_id, coins)
        print(f"Withdraw invoice error: {e}")
        bot.answer_callback_query(call.id, "Withdrawal failed. Balance restored.", show_alert=True)


# ═══════════════════════════════════════════════════════════════
# DAILY BONUS
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "daily_bonus")
def handle_daily_bonus(call):
    user_id = call.from_user.id
    l = lang(user_id)

    result = claim_daily_bonus(user_id)

    kb = types.InlineKeyboardMarkup()
    kb.add(back_main_btn(user_id))

    if result is None:
        bot.answer_callback_query(call.id, "Error!", show_alert=True)
        return

    if result < 0:
        remaining = abs(result)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        text = get_string('daily_wait', l, hours=hours, minutes=minutes)
    else:
        vip = get_vip_level(user_id)
        text = get_string('daily_claimed', l, amount=result, vip=f"{vip['emoji']} {vip['name']}")

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# REFERRAL
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_referral")
def handle_referral(call):
    user_id = call.from_user.id
    l = lang(user_id)

    count = get_referral_count(user_id)
    earnings = get_referral_earnings_total(user_id)
    username = get_bot_username()
    link = f"https://t.me/{username}?start={user_id}"

    share_text = get_string('referral_share_text', 'en', link=link)
    share_url = f"https://t.me/share/url?url={urllib.parse.quote(link)}&text={urllib.parse.quote(share_text)}"

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(get_string('referral_share', l), url=share_url))
    kb.add(back_main_btn(user_id))

    text = get_string('referral_title', l, count=count, earnings=earnings, link=link)
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_stats")
def handle_stats(call):
    user_id = call.from_user.id
    l = lang(user_id)

    stats = get_user_stats(user_id)
    if not stats:
        return

    user = stats['user']
    vip = get_vip_level(user_id)
    refs = get_referral_count(user_id)
    wagered = user['total_wagered'] or 0
    won = user['total_won'] or 0
    deposited = user['total_deposited'] or 0
    withdrawn = user['total_withdrawn'] or 0
    profit = won - wagered

    text = get_string('stats_title', l,
        balance=user['balance'] or 0,
        vip=f"{vip['emoji']} {vip['name']}",
        deposited=deposited,
        withdrawn=withdrawn,
        wagered=wagered,
        won=won,
        profit=profit,
        games=stats['total_games'],
        wins=stats['wins'],
        referrals=refs
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(back_main_btn(user_id))

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# LEADERBOARD
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data.startswith("lb_"))
def handle_leaderboard(call):
    user_id = call.from_user.id
    l = lang(user_id)
    period = call.data.replace("lb_", "")

    leaders = get_leaderboard(period, 10)
    medals = ["\U0001f947", "\U0001f948", "\U0001f949"] + [f"{i+1}." for i in range(3, 10)]

    if not leaders:
        entries = get_string('leaderboard_empty', l)
    else:
        lines = []
        for i, row in enumerate(leaders):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            name = f"@{row['username']}" if row['username'] else f"User#{row['user_id']}"
            profit = row['net_profit']
            lines.append(f"{medal} {name} \u2014 <b>{profit:+} coins</b>")
        entries = "\n".join(lines)

    period_labels = {"daily": "\U0001f4c5 Daily", "weekly": "\U0001f4c6 Weekly", "monthly": "\U0001f4c5 Monthly"}
    text = f"{get_string('leaderboard_title', l)} ({period_labels.get(period, period)})\n\n{entries}"

    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        types.InlineKeyboardButton("\U0001f4c5 Daily", callback_data="lb_daily"),
        types.InlineKeyboardButton("\U0001f4c6 Weekly", callback_data="lb_weekly"),
        types.InlineKeyboardButton("\U0001f4c5 Monthly", callback_data="lb_monthly"),
    )
    kb.add(back_main_btn(user_id))

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# VIP INFO
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_vip")
def handle_vip_info(call):
    user_id = call.from_user.id
    l = lang(user_id)
    vip = get_vip_level(user_id)
    user = get_user(user_id)
    wagered = user['total_wagered'] if user else 0

    text = get_string('vip_title', l,
        current=f"{vip['emoji']} {vip['name']}",
        wagered=wagered or 0
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(back_main_btn(user_id))

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# LANGUAGE
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "menu_language")
def handle_language_menu(call):
    user_id = call.from_user.id
    l = lang(user_id)
    text = get_string('select_language', l)
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            reply_markup=language_kb()
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith("set_lang_"))
def handle_set_language(call):
    user_id = call.from_user.id
    new_lang = call.data.replace("set_lang_", "")
    if new_lang in SUPPORTED_LANGUAGES:
        set_language(user_id, new_lang)
        bot.answer_callback_query(call.id, f"Language set to {SUPPORTED_LANGUAGES[new_lang]}!")
    handle_back_main(call)


# ═══════════════════════════════════════════════════════════════
# ADMIN PANEL
# ═══════════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: c.data == "admin_panel")
def handle_admin_panel(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return

    stats = get_admin_stats()
    text = get_string('admin_panel', 'en', **stats)

    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("\U0001f4e2 Broadcast", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("\U0001f6ab Ban User", callback_data="admin_ban"),
    )
    kb.add(
        types.InlineKeyboardButton("\u2705 Unban User", callback_data="admin_unban"),
        types.InlineKeyboardButton("\U0001f4b0 Give Coins", callback_data="admin_give"),
    )
    kb.add(back_main_btn(user_id))

    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode='HTML', reply_markup=kb
        )
    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast")
def handle_admin_broadcast(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    admin_states[user_id] = 'broadcast'
    bot.send_message(call.message.chat.id, get_string('admin_broadcast_prompt', 'en'))


@bot.callback_query_handler(func=lambda c: c.data == "admin_ban")
def handle_admin_ban_prompt(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    admin_states[user_id] = 'ban'
    bot.send_message(call.message.chat.id, get_string('admin_ban_prompt', 'en'))


@bot.callback_query_handler(func=lambda c: c.data == "admin_unban")
def handle_admin_unban_prompt(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    admin_states[user_id] = 'unban'
    bot.send_message(call.message.chat.id, get_string('admin_unban_prompt', 'en'))


@bot.callback_query_handler(func=lambda c: c.data == "admin_give")
def handle_admin_give_prompt(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    admin_states[user_id] = 'give'
    bot.send_message(call.message.chat.id, "Send: user_id amount\nExample: 123456789 1000")


@bot.message_handler(func=lambda m: m.from_user.id in admin_states)
def handle_admin_action(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    state = admin_states.pop(user_id, None)
    if not state:
        return

    if state == 'broadcast':
        text = message.text or message.caption or ""
        user_ids = get_all_user_ids()
        sent = 0
        for uid in user_ids:
            try:
                if message.content_type == 'text':
                    bot.send_message(uid, text, parse_mode='HTML')
                else:
                    bot.copy_message(uid, message.chat.id, message.message_id)
                sent += 1
                time.sleep(0.05)
            except Exception:
                pass
        bot.send_message(
            message.chat.id,
            get_string('admin_broadcast_sent', 'en', count=sent)
        )

    elif state == 'ban':
        try:
            target_id = int(message.text.strip())
            ban_user(target_id)
            bot.send_message(message.chat.id, get_string('admin_banned', 'en', user_id=target_id))
        except ValueError:
            bot.send_message(message.chat.id, "Invalid user ID.")

    elif state == 'unban':
        try:
            target_id = int(message.text.strip())
            unban_user(target_id)
            bot.send_message(message.chat.id, get_string('admin_unbanned', 'en', user_id=target_id))
        except ValueError:
            bot.send_message(message.chat.id, "Invalid user ID.")

    elif state == 'give':
        try:
            parts = message.text.strip().split()
            target_id = int(parts[0])
            amount = int(parts[1])
            update_balance(target_id, amount)
            bot.send_message(
                message.chat.id,
                f"\u2705 Gave {amount} coins to user {target_id}."
            )
            try:
                bot.send_message(
                    target_id,
                    f"\U0001f381 <b>Admin Gift!</b>\n\n"
                    f"You received <b>{amount} coins</b> from admin!",
                    parse_mode='HTML'
                )
            except Exception:
                pass
        except (ValueError, IndexError):
            bot.send_message(message.chat.id, "Invalid format. Use: user_id amount")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    print("\U0001f3b0 Casino Bot starting...")
    init_db()
    print("\u2705 Database initialized")

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("\u2705 Flask health server started on port 5000")

    print("\U0001f680 Bot polling started!")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


if __name__ == '__main__':
    main()
