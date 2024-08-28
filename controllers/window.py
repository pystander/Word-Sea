from models.vocab.dictionary import Dictionary
from models.config.settings import Settings
from windows.dictionary import DictionaryWindow
from windows.list import ListWindow
from windows.flashcard import FlashCardWindow

WINDOW_CLASSES = {
    "dict": DictionaryWindow,
    "list": ListWindow,
    "flashcard": FlashCardWindow
}


class WindowController:
    """
    A controller for handling events across different windows.
    """

    def __init__(self, dict_path: str, settings_path: str) -> None:
        self.dict_path = dict_path
        self.settings_path = settings_path
        self.windows = {}

        self.dict = Dictionary()
        self.dict.from_csv(dict_path)

        self.settings = Settings()
        self.settings.from_csv(settings_path)

    def call(self, window_id: str, func_name: str, *args, **kwargs) -> None:
        if window_id in self.windows:
            getattr(self.windows[window_id], func_name)(*args, **kwargs)

    def broadcast(self, func_name: str, *args, **kwargs) -> None:
        for window in self.windows.values():
            getattr(window, func_name)(*args, **kwargs)

    def create_window(self, id: str) -> None:
        window = WINDOW_CLASSES[id](self)
        self.windows[window.window_id] = window
        self.call(window.window_id, "set_theme", self.settings.get_setting("qss_path"))

        window.show()

    def close_window(self, id: str) -> None:
        if id in self.windows:
            self.windows[id].close()
            del self.windows[id]

        if len(self.windows) == 0:
            self.settings.to_csv(self.settings_path)

    def set_theme(self, qss_path: str) -> None:
        self.settings.set_setting("qss_path", qss_path)
        self.broadcast("set_theme", self.settings.get_setting("qss_path"))
