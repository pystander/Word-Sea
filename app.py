import sys
import os

from PyQt5.QtWidgets import QApplication

from models.dict import Dictionary
from windows.dictionary import DictionaryWindow
from windows.list import ListWindow

DATA_DIR = "data/"
DICT_PATH = DATA_DIR + "dictionary.csv"
WINDOW_CLASSES = {
    "dict": DictionaryWindow,
    "list": ListWindow,
}


class WindowController:
    """
    A controller for handling events across different windows.
    """

    def __init__(self, dict_path: str) -> None:
        self.dict_path = dict_path
        self.stylesheet = ""

        self.dict = Dictionary()
        self.dict.from_csv(dict_path)

        self.windows = {}

    def open_window(self, id: str) -> None:
        if id in self.windows:
            self.windows[id].show()
            return

        window = WINDOW_CLASSES[id](self)
        self.windows[window.window_id] = window

        window.setStyleSheet(self.stylesheet)
        window.show()

    def close_window(self, id: str) -> None:
        if id in self.windows:
            self.windows[id].close()
            del self.windows[id]

    def set_theme(self, qss="") -> None:
        self.stylesheet = qss

        for window in self.windows.values():
            window.setStyleSheet(self.stylesheet)


if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    app = QApplication(sys.argv)
    controller = WindowController(DICT_PATH)
    controller.open_window("dict")

    sys.exit(app.exec_())
