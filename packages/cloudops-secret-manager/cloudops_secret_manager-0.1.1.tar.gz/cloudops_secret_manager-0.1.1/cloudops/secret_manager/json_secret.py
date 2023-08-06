import json


class JSONSecret:
    def __init__(self, path: str):
        self.path = path

    def pull(self) -> dict:
        with open(self.path, "r") as f:
            return json.load(f)

    def push(self, payload: dict) -> None:
        with open(self.path, "w") as f:
            json.dump(payload, f)
