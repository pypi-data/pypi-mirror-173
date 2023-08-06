import yaml


class YAMLSecret:
    def __init__(self, path: str):
        self.path = path

    def pull(self) -> dict:
        with open(self.path, "r") as f:
            return yaml.safe_load(f)

    def push(self, payload: dict) -> None:
        with open(self.path, "w") as f:
            yaml.dump(payload, f)
