from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from utils.search import bisect_left
from windows.window import Window

if TYPE_CHECKING:
    from app import WindowController


class ListWindow(Window):
    def __init__(self, controller: "WindowController", window_id="list") -> None:
        super(ListWindow, self).__init__(controller, window_id)
        uic.loadUi("ui/list.ui", self)

        # Widgets
        self.line_input = self.findChild(QLineEdit, "line_input")
        self.list_vocab = self.findChild(QListWidget, "list_vocab")

        self.line_input.returnPressed.connect(self.search)
        self.line_input.textChanged.connect(self.search)
        self.list_vocab.itemDoubleClicked.connect(self.view_vocab)

        for vocab in self.controller.dict.get_vocabs():
            item = QListWidgetItem()
            item.setData(Qt.UserRole, vocab)
            item.setText(vocab.word)
            self.list_vocab.addItem(item)

        # Window settings
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def view_vocab(self, item: QListWidgetItem) -> None:
        if "dict" in self.controller.windows:
            self.controller.windows["dict"].line_input.setText(item.text())
            self.controller.windows["dict"].search()

    def search(self) -> None:
        word = self.line_input.text()

        if word == "":
            self.reset_list()

        self.list_vocab.clear()

        for vocab in self.controller.dict.get_vocabs_by_prefix(word):
            item = QListWidgetItem()
            item.setData(Qt.UserRole, vocab)
            item.setText(vocab.word)
            self.list_vocab.addItem(item)

    def add_item(self, word: str) -> None:
        item = QListWidgetItem()
        item.setData(Qt.UserRole, self.controller.dict.get_vocab(word))
        item.setText(word)
        self.list_vocab.addItem(item)
        self.list_vocab.sortItems()

    def remove_item(self, word: str) -> None:
        left = bisect_left(self.controller.dict.get_words(), word)
        self.list_vocab.takeItem(left)

    def clear_item(self) -> None:
        self.list_vocab.clear()

    def reset_list(self) -> None:
        self.clear_item()

        for vocab in self.controller.dict.get_vocabs():
            item = QListWidgetItem()
            item.setData(Qt.UserRole, vocab)
            item.setText(vocab.word)
            self.list_vocab.addItem(item)
