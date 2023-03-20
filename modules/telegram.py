import requests

class telegram(object):
    def __init__(self, token, channel_id) -> None:
        self.channel_id = channel_id
        self.bot_URL = "https://api.telegram.org/bot" + token
        self.sendmsg_URL = self.bot_URL + "/sendMessage?parse_mode=HTML&chat_id=" + str(channel_id) + "&text="

    def send_msg(self, text):
        req = requests.get(self.sendmsg_URL + text)

        return req
