from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCloseEvent

from utils.search import bisect_left

if TYPE_CHECKING:
    from app import WindowController


class ListWindow(QMainWindow):
    def __init__(self, controller: "WindowController", window_id="list") -> None:
        super(ListWindow, self).__init__()
        uic.loadUi("ui/list.ui", self)

        self.controller = controller
        self.window_id = window_id

        self.line_input = self.findChild(QLineEdit, "line_input")
        self.list_vocab = self.findChild(QListWidget, "list_vocab")

        self.line_input.returnPressed.connect(self.search)
        self.line_input.textChanged.connect(self.search)
        self.list_vocab.itemDoubleClicked.connect(self.view_vocab)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        for vocab in self.controller.dict.get_vocabs():
            item = QListWidgetItem()
            item.setData(Qt.UserRole, vocab)
            item.setText(vocab.word)
            self.list_vocab.addItem(item)

    def view_vocab(self, item: QListWidgetItem) -> None:
        try:
            window_dict = self.controller.windows["dict"]
            window_dict.line_input.setText(item.text())
            window_dict.search()
        except:
            pass

    def search(self) -> None:
        word = self.line_input.text()

        if word == "":
            self.reset_list()

        prefix_vocabs = self.controller.dict.get_vocabs_by_prefix(word)

        self.list_vocab.clear()

        for vocab in prefix_vocabs:
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

    def closeEvent(self, clost_event: QCloseEvent) -> None:
        self.controller.close_window(self.window_id)

        return super().closeEvent(clost_event)
