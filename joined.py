from pyrogram import Client
import json
import sys

try:
    reload = sys.argv[1]
except IndexError:
    reload = "0"

if reload == "1":
    print("Reloading is enabled")
    reload = True
else:
    print("Reloading is disabled")
    reload = False

try:
    file_name = sys.argv[2]
except IndexError:
    file_name = "final.json"

json_obj = json.load(open(file_name))

accounts = json_obj['accounts']

# usernames = ["the_capybara_meme_bot", "UEEx_Miner_bot", "battle_games_com_bot", "memefi_coin_bot", "BlumCryptoBot", "major", "xkucoinbot",
#              "seed_coin_bot", "duckscoop_bot", "shib_miner_game_bot", "pepe_miner_game_bot", "TronKeeperBot",
#              "coinegg_miner_bot", "uxlink_bot", "jackdawflipbot", "TelgatherMinigamesBot"]

#usernames = ["TGAviator_Bot", "SERAPH_official_BOT", "PAWSOG_bot", "TelgatherMinigamesBot", "uxlink_bot", "RealSpin_bot"]

usernames = ["the_capybara_meme_bot", "UEEx_Miner_bot", "battle_games_com_bot", "memefi_coin_bot", "BlumCryptoBot", "major", "xkucoinbot",
             "seed_coin_bot", "duckscoop_bot", "shib_miner_game_bot", "pepe_miner_game_bot", "TronKeeperBot",
             "coinegg_miner_bot", "uxlink_bot", "jackdawflipbot", "TelgatherMinigamesBot", 
             "TGAviator_Bot", "SERAPH_official_BOT", "PAWSOG_bot", "uxlink_bot"]


for username in usernames:
    print(f"Resolving {username}")

    for num, account in enumerate(accounts):

        api_id = account['api_id']
        api_hash = account['api_hash']
        session_name = account['tg_id']
        string_session = account['string_session']

        app = Client(session_name, api_id=api_id, api_hash=api_hash, session_string=string_session)

        if username in account:
            if 'started' in account[username]:
                if not reload:
                    continue
                else:
                    if account[username]['started']:
                        print(f' [-] {username} already started before')
                        continue

        print(f" Name: {account['name']}")

        async def check_bot_started():
            async with app:
                ran = False
                async for _ in app.get_chat_history(username, limit=1):
                    print(f' [-] {username} started before')
                    ran = True

                    break

                if ran:
                    json_obj['accounts'][num][username]['started'] = True

                    with open(file_name, 'w') as f:
                        json.dump(json_obj, f, indent=4)
                else:
                    print(f' [+] {username} not started before')
                    json_obj['accounts'][num][username]['started'] = False

                    with open(file_name, 'w') as f:
                        json.dump(json_obj, f, indent=4)


        # Run the coroutine
        app.run(check_bot_started())
