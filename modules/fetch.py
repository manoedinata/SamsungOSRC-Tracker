import requests
import urllib3
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

class fetch(object):
    def __init__(self):
        self.URL = "https://opensource.samsung.com/uploadList?menuItem=mobile&classification1=mobile_phone"
        self.first_fetch = False
        self.data = {}
        self.releases = []

        self.session = requests.Session()
        self.session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def fetch_parse_sources(self):
        req = self.session.get(self.URL)
        parse = BeautifulSoup(req.text, "html.parser")

        return parse

    def dump_to_json(self):
        parse = self.fetch_parse_sources()
        currentTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        releasesTable = parse.find("table", {"class": "tbl-downList"})
        for release in releasesTable.find_all("tr", {"class": ""})[1:]:
            model = release.find_all("td")[0].text.strip()
            version = release.find_all("td")[1].encode_contents().decode().strip()
            if "<br/>" in version:
                version = ", ".join([x for x in version.split("<br/>")])
            description = release.find_all("td")[2].encode_contents().decode().strip()
            if "<br/>" in description:
                description = ", ".join([x for x in description.split("<br/>")])
            
            self.releases.append({
                "model": model,
                "version": version,
                "description": description,
            })

        self.data = {
            "fetch_date": currentTime,
            "releases": self.releases
        }

        fileName = "releases-new.json"
        if not os.path.exists("releases.json"):
            fileName = "releases.json"
            self.first_fetch = True

        with open(fileName, "w") as file:
            json.dump(self.data, file, indent=4)
