from pyrogram import Client
from lxml import html
import argparse
import requests
import random
import string
import time
import json
import sys
import os

parser = argparse.ArgumentParser(description="Process and set name, username, password, and email etc.")

parser.add_argument("--start", type=int, default=1, help="Start index for account creation")
parser.add_argument("--end", type=int, default=-1, help="End index for account creation")
parser.add_argument("--file", type=str, default="add.json", help="Path to json file (default: 'add.json')")
parser.add_argument("--api", action="store_true", default=False, help="Set API ID and Hash (default: False)")
parser.add_argument("--name", action="store_true", default=False, help="Set/change Name (default: False)")
parser.add_argument("--username", action="store_true", default=False, help="Set/change username (default: False)")
parser.add_argument("--fa2", action="store_true", default=False, help="Set/change password (default: False)")
parser.add_argument("--email", action="store_true", default=False, help="Set/change login email (default: False)")
parser.add_argument("--name-file", type=str, default="names.csv", help="Path to names file (default: 'names.csv')")
parser.add_argument("--ip", action="store_true", default=False, help="Change IP after each account (default: False)")
parser.add_argument("--pwd", type=str, help="Password to use or set (Required when --fa2 is set")

api_id_xpath = '//label[text()="App api_id:"]/parent::div/div/span/strong/text()'
api_hash_xpath = '//label[text()="App api_hash:"]/parent::div/div/span/text()'
app_title_xpath = '//input[@id="app_title"]/@value'
app_short_name_xpath = '//input[@id="app_shortname"]/@value'
create_hash_xpath = '//input[@name="hash"]/@value'

args = parser.parse_args()

skip_api = False

print(f"\nStart: {args.start}")
print(f"End: {args.end}")
print(f"File: {args.file}")
print(f"Set API: {args.api}")
print(f"Set Name: {args.name}")
print(f"Set Username: {args.username}")
print(f"Set Password: {args.fa2}")
print(f"Set Email: {args.email}")
print(f"Name File: {args.name_file}")
print(f"Password: {args.pwd}\n\n")

if args.fa2 and not args.pwd:
    print("Error: --pwd is required when --fa2 is set.")
    sys.exit(1)

if (args.name or args.username) and not args.file:
    print(f"Error: --file is required when {'--name' if args.name else '--username'} is set.")
    sys.exit(1)
else:
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

try:
    accounts = json.load(open(args.file))['accounts']
    if len(accounts) < 1:
        raise Exception("No accounts found in the file.")

    start = args.start - 1
    if args.end < 0:
        end = len(accounts)
    else:
        end = args.end - 1

except FileNotFoundError:
    print(f"Error: File '{args.file}' not found.")
    sys.exit(1)
except KeyError:
    print(f"Error: File '{args.file}' does not contain 'accounts' key.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: File '{args.file}' is not a valid JSON file.")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e.__class__.__name__} - {e}")
    sys.exit(1)

fa2 = args.pwd

time_out = 20
ip_change = False
success_count = 0
failed_count = 0
failed = {}

def change_ip():
    start_time_ = time.time()
    print("Changing IP...")
    os.system(
        "su -c cmd connectivity airplane-mode enable && su -c sleep 1 && "
        "su -c cmd connectivity airplane-mode disable"
    )
    while time.time() - start_time_ < 100:
        try:
            requests.head("https://google.com")
            print("Ip changed")
            break
        except:  # noqa
            pass

    time.sleep(1)

    changed_ip = False
    while time.time() - start_time_ < 100:
        try:
            requests.head("https://google.com")
            print("Ip changed")
            changed_ip = True
            break
        except:  # noqa
            pass

    return changed_ip


