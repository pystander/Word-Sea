import os
import csv


class Settings:
    """
    A model class for storing and retrieving Setting(s).
    """

    def __init__(self):
        self.settings = {}

    def set_setting(self, key: str, value: str) -> None:
        self.settings[key] = value

    def get_setting(self, key: str) -> str | None:
        return self.settings.get(key, None)

    def from_csv(self, path: str) -> None:
        if not os.path.exists(path):
            return

        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            self.settings = {row[0]: row[1] for row in reader}

    def to_csv(self, path: str) -> None:
        with open(path, "w+", newline="") as f:
            writer = csv.writer(f)

            for key, value in self.settings.items():
                writer.writerow([key, value])
