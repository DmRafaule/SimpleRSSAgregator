import os
import json
import uuid


DATA_FILE_NAME = "database"
DATA_FILE_EXT = "json"
DATA_FILE = ".".join([DATA_FILE_NAME, DATA_FILE_EXT])


class Feed:
    group = None
    source = None
    time_updated = None

    def __init__(self, data: dict):
        self.id = uuid.uuid1().hex
        keys = [attr for attr in dir(Feed) if not callable(getattr(Feed, attr)) and not attr.startswith("__")]
        for key in keys:
            if key in data and data[key] is not None:
                setattr(self, key, data[key])


class DataManager:
    path = str
    data = None

    def __init__(self):
        self.path = DATA_FILE
        self.data = {}
        self.data['display'] = 'all'
        self.data['feeds'] = []
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as F:
                json.dump(self.data, F, indent=2)

    def save(self, feed: Feed) -> None:
        with open(self.path, "r", encoding="utf-8") as F:
            self.data = json.load(F)

            self.data['feeds'].append({
                'group': feed.group,
                'source': feed.source,
                'time_updated': feed.time_updated,
            })
        with open(self.path, "w", encoding="utf-8") as F:
            json.dump(self.data, F, indent=2)

    def load(self) -> list:
        with open(self.path, "r", encoding="utf-8") as F:
            self.data = json.load(F)
        return self.data['feeds']

    # Used for updating data in memory (temporarly) database
    def update(self, new_data: list) -> None:
        self.data = new_data

    # Used for updating database on hard drive (replace by data in memory)
    def updateDataBase(self) -> None:
        with open(self.path, "w", encoding="utf-8") as F:
            json.dump(self.data, F, indent=2)
