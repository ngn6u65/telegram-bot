STRINGS = {
    "en": {
        "welcome": (
            "\U0001f3b0 <b>Welcome to the Casino!</b> \U0001f3b0\n\n"
            "\U0001f4b0 Your Balance: <b>{balance} coins</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae Play exciting games, win big, and climb the leaderboard!\n"
            "\u2b50 Buy coins with Telegram Stars\n"
            "\U0001f91d Invite friends & earn bonuses!"
        ),
        "main_menu": "\U0001f3b0 Main Menu",
        "games_menu": "\U0001f3ae Games",
        "slots": "\U0001f3b0 Slots",
        "mines": "\U0001f4a3 Mines",
        "dice": "\U0001f3b2 Dice",
        "coinflip": "\U0001fa99 Coin Flip",
        "wheel": "\U0001f3a1 Wheel",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 Buy Coins",
        "withdraw": "\U0001f4b8 Withdraw",
        "referral": "\U0001f91d Referrals",
        "stats": "\U0001f4ca My Stats",
        "leaderboard": "\U0001f3c6 Leaderboard",
        "daily_bonus": "\U0001f381 Daily Bonus",
        "vip_info": "\U0001f451 VIP Info",
        "settings": "\u2699\ufe0f Settings",
        "language": "\U0001f310 Language",
        "back": "\u25c0\ufe0f Back",
        "balance": "\U0001f4b0 Balance: <b>{balance} coins</b>",
        "balance_short": "\U0001f4b0 {balance} coins",
        "insufficient_balance": "\u274c Not enough coins! You need <b>{needed}</b> but have <b>{balance}</b>.",
        "select_bet": "\U0001f4b0 Select your bet amount:",
        "custom_bet": "\u270d\ufe0f Custom Bet",
        "enter_custom_bet": "Enter your bet amount (min: {min}, max: {max}):",
        "invalid_bet": "\u274c Invalid bet amount. Please try again.",
        "game_won": "\U0001f389 <b>YOU WON!</b>\n\n\U0001f4b0 Bet: {bet} coins\n\u2716\ufe0f Multiplier: x{multiplier}\n\U0001f3c6 Payout: <b>{payout} coins</b>",
        "game_lost": "\U0001f61e <b>You Lost!</b>\n\n\U0001f4b0 Bet: {bet} coins\n\U0001f4b8 Lost: {bet} coins",
        "cashback_applied": "\U0001f4ab VIP Cashback: +{amount} coins returned!",
        "play_again": "\U0001f504 Play Again",
        "double_bet": "\u23eb Double Bet",
        # Slots
        "slots_title": "\U0001f3b0 <b>SLOT MACHINE</b> \U0001f3b0",
        "slots_spinning": "\U0001f3b0 Spinning...\n\n\u2753 | \u2753 | \u2753",
        "slots_result": "\U0001f3b0 <b>SLOTS</b>\n\n{r1} | {r2} | {r3}\n\n{result}",
        "slots_paytable": (
            "\U0001f3b0 <b>Slots Paytable</b>\n\n"
            "\U0001f48e\U0001f48e\U0001f48e = x50\n"
            "7\ufe0f\u20e37\ufe0f\u20e37\ufe0f\u20e3 = x20\n"
            "\U0001f4a0\U0001f4a0\U0001f4a0 = x15\n"
            "\U0001f514\U0001f514\U0001f514 = x10\n"
            "\U0001f349\U0001f349\U0001f349 = x8\n"
            "\U0001f347\U0001f347\U0001f347 = x5\n"
            "\U0001f34a\U0001f34a\U0001f34a = x4\n"
            "\U0001f34b\U0001f34b\U0001f34b = x3\n"
            "\U0001f352\U0001f352\U0001f352 = x2\n"
            "2 matching = x1.5"
        ),
        # Mines
        "mines_title": "\U0001f4a3 <b>MINES</b>",
        "mines_select_count": "\U0001f4a3 How many mines? (1-24)\nMore mines = higher reward!",
        "mines_grid_header": "\U0001f4a3 <b>MINES</b> | Mines: {mines}\n\U0001f4b0 Bet: {bet} | Multiplier: <b>x{mult}</b>\n\U0001f48e Potential win: <b>{potential} coins</b>",
        "mines_safe": "\U0001f48e",
        "mines_bomb": "\U0001f4a5",
        "mines_hidden": "\u2b1c",
        "mines_cashout": "\U0001f4b0 Cash Out (x{mult})",
        "mines_hit": "\U0001f4a5 <b>BOOM!</b> You hit a mine!\n\n\U0001f4b0 Bet: {bet} coins\n\U0001f4b8 Lost: {bet} coins",
        "mines_won": "\U0001f48e <b>CASHED OUT!</b>\n\n\U0001f4b0 Bet: {bet} coins\n\u2716\ufe0f Multiplier: x{mult}\n\U0001f3c6 Won: <b>{payout} coins</b>",
        # Dice
        "dice_title": "\U0001f3b2 <b>DICE</b>",
        "dice_select": "Select prediction:",
        "dice_over": "\u2b06\ufe0f Over {target}",
        "dice_under": "\u2b07\ufe0f Under {target}",
        "dice_result": "\U0001f3b2 <b>DICE</b>\n\n\U0001f3af Roll: <b>{roll}</b>\n\U0001f4cd Target: {direction} {target}\n\U0001f4ca Win Chance: {chance}%\n\n{result}",
        "dice_select_target": "\U0001f3b2 Choose your target number:\n\nPick a number - roll {direction} to win!",
        # Coinflip
        "coinflip_title": "\U0001fa99 <b>COIN FLIP</b>",
        "coinflip_select": "\U0001fa99 Pick your side!\n\nMultiplier: <b>x1.95</b>",
        "heads": "\U0001f535 Heads",
        "tails": "\U0001f534 Tails",
        "coinflip_result": "\U0001fa99 <b>COIN FLIP</b>\n\n\U0001fa99 Result: <b>{result}</b>\n\n{outcome}",
        # Wheel
        "wheel_title": "\U0001f3a1 <b>WHEEL OF FORTUNE</b>",
        "wheel_spin": "\U0001f3a1 Spin the Wheel!",
        "wheel_segments": (
            "\U0001f3a1 <b>Wheel of Fortune</b>\n\n"
            "\U0001f534 Red = x2\n"
            "\U0001f535 Blue = x3\n"
            "\U0001f7e2 Green = x5\n"
            "\U0001f7e3 Purple = x10\n"
            "\U0001f7e1 Gold = x50\n"
            "\u26ab Lose = x0\n\n"
            "\U0001f4b0 Place your bet!"
        ),
        "wheel_result": "\U0001f3a1 <b>WHEEL</b>\n\n{color} Landed on: <b>{name}</b> (x{mult})\n\n{result}",
        # Crash
        "crash_title": "\U0001f4c8 <b>CRASH</b>",
        "crash_select_target": "\U0001f4c8 <b>CRASH</b>\n\nChoose your cashout target:\nHigher target = bigger risk & reward!\n\n\U0001f4b0 Bet: {bet} coins",
        "crash_result_win": "\U0001f4c8 <b>CRASH</b>\n\n\U0001f680 Crashed at: <b>x{crash}</b>\n\U0001f3af Your target: <b>x{target}</b>\n\n\U0001f389 <b>CASHED OUT before crash!</b>\n\U0001f4b0 Won: <b>{payout} coins</b>",
        "crash_result_lose": "\U0001f4c8 <b>CRASH</b>\n\n\U0001f4a5 Crashed at: <b>x{crash}</b>\n\U0001f3af Your target: <b>x{target}</b>\n\n\U0001f61e <b>Crashed before cashout!</b>\n\U0001f4b8 Lost: {bet} coins",
        # Economy
        "buy_title": (
            "\u2b50 <b>Buy Coins with Stars</b> \u2b50\n\n"
            "\U0001f4b0 Current balance: <b>{balance} coins</b>\n\n"
            "Select a package:"
        ),
        "buy_50": "\u2b50 50 Stars \u27a1 500 Coins",
        "buy_100": "\u2b50 100 Stars \u27a1 1,100 Coins (+10%)",
        "buy_250": "\u2b50 250 Stars \u27a1 3,000 Coins (+20%)",
        "buy_500": "\u2b50 500 Stars \u27a1 6,500 Coins (+30%)",
        "purchase_success": "\U0001f389 <b>Purchase Successful!</b>\n\n\u2b50 Paid: {stars} Stars\n\U0001f4b0 Received: <b>{coins} coins</b>\n\U0001f4b0 New Balance: <b>{balance} coins</b>",
        "withdraw_title": (
            "\U0001f4b8 <b>Withdraw Coins</b>\n\n"
            "\U0001f4b0 Balance: <b>{balance} coins</b>\n"
            "\U0001f4b1 Rate: 10 coins = 1 Star\n"
            "\U0001f6d1 Minimum: 1,000 coins (100 Stars)\n\n"
            "Select amount to withdraw:"
        ),
        "withdraw_1000": "1,000 Coins \u27a1 100 \u2b50",
        "withdraw_2500": "2,500 Coins \u27a1 250 \u2b50",
        "withdraw_5000": "5,000 Coins \u27a1 500 \u2b50",
        "withdraw_10000": "10,000 Coins \u27a1 1,000 \u2b50",
        "withdraw_success": "\U0001f4b8 <b>Withdrawal Processed!</b>\n\n\U0001f4b0 Deducted: {coins} coins\n\u2b50 Sent: <b>{stars} Stars</b>\n\U0001f4b0 Remaining: <b>{balance} coins</b>",
        "withdraw_min_error": "\u274c Minimum withdrawal is 1,000 coins (100 Stars).",
        # Referral
        "referral_title": (
            "\U0001f91d <b>Referral Program</b>\n\n"
            "\U0001f465 Your Referrals: <b>{count}</b>\n"
            "\U0001f4b0 Total Earned: <b>{earnings} coins</b>\n\n"
            "\U0001f517 Your Link:\n<code>{link}</code>\n\n"
            "\U0001f4e2 <b>How it works:</b>\n"
            "\u2022 Level 1: <b>10%</b> of every deposit from your referrals\n"
            "\u2022 Level 2: <b>5%</b> of deposits from their referrals\n\n"
            "\U0001f4e3 Share your link and earn passive income!"
        ),
        "referral_share": "\U0001f4e3 Share Link",
        "referral_share_text": "\U0001f3b0 Join the best Telegram Casino!\n\n\U0001f3ae 6 exciting games\n\U0001f4b0 Win big with Telegram Stars\n\U0001f381 Get bonus coins!\n\n\U0001f447 Join now: {link}",
        "referral_bonus_received": "\U0001f4b0 <b>Referral Bonus!</b>\n\nYou earned <b>{amount} coins</b> from a referral deposit!",
        # Stats
        "stats_title": (
            "\U0001f4ca <b>Your Statistics</b>\n\n"
            "\U0001f4b0 Balance: <b>{balance} coins</b>\n"
            "\U0001f451 VIP Level: <b>{vip}</b>\n"
            "\U0001f4b5 Total Deposited: <b>{deposited} coins</b>\n"
            "\U0001f4b8 Total Withdrawn: <b>{withdrawn} coins</b>\n"
            "\U0001f3b2 Total Wagered: <b>{wagered} coins</b>\n"
            "\U0001f3c6 Total Won: <b>{won} coins</b>\n"
            "\U0001f4ca Net Profit: <b>{profit} coins</b>\n"
            "\U0001f3ae Total Games: <b>{games}</b>\n"
            "\u2705 Wins: <b>{wins}</b>\n"
            "\U0001f465 Referrals: <b>{referrals}</b>"
        ),
        # Leaderboard
        "leaderboard_title": "\U0001f3c6 <b>Leaderboard</b>",
        "leaderboard_daily": "\U0001f4c5 Daily",
        "leaderboard_weekly": "\U0001f4c6 Weekly",
        "leaderboard_monthly": "\U0001f4c5 Monthly",
        "leaderboard_empty": "No players yet! Be the first to play!",
        "leaderboard_entry": "{medal} {name} \u2014 <b>{profit} coins</b>",
        # Daily Bonus
        "daily_claimed": "\U0001f381 <b>Daily Bonus Claimed!</b>\n\n\U0001f4b0 You received <b>{amount} coins</b>!\n\U0001f451 VIP Level: {vip}\n\nCome back tomorrow for more!",
        "daily_wait": "\u23f0 Daily bonus not ready!\n\nCome back in <b>{hours}h {minutes}m</b>",
        # VIP
        "vip_title": (
            "\U0001f451 <b>VIP System</b>\n\n"
            "Your Level: <b>{current}</b>\n"
            "Total Wagered: <b>{wagered} coins</b>\n\n"
            "\U0001f949 Bronze (0+): 50 daily coins\n"
            "\U0001f948 Silver (5K+): 1% cashback, 75 daily\n"
            "\U0001f947 Gold (25K+): 2% cashback, 100 daily\n"
            "\U0001f48e Platinum (100K+): 3% cashback, 150 daily\n"
            "\U0001f451 Diamond (500K+): 5% cashback, 250 daily\n\n"
            "Keep playing to level up!"
        ),
        # Admin
        "admin_panel": (
            "\U0001f6e1\ufe0f <b>Admin Panel</b>\n\n"
            "\U0001f465 Total Users: <b>{total_users}</b>\n"
            "\U0001f4b5 Total Deposited: <b>{total_deposited}</b>\n"
            "\U0001f4b8 Total Withdrawn: <b>{total_withdrawn}</b>\n"
            "\U0001f4b0 Total Balance (in play): <b>{total_balance}</b>\n"
            "\U0001f3ae Total Games: <b>{total_games}</b>\n"
            "\U0001f3b2 Total Wagered: <b>{total_wagered}</b>\n"
            "\U0001f3c6 Total Payouts: <b>{total_payouts}</b>\n"
            "\U0001f4b0 House Profit: <b>{house_profit}</b>\n"
            "\U0001f4c8 Active Today: <b>{active_today}</b>\n"
            "\U0001f4b5 Deposits Today: <b>{deposits_today}</b>"
        ),
        "admin_broadcast": "\U0001f4e2 Broadcast",
        "admin_broadcast_prompt": "Send the message you want to broadcast to all users:",
        "admin_broadcast_sent": "\u2705 Broadcast sent to {count} users!",
        "admin_ban": "\U0001f6ab Ban User",
        "admin_unban": "\u2705 Unban User",
        "admin_ban_prompt": "Send the user ID to ban:",
        "admin_unban_prompt": "Send the user ID to unban:",
        "admin_banned": "\U0001f6ab User {user_id} has been banned.",
        "admin_unbanned": "\u2705 User {user_id} has been unbanned.",
        "banned_message": "\U0001f6ab You are banned from this bot.",
        "select_language": "\U0001f310 Select your language:",
    },
    "ru": {
        "welcome": (
            "\U0001f3b0 <b>\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c \u0432 \u041a\u0430\u0437\u0438\u043d\u043e!</b> \U0001f3b0\n\n"
            "\U0001f4b0 \u0411\u0430\u043b\u0430\u043d\u0441: <b>{balance} \u043c\u043e\u043d\u0435\u0442</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae \u0418\u0433\u0440\u0430\u0439, \u0432\u044b\u0438\u0433\u0440\u044b\u0432\u0430\u0439 \u0438 \u043f\u043e\u0434\u043d\u0438\u043c\u0430\u0439\u0441\u044f \u0432 \u0440\u0435\u0439\u0442\u0438\u043d\u0433\u0435!"
        ),
        "main_menu": "\U0001f3b0 \u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e",
        "games_menu": "\U0001f3ae \u0418\u0433\u0440\u044b",
        "slots": "\U0001f3b0 \u0421\u043b\u043e\u0442\u044b",
        "mines": "\U0001f4a3 \u041c\u0438\u043d\u044b",
        "dice": "\U0001f3b2 \u041a\u043e\u0441\u0442\u0438",
        "coinflip": "\U0001fa99 \u041c\u043e\u043d\u0435\u0442\u043a\u0430",
        "wheel": "\U0001f3a1 \u041a\u043e\u043b\u0435\u0441\u043e",
        "crash": "\U0001f4c8 \u041a\u0440\u044d\u0448",
        "buy_coins": "\u2b50 \u041a\u0443\u043f\u0438\u0442\u044c \u043c\u043e\u043d\u0435\u0442\u044b",
        "withdraw": "\U0001f4b8 \u0412\u044b\u0432\u0435\u0441\u0442\u0438",
        "referral": "\U0001f91d \u0420\u0435\u0444\u0435\u0440\u0430\u043b\u044b",
        "stats": "\U0001f4ca \u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430",
        "leaderboard": "\U0001f3c6 \u0420\u0435\u0439\u0442\u0438\u043d\u0433",
        "daily_bonus": "\U0001f381 \u0415\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u044b\u0439 \u0431\u043e\u043d\u0443\u0441",
        "vip_info": "\U0001f451 VIP \u0438\u043d\u0444\u043e",
        "settings": "\u2699\ufe0f \u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
        "language": "\U0001f310 \u042f\u0437\u044b\u043a",
        "back": "\u25c0\ufe0f \u041d\u0430\u0437\u0430\u0434",
        "balance": "\U0001f4b0 \u0411\u0430\u043b\u0430\u043d\u0441: <b>{balance} \u043c\u043e\u043d\u0435\u0442</b>",
        "balance_short": "\U0001f4b0 {balance} \u043c\u043e\u043d\u0435\u0442",
        "insufficient_balance": "\u274c \u041d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u043c\u043e\u043d\u0435\u0442! \u041d\u0443\u0436\u043d\u043e <b>{needed}</b>, \u0435\u0441\u0442\u044c <b>{balance}</b>.",
        "select_bet": "\U0001f4b0 \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0441\u0442\u0430\u0432\u043a\u0443:",
        "game_won": "\U0001f389 <b>\u0412\u042b \u0412\u042b\u0418\u0413\u0420\u0410\u041b\u0418!</b>\n\n\U0001f4b0 \u0421\u0442\u0430\u0432\u043a\u0430: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 \u0412\u044b\u0438\u0433\u0440\u044b\u0448: <b>{payout} \u043c\u043e\u043d\u0435\u0442</b>",
        "game_lost": "\U0001f61e <b>\u041f\u0440\u043e\u0438\u0433\u0440\u044b\u0448!</b>\n\n\U0001f4b0 \u0421\u0442\u0430\u0432\u043a\u0430: {bet}\n\U0001f4b8 \u041f\u043e\u0442\u0435\u0440\u044f: {bet}",
        "cashback_applied": "\U0001f4ab VIP \u041a\u044d\u0448\u0431\u044d\u043a: +{amount} \u043c\u043e\u043d\u0435\u0442!",
        "play_again": "\U0001f504 \u0418\u0433\u0440\u0430\u0442\u044c \u0441\u043d\u043e\u0432\u0430",
        "double_bet": "\u23eb \u0423\u0434\u0432\u043e\u0438\u0442\u044c",
        "slots_title": "\U0001f3b0 <b>\u0421\u041b\u041e\u0422\u042b</b> \U0001f3b0",
        "slots_result": "\U0001f3b0 <b>\u0421\u041b\u041e\u0422\u042b</b>\n\n{r1} | {r2} | {r3}\n\n{result}",
        "mines_title": "\U0001f4a3 <b>\u041c\u0418\u041d\u042b</b>",
        "mines_select_count": "\U0001f4a3 \u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043c\u0438\u043d? (1-24)\n\u0411\u043e\u043b\u044c\u0448\u0435 \u043c\u0438\u043d = \u0431\u043e\u043b\u044c\u0448\u0435 \u043d\u0430\u0433\u0440\u0430\u0434\u0430!",
        "mines_grid_header": "\U0001f4a3 <b>\u041c\u0418\u041d\u042b</b> | \u041c\u0438\u043d: {mines}\n\U0001f4b0 \u0421\u0442\u0430\u0432\u043a\u0430: {bet} | x<b>{mult}</b>\n\U0001f48e \u0412\u043e\u0437\u043c\u043e\u0436\u043d\u044b\u0439 \u0432\u044b\u0438\u0433\u0440\u044b\u0448: <b>{potential}</b>",
        "mines_cashout": "\U0001f4b0 \u0417\u0430\u0431\u0440\u0430\u0442\u044c (x{mult})",
        "mines_hit": "\U0001f4a5 <b>\u0411\u0423\u041c!</b> \u0412\u044b \u043d\u0430\u0441\u0442\u0443\u043f\u0438\u043b\u0438 \u043d\u0430 \u043c\u0438\u043d\u0443!\n\n\U0001f4b8 \u041f\u043e\u0442\u0435\u0440\u044f: {bet}",
        "mines_won": "\U0001f48e <b>\u0417\u0410\u0411\u0420\u0410\u041b\u0418!</b>\n\n\u2716\ufe0f x{mult}\n\U0001f3c6 \u0412\u044b\u0438\u0433\u0440\u044b\u0448: <b>{payout}</b>",
        "dice_title": "\U0001f3b2 <b>\u041a\u041e\u0421\u0422\u0418</b>",
        "dice_over": "\u2b06\ufe0f \u0411\u043e\u043b\u044c\u0448\u0435 {target}",
        "dice_under": "\u2b07\ufe0f \u041c\u0435\u043d\u044c\u0448\u0435 {target}",
        "dice_result": "\U0001f3b2 <b>\u041a\u041e\u0421\u0422\u0418</b>\n\n\U0001f3af \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442: <b>{roll}</b>\n\U0001f4cd \u0426\u0435\u043b\u044c: {direction} {target}\n\n{result}",
        "coinflip_title": "\U0001fa99 <b>\u041c\u041e\u041d\u0415\u0422\u041a\u0410</b>",
        "coinflip_select": "\U0001fa99 \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0441\u0442\u043e\u0440\u043e\u043d\u0443!\n\nx1.95",
        "heads": "\U0001f535 \u041e\u0440\u0451\u043b",
        "tails": "\U0001f534 \u0420\u0435\u0448\u043a\u0430",
        "coinflip_result": "\U0001fa99 <b>\u041c\u041e\u041d\u0415\u0422\u041a\u0410</b>\n\n\U0001fa99 \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442: <b>{result}</b>\n\n{outcome}",
        "wheel_title": "\U0001f3a1 <b>\u041a\u041e\u041b\u0415\u0421\u041e \u0423\u0414\u0410\u0427\u0418</b>",
        "wheel_result": "\U0001f3a1 <b>\u041a\u041e\u041b\u0415\u0421\u041e</b>\n\n{color} <b>{name}</b> (x{mult})\n\n{result}",
        "crash_title": "\U0001f4c8 <b>\u041a\u0420\u042d\u0428</b>",
        "crash_select_target": "\U0001f4c8 <b>\u041a\u0420\u042d\u0428</b>\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0446\u0435\u043b\u044c:\n\n\U0001f4b0 \u0421\u0442\u0430\u0432\u043a\u0430: {bet}",
        "crash_result_win": "\U0001f4c8 <b>\u041a\u0420\u042d\u0428</b>\n\n\U0001f680 \u041a\u0440\u044d\u0448 \u043d\u0430: <b>x{crash}</b>\n\U0001f3af \u0426\u0435\u043b\u044c: <b>x{target}</b>\n\n\U0001f389 <b>\u0423\u0421\u041f\u0415\u041b\u0418!</b>\n\U0001f4b0 \u0412\u044b\u0438\u0433\u0440\u044b\u0448: <b>{payout}</b>",
        "crash_result_lose": "\U0001f4c8 <b>\u041a\u0420\u042d\u0428</b>\n\n\U0001f4a5 \u041a\u0440\u044d\u0448 \u043d\u0430: <b>x{crash}</b>\n\U0001f3af \u0426\u0435\u043b\u044c: <b>x{target}</b>\n\n\U0001f61e <b>\u041d\u0435 \u0443\u0441\u043f\u0435\u043b\u0438!</b>\n\U0001f4b8 \u041f\u043e\u0442\u0435\u0440\u044f: {bet}",
        "buy_title": "\u2b50 <b>\u041a\u0443\u043f\u0438\u0442\u044c \u043c\u043e\u043d\u0435\u0442\u044b</b>\n\n\U0001f4b0 \u0411\u0430\u043b\u0430\u043d\u0441: <b>{balance}</b>\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0430\u043a\u0435\u0442:",
        "purchase_success": "\U0001f389 <b>\u041f\u043e\u043a\u0443\u043f\u043a\u0430 \u0443\u0441\u043f\u0435\u0448\u043d\u0430!</b>\n\n\u2b50 \u041e\u043f\u043b\u0430\u0442\u0430: {stars}\n\U0001f4b0 \u041f\u043e\u043b\u0443\u0447\u0435\u043d\u043e: <b>{coins}</b>\n\U0001f4b0 \u0411\u0430\u043b\u0430\u043d\u0441: <b>{balance}</b>",
        "withdraw_title": "\U0001f4b8 <b>\u0412\u044b\u0432\u0435\u0441\u0442\u0438</b>\n\n\U0001f4b0 \u0411\u0430\u043b\u0430\u043d\u0441: <b>{balance}</b>\n\U0001f4b1 \u041a\u0443\u0440\u0441: 10 \u043c\u043e\u043d\u0435\u0442 = 1 \u0417\u0432\u0435\u0437\u0434\u0430\n\U0001f6d1 \u041c\u0438\u043d\u0438\u043c\u0443\u043c: 1,000 \u043c\u043e\u043d\u0435\u0442",
        "withdraw_success": "\U0001f4b8 <b>\u0412\u044b\u0432\u043e\u0434 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d!</b>\n\n\U0001f4b0 \u0421\u043f\u0438\u0441\u0430\u043d\u043e: {coins}\n\u2b50 \u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e: <b>{stars} \u0417\u0432\u0435\u0437\u0434</b>",
        "referral_title": "\U0001f91d <b>\u0420\u0435\u0444\u0435\u0440\u0430\u043b\u044c\u043d\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430</b>\n\n\U0001f465 \u0420\u0435\u0444\u0435\u0440\u0430\u043b\u044b: <b>{count}</b>\n\U0001f4b0 \u0417\u0430\u0440\u0430\u0431\u043e\u0442\u0430\u043d\u043e: <b>{earnings}</b>\n\n\U0001f517 \u0421\u0441\u044b\u043b\u043a\u0430:\n<code>{link}</code>\n\n\u2022 \u0423\u0440\u043e\u0432\u0435\u043d\u044c 1: <b>10%</b> \u043e\u0442 \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0432\n\u2022 \u0423\u0440\u043e\u0432\u0435\u043d\u044c 2: <b>5%</b> \u043e\u0442 \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0432 \u0438\u0445 \u0440\u0435\u0444\u0435\u0440\u0430\u043b\u043e\u0432",
        "referral_share": "\U0001f4e3 \u041f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f",
        "stats_title": "\U0001f4ca <b>\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430</b>\n\n\U0001f4b0 \u0411\u0430\u043b\u0430\u043d\u0441: <b>{balance}</b>\n\U0001f451 VIP: <b>{vip}</b>\n\U0001f3b2 \u0421\u0442\u0430\u0432\u043a\u0438: <b>{wagered}</b>\n\U0001f3c6 \u0412\u044b\u0438\u0433\u0440\u044b\u0448\u0438: <b>{won}</b>\n\U0001f3ae \u0418\u0433\u0440: <b>{games}</b>\n\u2705 \u041f\u043e\u0431\u0435\u0434: <b>{wins}</b>",
        "leaderboard_title": "\U0001f3c6 <b>\u0420\u0435\u0439\u0442\u0438\u043d\u0433</b>",
        "leaderboard_empty": "\u041f\u043e\u043a\u0430 \u043d\u0438\u043a\u043e\u0433\u043e! \u0411\u0443\u0434\u044c\u0442\u0435 \u043f\u0435\u0440\u0432\u044b\u043c!",
        "daily_claimed": "\U0001f381 <b>\u0411\u043e\u043d\u0443\u0441 \u043f\u043e\u043b\u0443\u0447\u0435\u043d!</b>\n\n\U0001f4b0 +<b>{amount}</b> \u043c\u043e\u043d\u0435\u0442\n\U0001f451 VIP: {vip}",
        "daily_wait": "\u23f0 \u0411\u043e\u043d\u0443\u0441 \u043d\u0435 \u0433\u043e\u0442\u043e\u0432!\n\n\u0412\u043e\u0437\u0432\u0440\u0430\u0449\u0430\u0439\u0442\u0435\u0441\u044c \u0447\u0435\u0440\u0435\u0437 <b>{hours}\u0447 {minutes}\u043c</b>",
        "select_language": "\U0001f310 \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u044f\u0437\u044b\u043a:",
        "banned_message": "\U0001f6ab \u0412\u044b \u0437\u0430\u0431\u0430\u043d\u0435\u043d\u044b.",
        "insufficient_balance": "\u274c \u041d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u043c\u043e\u043d\u0435\u0442!",
    },
    "es": {
        "welcome": (
            "\U0001f3b0 <b>\u00a1Bienvenido al Casino!</b> \U0001f3b0\n\n"
            "\U0001f4b0 Saldo: <b>{balance} monedas</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae \u00a1Juega, gana y sube en el ranking!"
        ),
        "main_menu": "\U0001f3b0 Men\u00fa Principal",
        "games_menu": "\U0001f3ae Juegos",
        "slots": "\U0001f3b0 Tragamonedas",
        "mines": "\U0001f4a3 Minas",
        "dice": "\U0001f3b2 Dados",
        "coinflip": "\U0001fa99 Moneda",
        "wheel": "\U0001f3a1 Ruleta",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 Comprar Monedas",
        "withdraw": "\U0001f4b8 Retirar",
        "referral": "\U0001f91d Referidos",
        "stats": "\U0001f4ca Estad\u00edsticas",
        "leaderboard": "\U0001f3c6 Ranking",
        "daily_bonus": "\U0001f381 Bono Diario",
        "vip_info": "\U0001f451 Info VIP",
        "settings": "\u2699\ufe0f Ajustes",
        "language": "\U0001f310 Idioma",
        "back": "\u25c0\ufe0f Volver",
        "balance": "\U0001f4b0 Saldo: <b>{balance} monedas</b>",
        "balance_short": "\U0001f4b0 {balance} monedas",
        "insufficient_balance": "\u274c \u00a1Saldo insuficiente!",
        "select_bet": "\U0001f4b0 Elige tu apuesta:",
        "game_won": "\U0001f389 <b>\u00a1GANASTE!</b>\n\n\U0001f4b0 Apuesta: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 Premio: <b>{payout} monedas</b>",
        "game_lost": "\U0001f61e <b>\u00a1Perdiste!</b>\n\n\U0001f4b0 Apuesta: {bet}\n\U0001f4b8 P\u00e9rdida: {bet}",
        "play_again": "\U0001f504 Jugar de Nuevo",
        "double_bet": "\u23eb Doblar",
        "heads": "\U0001f535 Cara",
        "tails": "\U0001f534 Cruz",
        "select_language": "\U0001f310 Elige tu idioma:",
        "banned_message": "\U0001f6ab Est\u00e1s baneado.",
        "daily_claimed": "\U0001f381 <b>\u00a1Bono recibido!</b>\n\n\U0001f4b0 +<b>{amount}</b> monedas\n\U0001f451 VIP: {vip}",
        "daily_wait": "\u23f0 \u00a1Bono no disponible!\n\nVuelve en <b>{hours}h {minutes}m</b>",
        "leaderboard_title": "\U0001f3c6 <b>Ranking</b>",
        "leaderboard_empty": "\u00a1Nadie a\u00fan! \u00a1S\u00e9 el primero!",
    },
    "fr": {
        "welcome": (
            "\U0001f3b0 <b>Bienvenue au Casino!</b> \U0001f3b0\n\n"
            "\U0001f4b0 Solde: <b>{balance} pi\u00e8ces</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae Jouez, gagnez et montez dans le classement!"
        ),
        "main_menu": "\U0001f3b0 Menu Principal",
        "games_menu": "\U0001f3ae Jeux",
        "slots": "\U0001f3b0 Machine \u00e0 sous",
        "mines": "\U0001f4a3 Mines",
        "dice": "\U0001f3b2 D\u00e9s",
        "coinflip": "\U0001fa99 Pile ou Face",
        "wheel": "\U0001f3a1 Roue",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 Acheter Pi\u00e8ces",
        "withdraw": "\U0001f4b8 Retirer",
        "referral": "\U0001f91d Parrainage",
        "stats": "\U0001f4ca Statistiques",
        "leaderboard": "\U0001f3c6 Classement",
        "daily_bonus": "\U0001f381 Bonus Quotidien",
        "vip_info": "\U0001f451 Info VIP",
        "settings": "\u2699\ufe0f Param\u00e8tres",
        "language": "\U0001f310 Langue",
        "back": "\u25c0\ufe0f Retour",
        "balance": "\U0001f4b0 Solde: <b>{balance} pi\u00e8ces</b>",
        "insufficient_balance": "\u274c Solde insuffisant!",
        "select_bet": "\U0001f4b0 Choisissez votre mise:",
        "game_won": "\U0001f389 <b>GAGN\u00c9!</b>\n\n\U0001f4b0 Mise: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 Gain: <b>{payout} pi\u00e8ces</b>",
        "game_lost": "\U0001f61e <b>Perdu!</b>\n\n\U0001f4b0 Mise: {bet}\n\U0001f4b8 Perte: {bet}",
        "play_again": "\U0001f504 Rejouer",
        "heads": "\U0001f535 Pile",
        "tails": "\U0001f534 Face",
        "select_language": "\U0001f310 Choisissez votre langue:",
        "banned_message": "\U0001f6ab Vous \u00eates banni.",
        "daily_claimed": "\U0001f381 <b>Bonus re\u00e7u!</b>\n\n\U0001f4b0 +<b>{amount}</b> pi\u00e8ces\n\U0001f451 VIP: {vip}",
        "daily_wait": "\u23f0 Bonus pas pr\u00eat!\n\nRevenez dans <b>{hours}h {minutes}m</b>",
    },
    "de": {
        "welcome": (
            "\U0001f3b0 <b>Willkommen im Casino!</b> \U0001f3b0\n\n"
            "\U0001f4b0 Guthaben: <b>{balance} M\u00fcnzen</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae Spiele, gewinne und steige im Ranking auf!"
        ),
        "main_menu": "\U0001f3b0 Hauptmen\u00fc",
        "games_menu": "\U0001f3ae Spiele",
        "slots": "\U0001f3b0 Spielautomat",
        "mines": "\U0001f4a3 Minen",
        "dice": "\U0001f3b2 W\u00fcrfel",
        "coinflip": "\U0001fa99 M\u00fcnzwurf",
        "wheel": "\U0001f3a1 Gl\u00fccksrad",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 M\u00fcnzen Kaufen",
        "withdraw": "\U0001f4b8 Abheben",
        "referral": "\U0001f91d Empfehlungen",
        "stats": "\U0001f4ca Statistiken",
        "leaderboard": "\U0001f3c6 Rangliste",
        "daily_bonus": "\U0001f381 T\u00e4glicher Bonus",
        "vip_info": "\U0001f451 VIP Info",
        "back": "\u25c0\ufe0f Zur\u00fcck",
        "balance": "\U0001f4b0 Guthaben: <b>{balance} M\u00fcnzen</b>",
        "insufficient_balance": "\u274c Nicht gen\u00fcgend M\u00fcnzen!",
        "select_bet": "\U0001f4b0 W\u00e4hle deinen Einsatz:",
        "game_won": "\U0001f389 <b>GEWONNEN!</b>\n\n\U0001f4b0 Einsatz: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 Gewinn: <b>{payout} M\u00fcnzen</b>",
        "game_lost": "\U0001f61e <b>Verloren!</b>\n\n\U0001f4b0 Einsatz: {bet}\n\U0001f4b8 Verlust: {bet}",
        "play_again": "\U0001f504 Nochmal",
        "heads": "\U0001f535 Kopf",
        "tails": "\U0001f534 Zahl",
        "select_language": "\U0001f310 Sprache w\u00e4hlen:",
        "banned_message": "\U0001f6ab Du bist gesperrt.",
        "daily_claimed": "\U0001f381 <b>Bonus erhalten!</b>\n\n\U0001f4b0 +<b>{amount}</b> M\u00fcnzen\n\U0001f451 VIP: {vip}",
        "daily_wait": "\u23f0 Bonus nicht bereit!\n\nKomm in <b>{hours}h {minutes}m</b> wieder",
    },
    "pt": {
        "welcome": (
            "\U0001f3b0 <b>Bem-vindo ao Casino!</b> \U0001f3b0\n\n"
            "\U0001f4b0 Saldo: <b>{balance} moedas</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae Jogue, ganhe e suba no ranking!"
        ),
        "main_menu": "\U0001f3b0 Menu Principal",
        "games_menu": "\U0001f3ae Jogos",
        "slots": "\U0001f3b0 Ca\u00e7a-n\u00edqueis",
        "mines": "\U0001f4a3 Minas",
        "dice": "\U0001f3b2 Dados",
        "coinflip": "\U0001fa99 Moeda",
        "wheel": "\U0001f3a1 Roleta",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 Comprar Moedas",
        "withdraw": "\U0001f4b8 Sacar",
        "referral": "\U0001f91d Indica\u00e7\u00f5es",
        "stats": "\U0001f4ca Estat\u00edsticas",
        "leaderboard": "\U0001f3c6 Ranking",
        "daily_bonus": "\U0001f381 B\u00f4nus Di\u00e1rio",
        "vip_info": "\U0001f451 Info VIP",
        "back": "\u25c0\ufe0f Voltar",
        "balance": "\U0001f4b0 Saldo: <b>{balance} moedas</b>",
        "insufficient_balance": "\u274c Saldo insuficiente!",
        "select_bet": "\U0001f4b0 Escolha sua aposta:",
        "game_won": "\U0001f389 <b>GANHOU!</b>\n\n\U0001f4b0 Aposta: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 Pr\u00eamio: <b>{payout} moedas</b>",
        "game_lost": "\U0001f61e <b>Perdeu!</b>\n\n\U0001f4b0 Aposta: {bet}\n\U0001f4b8 Perda: {bet}",
        "play_again": "\U0001f504 Jogar Novamente",
        "heads": "\U0001f535 Cara",
        "tails": "\U0001f534 Coroa",
        "select_language": "\U0001f310 Escolha seu idioma:",
        "banned_message": "\U0001f6ab Voc\u00ea est\u00e1 banido.",
        "daily_claimed": "\U0001f381 <b>B\u00f4nus recebido!</b>\n\n\U0001f4b0 +<b>{amount}</b> moedas\n\U0001f451 VIP: {vip}",
        "daily_wait": "\u23f0 B\u00f4nus n\u00e3o dispon\u00edvel!\n\nVolte em <b>{hours}h {minutes}m</b>",
    },
    "tr": {
        "welcome": (
            "\U0001f3b0 <b>Kumarhaneye Ho\u015f Geldiniz!</b> \U0001f3b0\n\n"
            "\U0001f4b0 Bakiye: <b>{balance} jeton</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae Oyna, kazan ve s\u0131ralamada y\u00fcksel!"
        ),
        "main_menu": "\U0001f3b0 Ana Men\u00fc",
        "games_menu": "\U0001f3ae Oyunlar",
        "slots": "\U0001f3b0 Slot",
        "mines": "\U0001f4a3 May\u0131nlar",
        "dice": "\U0001f3b2 Zar",
        "coinflip": "\U0001fa99 Yaz\u0131 Tura",
        "wheel": "\U0001f3a1 \u00c7ark",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 Jeton Al",
        "withdraw": "\U0001f4b8 \u00c7ek",
        "referral": "\U0001f91d Davet",
        "stats": "\U0001f4ca \u0130statistikler",
        "leaderboard": "\U0001f3c6 S\u0131ralama",
        "daily_bonus": "\U0001f381 G\u00fcnl\u00fck Bonus",
        "vip_info": "\U0001f451 VIP Bilgi",
        "back": "\u25c0\ufe0f Geri",
        "balance": "\U0001f4b0 Bakiye: <b>{balance} jeton</b>",
        "insufficient_balance": "\u274c Yetersiz bakiye!",
        "select_bet": "\U0001f4b0 Bahis miktar\u0131n\u0131 se\u00e7:",
        "game_won": "\U0001f389 <b>KAZANDIN!</b>\n\n\U0001f4b0 Bahis: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 \u00d6d\u00fcl: <b>{payout} jeton</b>",
        "game_lost": "\U0001f61e <b>Kaybettin!</b>\n\n\U0001f4b0 Bahis: {bet}\n\U0001f4b8 Kay\u0131p: {bet}",
        "play_again": "\U0001f504 Tekrar Oyna",
        "heads": "\U0001f535 Yaz\u0131",
        "tails": "\U0001f534 Tura",
        "select_language": "\U0001f310 Dil se\u00e7:",
        "banned_message": "\U0001f6ab Engellendiniz.",
        "daily_claimed": "\U0001f381 <b>Bonus al\u0131nd\u0131!</b>\n\n\U0001f4b0 +<b>{amount}</b> jeton\n\U0001f451 VIP: {vip}",
        "daily_wait": "\u23f0 Bonus haz\u0131r de\u011fil!\n\n<b>{hours}s {minutes}dk</b> sonra gel",
    },
    "hi": {
        "welcome": (
            "\U0001f3b0 <b>\u0915\u0948\u0938\u0940\u0928\u094b \u092e\u0947\u0902 \u0938\u094d\u0935\u093e\u0917\u0924 \u0939\u0948!</b> \U0001f3b0\n\n"
            "\U0001f4b0 \u092c\u0948\u0932\u0947\u0902\u0938: <b>{balance} \u0938\u093f\u0915\u094d\u0915\u0947</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae \u0916\u0947\u0932\u094b, \u091c\u0940\u0924\u094b \u0914\u0930 \u0930\u0948\u0902\u0915\u093f\u0902\u0917 \u092e\u0947\u0902 \u090a\u092a\u0930 \u091a\u0922\u093c\u094b!"
        ),
        "main_menu": "\U0001f3b0 \u092e\u0941\u0916\u094d\u092f \u092e\u0947\u0928\u0942",
        "games_menu": "\U0001f3ae \u0916\u0947\u0932",
        "slots": "\U0001f3b0 \u0938\u094d\u0932\u0949\u091f\u094d\u0938",
        "mines": "\U0001f4a3 \u092e\u093e\u0907\u0928\u094d\u0938",
        "dice": "\U0001f3b2 \u092a\u093e\u0938\u093e",
        "coinflip": "\U0001fa99 \u0938\u093f\u0915\u094d\u0915\u093e",
        "wheel": "\U0001f3a1 \u092a\u0939\u093f\u092f\u093e",
        "crash": "\U0001f4c8 \u0915\u094d\u0930\u0948\u0936",
        "buy_coins": "\u2b50 \u0938\u093f\u0915\u094d\u0915\u0947 \u0916\u0930\u0940\u0926\u0947\u0902",
        "withdraw": "\U0001f4b8 \u0928\u093f\u0915\u093e\u0932\u0947\u0902",
        "referral": "\U0001f91d \u0930\u0947\u092b\u0930\u0932",
        "stats": "\U0001f4ca \u0906\u0902\u0915\u0921\u093c\u0947",
        "leaderboard": "\U0001f3c6 \u0930\u0948\u0902\u0915\u093f\u0902\u0917",
        "daily_bonus": "\U0001f381 \u0926\u0948\u0928\u093f\u0915 \u092c\u094b\u0928\u0938",
        "back": "\u25c0\ufe0f \u0935\u093e\u092a\u0938",
        "balance": "\U0001f4b0 \u092c\u0948\u0932\u0947\u0902\u0938: <b>{balance} \u0938\u093f\u0915\u094d\u0915\u0947</b>",
        "insufficient_balance": "\u274c \u092a\u0930\u094d\u092f\u093e\u092a\u094d\u0924 \u0938\u093f\u0915\u094d\u0915\u0947 \u0928\u0939\u0940\u0902!",
        "select_bet": "\U0001f4b0 \u0905\u092a\u0928\u0940 \u0936\u0930\u094d\u0924 \u091a\u0941\u0928\u0947\u0902:",
        "game_won": "\U0001f389 <b>\u0906\u092a \u091c\u0940\u0924\u0947!</b>\n\n\U0001f4b0 \u0936\u0930\u094d\u0924: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 \u091c\u0940\u0924: <b>{payout} \u0938\u093f\u0915\u094d\u0915\u0947</b>",
        "game_lost": "\U0001f61e <b>\u0939\u093e\u0930 \u0917\u090f!</b>\n\n\U0001f4b0 \u0936\u0930\u094d\u0924: {bet}\n\U0001f4b8 \u0928\u0941\u0915\u0938\u093e\u0928: {bet}",
        "play_again": "\U0001f504 \u092b\u093f\u0930 \u0938\u0947 \u0916\u0947\u0932\u0947\u0902",
        "heads": "\U0001f535 \u091a\u093f\u0924",
        "tails": "\U0001f534 \u092a\u091f",
        "select_language": "\U0001f310 \u092d\u093e\u0937\u093e \u091a\u0941\u0928\u0947\u0902:",
        "banned_message": "\U0001f6ab \u0906\u092a \u092a\u094d\u0930\u0924\u093f\u092c\u0902\u0927\u093f\u0924 \u0939\u0948\u0902\u0964",
    },
    "zh": {
        "welcome": (
            "\U0001f3b0 <b>\u6b22\u8fce\u6765\u5230\u8d4c\u573a\uff01</b> \U0001f3b0\n\n"
            "\U0001f4b0 \u4f59\u989d: <b>{balance} \u5e01</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae \u73a9\u6e38\u620f\uff0c\u8d62\u5927\u5956\uff0c\u767b\u4e0a\u6392\u884c\u699c\uff01"
        ),
        "main_menu": "\U0001f3b0 \u4e3b\u83dc\u5355",
        "games_menu": "\U0001f3ae \u6e38\u620f",
        "slots": "\U0001f3b0 \u8001\u864e\u673a",
        "mines": "\U0001f4a3 \u626b\u96f7",
        "dice": "\U0001f3b2 \u9ab0\u5b50",
        "coinflip": "\U0001fa99 \u629b\u786c\u5e01",
        "wheel": "\U0001f3a1 \u8f6c\u76d8",
        "crash": "\U0001f4c8 Crash",
        "buy_coins": "\u2b50 \u8d2d\u4e70\u5e01",
        "withdraw": "\U0001f4b8 \u63d0\u73b0",
        "referral": "\U0001f91d \u63a8\u8350",
        "stats": "\U0001f4ca \u7edf\u8ba1",
        "leaderboard": "\U0001f3c6 \u6392\u884c\u699c",
        "daily_bonus": "\U0001f381 \u6bcf\u65e5\u5956\u52b1",
        "back": "\u25c0\ufe0f \u8fd4\u56de",
        "balance": "\U0001f4b0 \u4f59\u989d: <b>{balance} \u5e01</b>",
        "insufficient_balance": "\u274c \u4f59\u989d\u4e0d\u8db3\uff01",
        "select_bet": "\U0001f4b0 \u9009\u62e9\u4e0b\u6ce8\u91d1\u989d:",
        "game_won": "\U0001f389 <b>\u4f60\u8d62\u4e86\uff01</b>\n\n\U0001f4b0 \u4e0b\u6ce8: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 \u5956\u91d1: <b>{payout} \u5e01</b>",
        "game_lost": "\U0001f61e <b>\u4f60\u8f93\u4e86\uff01</b>\n\n\U0001f4b0 \u4e0b\u6ce8: {bet}\n\U0001f4b8 \u635f\u5931: {bet}",
        "play_again": "\U0001f504 \u518d\u6765\u4e00\u6b21",
        "heads": "\U0001f535 \u6b63\u9762",
        "tails": "\U0001f534 \u53cd\u9762",
        "select_language": "\U0001f310 \u9009\u62e9\u8bed\u8a00:",
        "banned_message": "\U0001f6ab \u4f60\u5df2\u88ab\u5c01\u7981\u3002",
    },
    "ja": {
        "welcome": (
            "\U0001f3b0 <b>\u30ab\u30b8\u30ce\u3078\u3088\u3046\u3053\u305d\uff01</b> \U0001f3b0\n\n"
            "\U0001f4b0 \u6b8b\u9ad8: <b>{balance} \u30b3\u30a4\u30f3</b>\n"
            "\U0001f451 VIP: <b>{vip}</b>\n\n"
            "\U0001f3ae \u904a\u3093\u3067\u3001\u52dd\u3063\u3066\u3001\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u4e0a\u3052\u3088\u3046\uff01"
        ),
        "main_menu": "\U0001f3b0 \u30e1\u30a4\u30f3\u30e1\u30cb\u30e5\u30fc",
        "games_menu": "\U0001f3ae \u30b2\u30fc\u30e0",
        "slots": "\U0001f3b0 \u30b9\u30ed\u30c3\u30c8",
        "mines": "\U0001f4a3 \u30de\u30a4\u30f3",
        "dice": "\U0001f3b2 \u30c0\u30a4\u30b9",
        "coinflip": "\U0001fa99 \u30b3\u30a4\u30f3\u30d5\u30ea\u30c3\u30d7",
        "wheel": "\U0001f3a1 \u30eb\u30fc\u30ec\u30c3\u30c8",
        "crash": "\U0001f4c8 \u30af\u30e9\u30c3\u30b7\u30e5",
        "buy_coins": "\u2b50 \u30b3\u30a4\u30f3\u8cfc\u5165",
        "withdraw": "\U0001f4b8 \u5f15\u304d\u51fa\u3057",
        "referral": "\U0001f91d \u7d39\u4ecb",
        "stats": "\U0001f4ca \u7d71\u8a08",
        "leaderboard": "\U0001f3c6 \u30e9\u30f3\u30ad\u30f3\u30b0",
        "daily_bonus": "\U0001f381 \u30c7\u30a4\u30ea\u30fc\u30dc\u30fc\u30ca\u30b9",
        "back": "\u25c0\ufe0f \u623b\u308b",
        "balance": "\U0001f4b0 \u6b8b\u9ad8: <b>{balance} \u30b3\u30a4\u30f3</b>",
        "insufficient_balance": "\u274c \u6b8b\u9ad8\u4e0d\u8db3\uff01",
        "select_bet": "\U0001f4b0 \u30d9\u30c3\u30c8\u984d\u3092\u9078\u629e:",
        "game_won": "\U0001f389 <b>\u52dd\u3061\uff01</b>\n\n\U0001f4b0 \u30d9\u30c3\u30c8: {bet}\n\u2716\ufe0f x{multiplier}\n\U0001f3c6 \u7372\u5f97: <b>{payout} \u30b3\u30a4\u30f3</b>",
        "game_lost": "\U0001f61e <b>\u8ca0\u3051\uff01</b>\n\n\U0001f4b0 \u30d9\u30c3\u30c8: {bet}\n\U0001f4b8 \u640d\u5931: {bet}",
        "play_again": "\U0001f504 \u3082\u3046\u4e00\u5ea6",
        "heads": "\U0001f535 \u8868",
        "tails": "\U0001f534 \u88cf",
        "select_language": "\U0001f310 \u8a00\u8a9e\u3092\u9078\u629e:",
        "banned_message": "\U0001f6ab \u30d0\u30f3\u3055\u308c\u3066\u3044\u307e\u3059\u3002",
    },
}


SUPPORTED_LANGUAGES = {
    "en": "English \U0001f1fa\U0001f1f8",
    "ru": "\u0420\u0443\u0441\u0441\u043a\u0438\u0439 \U0001f1f7\U0001f1fa",
    "es": "Espa\u00f1ol \U0001f1ea\U0001f1f8",
    "fr": "Fran\u00e7ais \U0001f1eb\U0001f1f7",
    "de": "Deutsch \U0001f1e9\U0001f1ea",
    "pt": "Portugu\u00eas \U0001f1e7\U0001f1f7",
    "tr": "T\u00fcrk\u00e7e \U0001f1f9\U0001f1f7",
    "hi": "\u0939\u093f\u0928\u094d\u0926\u0940 \U0001f1ee\U0001f1f3",
    "zh": "\u4e2d\u6587 \U0001f1e8\U0001f1f3",
    "ja": "\u65e5\u672c\u8a9e \U0001f1ef\U0001f1f5",
}


def get_string(key, lang='en', **kwargs):
    strings = STRINGS.get(lang, STRINGS['en'])
    text = strings.get(key)
    if text is None:
        text = STRINGS['en'].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