for i in range(start, end):
    try:
        os.remove('add_account.session')
    except FileNotFoundError:
        pass

    json_obj = json.load(open(args.file))

    accounts = json_obj["accounts"]

    account = accounts[i]
    tg_id = account["tg_id"]
    number = "+88" + account["number"]
    string_session = account["string_session"]
    config_name = account["name"]

    try:
        api_id = account["api_id"]
    except KeyError:
        api_id = 26490266

    try:
        api_hash = account["api_hash"]
    except KeyError:
        api_hash = "ed36fb11b5a837f0be587cbf216bb4db"

    if ip_change:
        if not change_ip():
            print("Error: IP not changed.")
            sys.exit(1)
        else:
            ip_change = False

    try:

        app = Client("add_account", api_id, api_hash, app_version="Android 11.1.1",
                     device_model="Redmi Redmi Note 11 Pro 5G", system_version="Linux 5.4.147-qgki-ge80e80e512ef",
                     password=fa2, session_string=string_session, in_memory=True)


        async def main():
            global success_count, failed_count, skip_api
            async with app:
                print(f"Account : {config_name}")
                user = await app.get_me()

                if user.last_name:
                    name = user.first_name + " " + user.last_name
                else:
                    name = user.first_name

                user_name_current = user.username

                if args.name or args.username:
                    names_file = open(args.name_file, "r")
                    names_txt = names_file.read()
                    names_file.close()
                    found_uni = False
                    for name_line in names_txt.split("\n"):
                        if len(name_line.split(",")) == 2:
                            f_name = name_line.split(",")[0].strip()
                            l_name = name_line.split(",")[1].strip()
                            found_uni = True
                            with open(args.name_file, "w") as names_file:
                                names_file.write(names_txt.replace(f_name + "," + l_name, "username"))
                                names_file.close()
                            break

                    if not found_uni:
                        print("Error: No unique name found in file.")
                        sys.exit(1)

                if args.name:

                    is_name_set = False

                    try:
                        print(f"Setting name to {f_name} {l_name}")
                        await app.update_profile(first_name=f_name, last_name=l_name)
                        is_name_set = True
                        print(f"Name set to {f_name} {l_name}")
                    except Exception as e_:
                        try:
                            print(e_.__class__.__name__ + " - " + str(e_) + "\n")
                            print("Name not set. Trying again.")
                            await app.update_profile(first_name=f_name, last_name=l_name)
                            is_name_set = True
                            print(f"Name set to {f_name} {l_name}")
                        except Exception as e_:
                            print(e_.__class__.__name__ + " - " + str(e_) + "\n")

                    if not is_name_set:
                        print("Error: Name not set.")
                        sys.exit(1)
                    else:
                        name = f_name + " " + l_name

                if args.username:

                    username_to_set = f"{f_name}{l_name}"

                    is_username_set = False

                    try:
                        print(f"Setting username to {username_to_set}")
                        await app.set_username(username_to_set)
                        is_username_set = True
                        print(f"Username set to {username_to_set}")
                    except:  # noqa
                        # print(e.__class__.__name__ + " - " + str(e) + "\n")
                        print("Username not set. Trying again.")
                        rand_4_letters = ''.join(random.choices(string.ascii_lowercase, k=4))
                        username_to_set = f"{f_name}{l_name}{rand_4_letters}"
                        try:
                            print(f"Setting username to {username_to_set}")
                            await app.set_username(username_to_set)
                            is_username_set = True
                            print(f"Username set to {username_to_set}")
                        except Exception as e_:
                            print(e_.__class__.__name__ + " - " + str(e_) + "\n")
                            print("Username not set. Trying again.")
                            username_to_set = f"{f_name}{l_name}{random.randint(100, 999)}"
                            try:
                                print(f"Setting username to {username_to_set}")
                                await app.set_username(username_to_set)
                                is_username_set = True
                                print(f"Username set to {username_to_set}")
                            except Exception as e_:
                                print(e_.__class__.__name__ + " - " + str(e_) + "\n")
                                print("Username not set. Trying again.")
                                rand_3_digits = str(random.randint(100, 999))
                                rand_4_letters = ''.join(random.choices(string.ascii_lowercase, k=4))
                                username_to_set = f"{f_name}{rand_4_letters}{l_name}"
                                try:
                                    print(f"Setting username to {username_to_set}")
                                    await app.set_username(username_to_set)
                                    is_username_set = True
                                    print(f"Username set to {username_to_set}")
                                except Exception as e_:
                                    print(e_.__class__.__name__ + " - " + str(e_) + "\n")
                                    print("Username not set. Trying again.")
                                    username_to_set = f"{f_name}{rand_3_digits}{rand_4_letters}{l_name}"
                                    try:
                                        print(f"Setting username to {username_to_set}")
                                        await app.set_username(username_to_set)
                                        is_username_set = True
                                        print(f"Username set to {username_to_set}")
                                    except Exception as e_:
                                        print(e_.__class__.__name__ + " - " + str(e_) + "\n")

                    if not is_username_set:
                        print("Error: Username not set.")
                        sys.exit(1)
                    else:
                        user_name = username_to_set
                else:
                    user_name = user_name_current

                if args.api:

                    if 'api_id' in account and 'api_hash' in account:
                        print("API ID and Hash already set.")
                        skip_api = True
                    else:
                        skip_api = False
                        print("Setting API ID and Hash")

                        headers = {
                            'Host': 'my.telegram.org',
                            'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                            'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Sec-Ch-Ua-Platform': '"Android"',
                            'X-Requested-With': 'XMLHttpRequest',
                            'Sec-Ch-Ua-Mobile': '?1',
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://my.telegram.org',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://my.telegram.org/auth?to=apps',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Priority': 'u=1, i',
                        }

                        data = {
                            'phone': number,
                        }

                        response = requests.post('https://my.telegram.org/auth/send_password', headers=headers, data=data)
                        print(response.text)

                        random_hash = response.json()['random_hash']

                        start_time = time.time()

                        code = None

                        time.sleep(2)

                        while time.time() - start_time < time_out and not code:
                            async for dialog in app.get_dialogs(10):
                                try:
                                    message_text = dialog.top_message.text
                                    if 'web login code' in message_text.lower():
                                        code = message_text.split(':\n')[1].split('\n')[0].strip()
                                        print(f"Web Code: {code}")
                                        break
                                except:  # noqa
                                    time.sleep(2)

                        if not code:
                            raise Exception("Code not received.")

                        headers = {
                            'Host': 'my.telegram.org',
                            'Sec-Ch-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                            'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Sec-Ch-Ua-Platform': '"Android"',
                            'X-Requested-With': 'XMLHttpRequest',
                            'Sec-Ch-Ua-Mobile': '?1',
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://my.telegram.org',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://my.telegram.org/auth?to=apps',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Priority': 'u=1, i',
                        }

                        data = {
                            'phone': number,
                            'random_hash': random_hash,
                            'password': code,
                            'remember': '1',
                        }

                        response = requests.post('https://my.telegram.org/auth/login', headers=headers, data=data)
                        print(response.text)

                        cook = response.cookies.get_dict()
                        print(cook)

                        stel_token = cook['stel_token']
                        json_obj["accounts"][i]["stel_token"] = str(stel_token)

                        headers = {
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'cache-control': 'max-age=0',
                            'priority': 'u=0, i',
                            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'document',
                            'sec-fetch-mode': 'navigate',
                            'sec-fetch-site': 'none',
                            'sec-fetch-user': '?1',
                            'upgrade-insecure-requests': '1',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        }

                        response = requests.get('https://my.telegram.org/apps', cookies=cook, headers=headers)
                        doc = html.fromstring(response.text)

                        try:
                            api_id_ = doc.xpath(api_id_xpath)[0]
                            api_hash_ = doc.xpath(api_hash_xpath)[0]
                            app_title = doc.xpath(app_title_xpath)[0]
                            app_short_name = doc.xpath(app_short_name_xpath)[0]
                        except IndexError:
                            create_hash = doc.xpath(create_hash_xpath)[0]

                            cookies = {
                                'stel_token': f'{stel_token}',
                            }

                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; 2201116SG Build/TD1A.221105.003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.70 Mobile Safari/537.36',
                                'sec-ch-ua-platform': '"Android"',
                                'x-requested-with': 'XMLHttpRequest',
                                'sec-ch-ua': '"Android WebView";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'sec-ch-ua-mobile': '?1',
                                'origin': 'https://my.telegram.org',
                                'sec-fetch-site': 'same-origin',
                                'sec-fetch-mode': 'cors',
                                'sec-fetch-dest': 'empty',
                                'referer': 'https://my.telegram.org/apps',
                                'accept-language': 'en-US,en;q=0.9',
                                'priority': 'u=1, i'
                            }

                            rand_3_lts = ''.join(random.choices(string.ascii_lowercase, k=3))

                            data = {
                                'hash': create_hash,
                                'app_title': name,
                                'app_shortname': f"{name.replace(' ', '')}{rand_3_lts}"[0:30],
                                'app_url': '',
                                'app_platform': 'android',
                                'app_desc': '',
                            }

                            requests.post('https://my.telegram.org/apps/create', cookies=cookies, headers=headers, data=data)

                            headers = {
                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                                'cache-control': 'max-age=0',
                                'priority': 'u=0, i',
                                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-ch-ua-platform': '"Windows"',
                                'sec-fetch-dest': 'document',
                                'sec-fetch-mode': 'navigate',
                                'sec-fetch-site': 'none',
                                'sec-fetch-user': '?1',
                                'upgrade-insecure-requests': '1',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                            }

                            response = requests.get('https://my.telegram.org/apps', cookies=cook, headers=headers)
                            doc = html.fromstring(response.text)

                            api_id_ = doc.xpath(api_id_xpath)[0]
                            api_hash_ = doc.xpath(api_hash_xpath)[0]
                            app_title = doc.xpath(app_title_xpath)[0]
                            app_short_name = doc.xpath(app_short_name_xpath)[0]

                    with open(args.file, 'w') as f:
                        if args.name:
                            json_obj["accounts"][i]["name"] = name
                        if args.username:
                            json_obj["accounts"][i]["username"] = user_name
                        if args.api and not skip_api:
                            json_obj["accounts"][i]["api_id"] = api_id_
                            json_obj["accounts"][i]["api_hash"] = api_hash_
                            json_obj["accounts"][i]["app_title"] = app_title
                            json_obj["accounts"][i]["app_short_name"] = app_short_name

                        json.dump(json_obj, f, indent=4)

        app.run(main())

        if not skip_api:
            success_count += 1
            if args.ip:
                ip_change = True
        else:
                ip_change = False

        print(f"Success: {success_count} - Failed: {failed_count}")

    except Exception as e:
        ip_change = True
        print(e.__class__.__name__ + " - " + str(e) + "\n")
        failed_count += 1
        failed[number] = f"{e.__class__.__name__} - {str(e)}"
