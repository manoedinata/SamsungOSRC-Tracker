import json
import jsondiff

class diff(object):
    def __init__(self, old_releases, releases):
        self.diff_inserts = []

        with open(old_releases, "r") as file:
            self.old_releases = json.load(file)

        with open(releases, "r") as file:
            self.releases = json.load(file)

    def get_diff(self):
        diff = jsondiff.diff(self.old_releases, self.releases)
        insert = diff.get("releases")
        if not insert:
            return None

        sourcesDiff = insert.get(jsondiff.insert)
        if not sourcesDiff:
            return None

        for index, changes in sourcesDiff:
            self.diff_inserts.append(changes)
        return self.diff_inserts
