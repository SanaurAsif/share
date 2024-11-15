from pyrogram import Client
import argparse
import random
import string
import json
import sys
import os

parser = argparse.ArgumentParser(description="Input owner, username, and optional flags.")

parser.add_argument("owner", nargs='?', default="me", help="Owner's name (default: 'me')")
parser.add_argument("--name", action="store_true", default=False, help="Set/change Name (default: False)")
parser.add_argument("--username", action="store_true", default=False, help="Set/change username (default: False)")
parser.add_argument("--fa2", action="store_true", default=False, help="Set/change password (default: False)")
parser.add_argument("--email", action="store_true", default=False, help="Set/change login email (default: False)")
parser.add_argument("--file", type=str, default="names.csv", help="Path to names file (default: 'names.csv')")
parser.add_argument("--pwd", type=str, help="Password to use or set (Required when --fa2 is set")

args = parser.parse_args()

print(f"\nOwner: {args.owner}")
print(f"Set Name: {args.name}")
print(f"Set Username: {args.username}")
print(f"Set Password: {args.fa2}")
print(f"Set Email: {args.email}")
print(f"File Name: {args.file}")
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

fa2 = args.pwd

owner_name = args.owner

while True:

    phone = input("Enter your phone number with country code: ")

    if not phone:
        break

    try:
        os.remove('add_account.session')
    except FileNotFoundError:
        pass

    app = Client("add_account", 26490266, "ed36fb11b5a837f0be587cbf216bb4db", app_version="Android 11.1.1",
                 device_model="Redmi Redmi Note 11 Pro 5G", system_version="Linux 5.4.147-qgki-ge80e80e512ef",
                 phone_number=phone, hide_password=True, password=fa2, in_memory=True)


    async def main():
        async with app:

            user = await app.get_me()

            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name

            tg_id = user.id
            user_name_current = user.username

            if args.name or args.username:
                names_file = open(args.file, "r")
                names_txt = names_file.read()
                names_file.close()
                found_uni = False
                for name_line in names_txt.split("\n"):
                    if len(name_line.split(",")) == 2:
                        f_name = name_line.split(",")[0].strip()
                        l_name = name_line.split(",")[1].strip()
                        found_uni = True
                        with open(args.file, "w") as names_file:
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
                except Exception as e:
                    try:
                        print(e.__class__.__name__ + " - " + str(e) + "\n")
                        print("Name not set. Trying again.")
                        await app.update_profile(first_name=f_name, last_name=l_name)
                        is_name_set = True
                        print(f"Name set to {f_name} {l_name}")
                    except Exception as e:
                        print(e.__class__.__name__ + " - " + str(e) + "\n")

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
                    except Exception as e:
                        print(e.__class__.__name__ + " - " + str(e) + "\n")
                        print("Username not set. Trying again.")
                        username_to_set = f"{f_name}{l_name}{random.randint(100, 999)}"
                        try:
                            print(f"Setting username to {username_to_set}")
                            await app.set_username(username_to_set)
                            is_username_set = True
                            print(f"Username set to {username_to_set}")
                        except Exception as e:
                            print(e.__class__.__name__ + " - " + str(e) + "\n")
                            print("Username not set. Trying again.")
                            rand_3_digits = str(random.randint(100, 999))
                            rand_4_letters = ''.join(random.choices(string.ascii_lowercase, k=4))
                            username_to_set = f"{f_name}{rand_4_letters}{l_name}"
                            try:
                                print(f"Setting username to {username_to_set}")
                                await app.set_username(username_to_set)
                                is_username_set = True
                                print(f"Username set to {username_to_set}")
                            except Exception as e:
                                print(e.__class__.__name__ + " - " + str(e) + "\n")
                                print("Username not set. Trying again.")
                                username_to_set = f"{f_name}{rand_3_digits}{rand_4_letters}{l_name}"
                                try:
                                    print(f"Setting username to {username_to_set}")
                                    await app.set_username(username_to_set)
                                    is_username_set = True
                                    print(f"Username set to {username_to_set}")
                                except Exception as e:
                                    print(e.__class__.__name__ + " - " + str(e) + "\n")

                if not is_username_set:
                    print("Error: Username not set.")
                    sys.exit(1)
                else:
                    user_name = username_to_set
            else:
                user_name = user_name_current

            print(f" [+] {name} - {tg_id}")

            string_session = await app.export_session_string()

            try:
                r_file = open("add.json", "r")
                pre_json = json.load(r_file)
                r_file.close()
                if 'accounts' in pre_json:
                    if pre_json['accounts']:
                        accounts_list = pre_json['accounts']
            except FileNotFoundError:
                accounts_list = []

            accounts_list.append(
                {"tg_id": f"{tg_id}", "number": f"{phone.replace('+88', '')}", "username": f"{user_name}",
                 "name": f"{name}", "string_session": f"{string_session}", "strict_refer": False, "owner": owner_name}
            )

            main_dict = {
                "accounts": accounts_list
            }

            with open('add.json', 'w') as json_file:
                json.dump(main_dict, json_file, indent=4)


    app.run(main())
