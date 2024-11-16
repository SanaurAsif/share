import json
import sys

try:
    file_name = sys.argv[1]
except IndexError:
    file_name = "final.json"

json_obj = json.load(open(file_name))

accounts = json_obj['accounts']

#usernames = ["the_capybara_meme_bot", "UEEx_Miner_bot", "battle_games_com_bot", "memefi_coin_bot", "BlumCryptoBot", "major", "xkucoinbot",
#             "seed_coin_bot", "duckscoop_bot", "shib_miner_game_bot", "pepe_miner_game_bot", "TronKeeperBot",
#             "coinegg_miner_bot", "uxlink_bot", "jackdawflipbot", "TelgatherMinigamesBot", "TGAviator_Bot", "SERAPH_official_BOT", "SoarFunTradingBot", "PAWSOG_bot", "TelgatherMinigamesBot"]

usernames = ["the_capybara_meme_bot", "UEEx_Miner_bot", "battle_games_com_bot", "memefi_coin_bot", "BlumCryptoBot", "major", "xkucoinbot",
             "seed_coin_bot", "duckscoop_bot", "shib_miner_game_bot", "pepe_miner_game_bot", "TronKeeperBot",
             "coinegg_miner_bot", "uxlink_bot", "jackdawflipbot", "TelgatherMinigamesBot", 
             "TGAviator_Bot", "SERAPH_official_BOT", "PAWSOG_bot", "uxlink_bot"]

total_accounts = len(accounts)

for username in usernames:

    available_count = 0
    not_available_count = 0
    not_checked_count = 0
    strict_refer_count = 0
    username_not_found_count = 0

    for account in accounts:
        if username in account:
            if 'strict_refer' in account:
                if account['strict_refer']:
                    strict_refer_count += 1
                else:
                    if 'started' in account[username]:
                        if account[username]['started']:
                            not_available_count += 1
                        else:
                            available_count += 1
                    else:
                        not_checked_count += 1
        else:
            username_not_found_count += 1

    print(f"\n\n [+ ] Username: {username}\n")
    print(f" [+] Total accounts: {total_accounts}")
    print(f" [+] Total available: {available_count}")
    print(f" [+] Total not available: {not_available_count}")
    print(f" [+] Total strict refer: {strict_refer_count}")
    print(f" [+] Total not checked: {not_checked_count}")
    print(f" [+] Total username not found: {username_not_found_count}")
