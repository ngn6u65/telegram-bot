import random
import math

# ============================================================
# SLOTS
# ============================================================

SLOT_SYMBOLS = [
    {"emoji": "\U0001f352", "name": "Cherry", "weight": 30},
    {"emoji": "\U0001f34b", "name": "Lemon", "weight": 25},
    {"emoji": "\U0001f34a", "name": "Orange", "weight": 20},
    {"emoji": "\U0001f347", "name": "Grape", "weight": 18},
    {"emoji": "\U0001f349", "name": "Watermelon", "weight": 14},
    {"emoji": "\U0001f514", "name": "Bell", "weight": 10},
    {"emoji": "\U0001f4a0", "name": "Bar", "weight": 6},
    {"emoji": "7\ufe0f\u20e3", "name": "Seven", "weight": 3},
    {"emoji": "\U0001f48e", "name": "Diamond", "weight": 1},
]

SLOT_PAYOUTS = {
    "Diamond": 50,
    "Seven": 20,
    "Bar": 15,
    "Bell": 10,
    "Watermelon": 8,
    "Grape": 5,
    "Orange": 4,
    "Lemon": 3,
    "Cherry": 2,
}


def _weighted_spin():
    total = sum(s['weight'] for s in SLOT_SYMBOLS)
    r = random.randint(1, total)
    cumulative = 0
    for s in SLOT_SYMBOLS:
        cumulative += s['weight']
        if r <= cumulative:
            return s
    return SLOT_SYMBOLS[0]


def play_slots(bet):
    reels = [_weighted_spin() for _ in range(3)]
    names = [r['name'] for r in reels]
    emojis = [r['emoji'] for r in reels]

    if names[0] == names[1] == names[2]:
        multiplier = SLOT_PAYOUTS.get(names[0], 2)
    elif names[0] == names[1] or names[1] == names[2] or names[0] == names[2]:
        multiplier = 1.5
    else:
        multiplier = 0

    payout = int(bet * multiplier)
    return {
        'reels': reels,
        'emojis': emojis,
        'multiplier': multiplier,
        'payout': payout,
        'won': payout > 0,
    }


# ============================================================
# MINES
# ============================================================

MINES_GRID_SIZE = 25
MINES_HOUSE_EDGE = 0.03


def create_mines_game(num_mines):
    positions = list(range(MINES_GRID_SIZE))
    mine_positions = set(random.sample(positions, num_mines))
    return {
        'mines': mine_positions,
        'num_mines': num_mines,
        'revealed': set(),
        'alive': True,
        'cashed_out': False,
    }


def calculate_mines_multiplier(num_mines, num_revealed):
    if num_revealed == 0:
        return 1.0
    safe_total = MINES_GRID_SIZE - num_mines
    prob = 1.0
    for i in range(num_revealed):
        prob *= (safe_total - i) / (MINES_GRID_SIZE - i)
    if prob <= 0:
        return 1.0
    fair = 1.0 / prob
    return round(fair * (1 - MINES_HOUSE_EDGE), 2)


def reveal_mine_cell(game, cell_index):
    if cell_index in game['revealed']:
        return None
    if not game['alive']:
        return None

    is_mine = cell_index in game['mines']
    if is_mine:
        game['alive'] = False
        return {
            'is_mine': True,
            'multiplier': 0,
            'game_over': True,
        }

    game['revealed'].add(cell_index)
    num_revealed = len(game['revealed'])
    multiplier = calculate_mines_multiplier(game['num_mines'], num_revealed)
    safe_remaining = (MINES_GRID_SIZE - game['num_mines']) - num_revealed

    return {
        'is_mine': False,
        'multiplier': multiplier,
        'game_over': safe_remaining == 0,
        'safe_remaining': safe_remaining,
    }


# ============================================================
# DICE
# ============================================================

DICE_HOUSE_EDGE = 0.03


def play_dice(bet, target, direction):
    roll = round(random.uniform(0.01, 100.0), 2)

    if direction == 'over':
        win_chance = (100.0 - target) / 100.0
        won = roll > target
    else:
        win_chance = target / 100.0
        won = roll < target

    if win_chance <= 0 or win_chance >= 1:
        return {'roll': roll, 'won': False, 'multiplier': 0, 'payout': 0}

    multiplier = round((1.0 / win_chance) * (1 - DICE_HOUSE_EDGE), 2)
    payout = int(bet * multiplier) if won else 0

    return {
        'roll': roll,
        'won': won,
        'multiplier': multiplier,
        'payout': payout,
        'win_chance': round(win_chance * 100, 1),
    }


# ============================================================
# COIN FLIP
# ============================================================

COINFLIP_MULTIPLIER = 1.95


def play_coinflip(bet, choice):
    result = random.choice(['heads', 'tails'])
    won = (choice == result)
    payout = int(bet * COINFLIP_MULTIPLIER) if won else 0

    return {
        'result': result,
        'won': won,
        'multiplier': COINFLIP_MULTIPLIER if won else 0,
        'payout': payout,
    }


# ============================================================
# WHEEL OF FORTUNE
# ============================================================

WHEEL_SEGMENTS = [
    {"color": "\u26ab", "name": "Lose", "multiplier": 0, "weight": 678},
    {"color": "\U0001f534", "name": "Red", "multiplier": 2, "weight": 200},
    {"color": "\U0001f535", "name": "Blue", "multiplier": 3, "weight": 80},
    {"color": "\U0001f7e2", "name": "Green", "multiplier": 5, "weight": 30},
    {"color": "\U0001f7e1", "name": "Gold", "multiplier": 50, "weight": 2},
    {"color": "\U0001f7e3", "name": "Purple", "multiplier": 10, "weight": 10},
]


def spin_wheel(bet):
    total_weight = sum(s['weight'] for s in WHEEL_SEGMENTS)
    r = random.randint(1, total_weight)
    cumulative = 0
    segment = WHEEL_SEGMENTS[0]
    for s in WHEEL_SEGMENTS:
        cumulative += s['weight']
        if r <= cumulative:
            segment = s
            break

    payout = int(bet * segment['multiplier'])
    return {
        'segment': segment,
        'multiplier': segment['multiplier'],
        'payout': payout,
        'won': payout > 0,
    }


# ============================================================
# CRASH
# ============================================================

CRASH_HOUSE_EDGE = 0.04


def generate_crash_point():
    r = random.random()
    if r < CRASH_HOUSE_EDGE:
        return 1.00
    crash = (1 - CRASH_HOUSE_EDGE) / (1 - r)
    return round(max(1.00, crash), 2)


def check_crash_cashout(crash_point, cashout_at):
    if cashout_at <= crash_point:
        return True
    return False


CRASH_STEPS = [1.10, 1.20, 1.30, 1.50, 1.70, 2.00, 2.50, 3.00, 4.00, 5.00,
               7.00, 10.00, 15.00, 20.00, 30.00, 50.00, 100.00]
