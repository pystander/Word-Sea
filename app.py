import sys
import os

from PyQt5.QtWidgets import QApplication

from models.dictionary import Dictionary
from windows.dictionary import DictionaryWindow
from windows.list import ListWindow
from windows.flashcard import FlashCardWindow

DATA_DIR = "data/"
DICT_PATH = DATA_DIR + "dictionary.csv"
WINDOW_CLASSES = {
    "dict": DictionaryWindow,
    "list": ListWindow,
    "flashcard": FlashCardWindow
}


class WindowController:
    """
    A controller for handling events across different windows.
    """

    def __init__(self, dict_path: str = DICT_PATH) -> None:
        self.dict_path = dict_path
        self.stylesheet = ""
        self.windows = {}

        self.dict = Dictionary()
        self.dict.from_csv(dict_path)

    def call(self, window_id: str, func_name: str, *args, **kwargs) -> None:
        if window_id in self.windows:
            getattr(self.windows[window_id], func_name)(*args, **kwargs)

    def broadcast(self, func_name: str, *args, **kwargs) -> None:
        for window in self.windows.values():
            getattr(window, func_name)(*args, **kwargs)

    def create_window(self, id: str) -> None:
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
        self.broadcast("setStyleSheet", qss)


if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    app = QApplication(sys.argv)
    controller = WindowController()
    controller.create_window("dict")

    sys.exit(app.exec_())
