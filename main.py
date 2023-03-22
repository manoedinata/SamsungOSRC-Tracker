import os
import sys
from urllib.parse import quote

from modules.fetch import fetch
from modules.get_releases_diff import diff
from modules.telegram import telegram

if len(sys.argv) < 3:
    print("Not enough arguments!")
    exit(1)
botToken = sys.argv[1]
channelId = sys.argv[2]

# Fetch
fetch_sources = fetch()
fetch_sources.dump_to_json()

if fetch_sources.first_fetch == True:
    print("First fetch detected! Doing nothing further...")
    quit()

diff = diff(old_releases="./releases.json", releases="./releases-new.json")
get_diff = diff.get_diff()
if not get_diff:
    print("No changes detected. Skipping...")
    os.replace("./releases-new.json", "./releases.json")
    quit()

message = ""
message += "<b>New sources detected!</b>"
message += "\n"
message += "Fetch date: " + diff.releases["fetch_date"]
message += "\n\n"
for source in get_diff:
    message += f"• Model: {source['model']} \n"
    message += f"  Version: {source['version']}\n"
    message += f"  Description: {source['description']}\n"
    message += "\n"

telegram = telegram(botToken, channelId)
tgSend = telegram.send_msg(quote(message))

# Replace the current releases JSON
print("Replacing releases data...")
os.replace("./releases-new.json", "./releases.json")
