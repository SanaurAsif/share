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

accounts = json_obj["accounts"]

usernames = ["the_capybara_meme_bot", "UEEx_Miner_bot", "battle_games_com_bot", "memefi_coin_bot", "BlumCryptoBot", "major", "xkucoinbot",
             "seed_coin_bot", "duckscoop_bot", "shib_miner_game_bot", "pepe_miner_game_bot", "TronKeeperBot",
             "coinegg_miner_bot", "uxlink_bot", "jackdawflipbot", "TelgatherMinigamesBot", 
             "TGAviator_Bot", "SERAPH_official_BOT", "PAWSOG_bot", "uxlink_bot"]

for username in usernames:

    print(f"Resolving {username}")

    for num, account in enumerate(accounts):

        if username in account and not reload:
            continue

        print(f" Name: {account['name']}")

        api_id = account["api_id"]
        api_hash = account["api_hash"]
        session_name = account["tg_id"]
        string_session = account["string_session"]

        app = Client(session_name, api_id=api_id, api_hash=api_hash, session_string=string_session)


        async def main():
            async with app:
                peer = await app.resolve_peer(username)
                peer_dict = {attr: getattr(peer, attr) for attr in dir(peer) if not callable(getattr(peer, attr)) and not attr.startswith("__")}
                print(peer_dict)
                json_obj["accounts"][num][username] = peer_dict
                json.dump(json_obj, open(file_name, "w"), indent=4)


        app.run(main())
