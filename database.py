import sqlite3
import time
import os

DATABASE = 'casino.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0,
                total_deposited INTEGER DEFAULT 0,
                total_withdrawn INTEGER DEFAULT 0,
                total_wagered INTEGER DEFAULT 0,
                total_won INTEGER DEFAULT 0,
                language TEXT DEFAULT 'en',
                referrer_id INTEGER,
                daily_bonus_last INTEGER DEFAULT 0,
                created_at INTEGER,
                last_active INTEGER
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tx_type TEXT NOT NULL,
                amount INTEGER NOT NULL,
                details TEXT DEFAULT '',
                created_at INTEGER
            );

            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                game_type TEXT NOT NULL,
                bet_amount INTEGER NOT NULL,
                multiplier REAL DEFAULT 0,
                payout INTEGER DEFAULT 0,
                created_at INTEGER
            );

            CREATE TABLE IF NOT EXISTS referral_earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER NOT NULL,
                from_user_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                level INTEGER DEFAULT 1,
                created_at INTEGER
            );

            CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY,
                banned_at INTEGER
            );

            CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id);
            CREATE INDEX IF NOT EXISTS idx_game_history_user ON game_history(user_id);
            CREATE INDEX IF NOT EXISTS idx_game_history_time ON game_history(created_at);
            CREATE INDEX IF NOT EXISTS idx_referral_earnings_referrer ON referral_earnings(referrer_id);
            CREATE INDEX IF NOT EXISTS idx_users_referrer ON users(referrer_id);
        ''')
        conn.commit()


def save_user(user_id, username, language='en', referrer_id=None):
    now = int(time.time())
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        if c.fetchone():
            c.execute(
                'UPDATE users SET username = ?, last_active = ? WHERE user_id = ?',
                (username, now, user_id)
            )
            return False
        else:
            c.execute(
                'INSERT INTO users (user_id, username, language, referrer_id, created_at, last_active) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, username, language, referrer_id, now, now)
            )
            conn.commit()
            return True


def get_user(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return c.fetchone()


def get_balance(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        return row['balance'] if row else 0


def update_balance(user_id, amount):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()


def add_deposit(user_id, stars, coins):
    now = int(time.time())
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            'UPDATE users SET balance = balance + ?, total_deposited = total_deposited + ? WHERE user_id = ?',
            (coins, coins, user_id)
        )
        c.execute(
            'INSERT INTO transactions (user_id, tx_type, amount, details, created_at) VALUES (?, ?, ?, ?, ?)',
            (user_id, 'deposit', coins, f'{stars} stars -> {coins} coins', now)
        )
        conn.commit()

    process_referral_bonus(user_id, coins)


def process_referral_bonus(user_id, deposit_amount):
    now = int(time.time())
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT referrer_id FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        if not row or not row['referrer_id']:
            return

        referrer_id = row['referrer_id']
        bonus_l1 = int(deposit_amount * 0.10)
        if bonus_l1 > 0:
            c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus_l1, referrer_id))
            c.execute(
                'INSERT INTO referral_earnings (referrer_id, from_user_id, amount, level, created_at) '
                'VALUES (?, ?, ?, 1, ?)',
                (referrer_id, user_id, bonus_l1, now)
            )
            c.execute(
                'INSERT INTO transactions (user_id, tx_type, amount, details, created_at) VALUES (?, ?, ?, ?, ?)',
                (referrer_id, 'referral_bonus', bonus_l1, f'L1 from user {user_id}', now)
            )

        c.execute('SELECT referrer_id FROM users WHERE user_id = ?', (referrer_id,))
        row2 = c.fetchone()
        if row2 and row2['referrer_id']:
            referrer_l2 = row2['referrer_id']
            bonus_l2 = int(deposit_amount * 0.05)
            if bonus_l2 > 0:
                c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus_l2, referrer_l2))
                c.execute(
                    'INSERT INTO referral_earnings (referrer_id, from_user_id, amount, level, created_at) '
                    'VALUES (?, ?, ?, 2, ?)',
                    (referrer_l2, user_id, bonus_l2, now)
                )
                c.execute(
                    'INSERT INTO transactions (user_id, tx_type, amount, details, created_at) VALUES (?, ?, ?, ?, ?)',
                    (referrer_l2, 'referral_bonus', bonus_l2, f'L2 from user {user_id}', now)
                )

        conn.commit()


def withdraw_coins(user_id, coins, stars):
    now = int(time.time())
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        if not row or row['balance'] < coins:
            return False
        c.execute(
            'UPDATE users SET balance = balance - ?, total_withdrawn = total_withdrawn + ? WHERE user_id = ?',
            (coins, coins, user_id)
        )
        c.execute(
            'INSERT INTO transactions (user_id, tx_type, amount, details, created_at) VALUES (?, ?, ?, ?, ?)',
            (user_id, 'withdraw', -coins, f'{coins} coins -> {stars} stars', now)
        )
        conn.commit()
        return True


def record_game(user_id, game_type, bet_amount, multiplier, payout):
    now = int(time.time())
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            'UPDATE users SET total_wagered = total_wagered + ?, total_won = total_won + ? WHERE user_id = ?',
            (bet_amount, payout, user_id)
        )
        c.execute(
            'INSERT INTO game_history (user_id, game_type, bet_amount, multiplier, payout, created_at) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, game_type, bet_amount, multiplier, payout, now)
        )
        conn.commit()


def place_bet(user_id, amount):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        if not row or row['balance'] < amount:
            return False
        c.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        return True


def add_winnings(user_id, amount):
    if amount <= 0:
        return
    with get_db() as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()


def get_language(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        return row['language'] if row and row['language'] else 'en'


def set_language(user_id, lang):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET language = ? WHERE user_id = ?', (lang, user_id))
        conn.commit()


def claim_daily_bonus(user_id):
    now = int(time.time())
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT daily_bonus_last, total_wagered FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        if not row:
            return None

        last_claim = row['daily_bonus_last'] or 0
        elapsed = now - last_claim
        if elapsed < 86400:
            remaining = 86400 - elapsed
            return -remaining

        vip = get_vip_level_by_wagered(row['total_wagered'] or 0)
        bonus = vip['daily_bonus']

        c.execute(
            'UPDATE users SET balance = balance + ?, daily_bonus_last = ? WHERE user_id = ?',
            (bonus, now, user_id)
        )
        c.execute(
            'INSERT INTO transactions (user_id, tx_type, amount, details, created_at) VALUES (?, ?, ?, ?, ?)',
            (user_id, 'daily_bonus', bonus, f'Daily bonus (VIP: {vip["name"]})', now)
        )
        conn.commit()
        return bonus


VIP_LEVELS = [
    {"name": "Bronze", "min_wagered": 0, "cashback": 0, "daily_bonus": 50, "emoji": "\U0001f949"},
    {"name": "Silver", "min_wagered": 5000, "cashback": 1, "daily_bonus": 75, "emoji": "\U0001f948"},
    {"name": "Gold", "min_wagered": 25000, "cashback": 2, "daily_bonus": 100, "emoji": "\U0001f947"},
    {"name": "Platinum", "min_wagered": 100000, "cashback": 3, "daily_bonus": 150, "emoji": "\U0001f48e"},
    {"name": "Diamond", "min_wagered": 500000, "cashback": 5, "daily_bonus": 250, "emoji": "\U0001f451"},
]


def get_vip_level_by_wagered(total_wagered):
    level = VIP_LEVELS[0]
    for vl in VIP_LEVELS:
        if total_wagered >= vl['min_wagered']:
            level = vl
    return level


def get_vip_level(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT total_wagered FROM users WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        wagered = row['total_wagered'] if row else 0
        return get_vip_level_by_wagered(wagered or 0)


def apply_cashback(user_id, bet_amount, lost_amount):
    vip = get_vip_level(user_id)
    if vip['cashback'] <= 0:
        return 0
    cashback = int(lost_amount * vip['cashback'] / 100)
    if cashback > 0:
        now = int(time.time())
        with get_db() as conn:
            c = conn.cursor()
            c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (cashback, user_id))
            c.execute(
                'INSERT INTO transactions (user_id, tx_type, amount, details, created_at) VALUES (?, ?, ?, ?, ?)',
                (user_id, 'cashback', cashback, f'VIP {vip["name"]} cashback', now)
            )
            conn.commit()
    return cashback


def get_referral_count(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as cnt FROM users WHERE referrer_id = ?', (user_id,))
        return c.fetchone()['cnt']


def get_referral_earnings_total(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT COALESCE(SUM(amount), 0) as total FROM referral_earnings WHERE referrer_id = ?', (user_id,))
        return c.fetchone()['total']


def get_leaderboard(period='daily', limit=10):
    now = int(time.time())
    if period == 'daily':
        since = now - 86400
    elif period == 'weekly':
        since = now - 604800
    else:
        since = now - 2592000

    with get_db() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT g.user_id, u.username,
                   SUM(g.payout) - SUM(g.bet_amount) as net_profit,
                   COUNT(*) as games_played
            FROM game_history g
            JOIN users u ON g.user_id = u.user_id
            WHERE g.created_at >= ?
            GROUP BY g.user_id
            ORDER BY net_profit DESC
            LIMIT ?
        ''', (since, limit))
        return c.fetchall()


def get_user_stats(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        if not user:
            return None

        c.execute(
            'SELECT COUNT(*) as total_games FROM game_history WHERE user_id = ?',
            (user_id,)
        )
        total_games = c.fetchone()['total_games']

        c.execute(
            'SELECT COUNT(*) as wins FROM game_history WHERE user_id = ? AND payout > 0',
            (user_id,)
        )
        wins = c.fetchone()['wins']

        c.execute(
            'SELECT game_type, COUNT(*) as cnt FROM game_history WHERE user_id = ? GROUP BY game_type',
            (user_id,)
        )
        by_game = {row['game_type']: row['cnt'] for row in c.fetchall()}

        return {
            'user': user,
            'total_games': total_games,
            'wins': wins,
            'by_game': by_game
        }


def get_total_users():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as cnt FROM users')
        return c.fetchone()['cnt']


def get_admin_stats():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) as cnt FROM users')
        total_users = c.fetchone()['cnt']

        c.execute('SELECT COALESCE(SUM(total_deposited), 0) as s FROM users')
        total_deposited = c.fetchone()['s']

        c.execute('SELECT COALESCE(SUM(total_withdrawn), 0) as s FROM users')
        total_withdrawn = c.fetchone()['s']

        c.execute('SELECT COALESCE(SUM(balance), 0) as s FROM users')
        total_balance = c.fetchone()['s']

        c.execute('SELECT COUNT(*) as cnt FROM game_history')
        total_games = c.fetchone()['cnt']

        c.execute('SELECT COALESCE(SUM(bet_amount), 0) as s FROM game_history')
        total_wagered = c.fetchone()['s']

        c.execute('SELECT COALESCE(SUM(payout), 0) as s FROM game_history')
        total_payouts = c.fetchone()['s']

        now = int(time.time())
        day_ago = now - 86400
        c.execute('SELECT COUNT(*) as cnt FROM users WHERE last_active >= ?', (day_ago,))
        active_today = c.fetchone()['cnt']

        c.execute(
            'SELECT COALESCE(SUM(total_deposited), 0) as s FROM users WHERE created_at >= ?',
            (day_ago,)
        )
        deposits_today = c.fetchone()['s']

        return {
            'total_users': total_users,
            'total_deposited': total_deposited,
            'total_withdrawn': total_withdrawn,
            'total_balance': total_balance,
            'total_games': total_games,
            'total_wagered': total_wagered,
            'total_payouts': total_payouts,
            'house_profit': total_wagered - total_payouts,
            'active_today': active_today,
            'deposits_today': deposits_today,
        }


def ban_user(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            'INSERT OR IGNORE INTO banned_users (user_id, banned_at) VALUES (?, ?)',
            (user_id, int(time.time()))
        )
        conn.commit()


def unban_user(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM banned_users WHERE user_id = ?', (user_id,))
        conn.commit()


def is_banned(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM banned_users WHERE user_id = ?', (user_id,))
        return c.fetchone() is not None


def get_all_user_ids():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('SELECT user_id FROM users')
        return [row['user_id'] for row in c.fetchall()]


def escape_html(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
