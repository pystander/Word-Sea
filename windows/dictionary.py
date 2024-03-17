from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QCloseEvent

from api.cambridge import fetch
from models.dict import Vocabulary, Dictionary

if TYPE_CHECKING:
    from app import WindowController


class DictionaryWindow(QMainWindow):
    def __init__(self, controller: "WindowController", window_id="dict") -> None:
        super(DictionaryWindow, self).__init__()
        uic.loadUi("ui/dictionary.ui", self)

        self.controller = controller
        self.window_id = window_id

        # Widgets
        self.line_input = self.findChild(QLineEdit, "line_input")
        self.button_search = self.findChild(QPushButton, "button_search")
        self.button_clear = self.findChild(QPushButton, "button_clear")
        self.button_remove = self.findChild(QPushButton, "button_remove")
        self.checkbox_learn = self.findChild(QCheckBox, "checkbox_learn")
        self.list_cluster = self.findChild(QListWidget, "list_cluster")

        self.line_input.returnPressed.connect(self.search)
        self.button_search.clicked.connect(self.search)
        self.button_clear.clicked.connect(self.clear)
        self.button_remove.clicked.connect(self.remove)

        self.completer = QCompleter(self.controller.dict.get_words())
        self.line_input.setCompleter(self.completer)

        # File menu
        self.action_open = self.findChild(QAction, "action_open")
        self.action_save = self.findChild(QAction, "action_save")
        self.action_save_as = self.findChild(QAction, "action_save_as")
        self.action_reset = self.findChild(QAction, "action_reset")

        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)
        self.action_save_as.triggered.connect(self.save_as)
        self.action_reset.triggered.connect(self.reset)

        self.action_save.setShortcut("Ctrl+S")

        # View menu
        self.action_theme_default = self.findChild(QAction, "action_theme_default")
        self.action_theme_dark = self.findChild(QAction, "action_theme_dark")
        self.action_list = self.findChild(QAction, "action_list")

        self.action_theme_default.triggered.connect(lambda: self.set_theme(""))
        self.action_theme_dark.triggered.connect(lambda: self.set_theme("qss/dark.qss"))
        self.action_list.triggered.connect(self.create_list_window)

        # Window settings
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def search(self) -> None:
        word = self.line_input.text()

        if word == "":
            return

        vocab = self.controller.dict.get_vocab(word)

        if vocab == None:
            vocab = fetch(word)

            if vocab == None:
                return

            if self.checkbox_learn.isChecked():
                self.controller.dict.add_vocab(vocab)
                self.completer.model().setStringList(self.controller.dict.get_words())

                if "list" in self.controller.windows:
                    self.controller.windows["list"].add_item(vocab.word)

        self.show_vocab(vocab)

    def clear(self) -> None:
        self.list_cluster.clear()
        self.line_input.setText("")

    def remove(self) -> None:
        if self.list_cluster.count() == 0:
            return

        word = self.list_cluster.item(0).text()
        self.controller.dict.remove_word(word)
        self.completer.model().setStringList(self.controller.dict.get_words())

        self.list_cluster.clear()
        self.line_input.setText("")

        if "list" in self.controller.windows:
            window_list = self.controller.windows["list"]
            window_list.remove_item(word)

    def show_vocab(self, vocab: Vocabulary) -> None:
        font = QFont()
        font.setBold(True)

        item = QListWidgetItem()
        item.setText(vocab.word)
        item.setFont(font)

        self.list_cluster.clear()
        self.list_cluster.addItem(item)

        for pos, cluster in vocab.clusters.items():
            meanings = cluster.meanings
            examples = cluster.examples
            synonyms = cluster.synonyms
            antonyms = cluster.antonyms
            related = cluster.related

            item = QListWidgetItem()

            cluster_text = pos + "\n"

            for i, meaning in enumerate(meanings):
                cluster_text += "%d. %s" % (i + 1, meaning) + "\n"

            if len(examples) > 0 and examples[0] != "":
                cluster_text += "\n" + "Examples:" + "\n"

                for example in examples:
                    cluster_text += "    " + "- %s" % example + "\n"

            if len(synonyms) > 0 and synonyms[0] != "":
                cluster_text += "\n" + "Synonyms: " + ', '.join(synonyms) + "\n"

            if len(antonyms) > 0 and antonyms[0] != "":
                cluster_text += "\n" + "Antonyms: " + ', '.join(antonyms) + "\n"

            if len(related) > 0 and related[0] != "":
                cluster_text += "\n" + "Related: " + ', '.join(related) + "\n"

            item.setText(cluster_text)
            self.list_cluster.addItem(item)

        self.controller.dict.sort()

    def open(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("csv")
        file_name, _ = dialog.getOpenFileName(self, "QFileDialog.getSaveFileName()", "", "CSV (*.csv)")

        if file_name:
            self.controller.dict = Dictionary()
            self.controller.dict.from_csv(file_name)

        self.completer.model().setStringList(self.controller.dict.get_words())
        self.controller.dict_path = file_name

    def save(self) -> None:
        self.controller.dict.to_csv(self.controller.dict_path)

    def save_as(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("csv")
        file_name, _ = dialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "CSV (*.csv)")

        if file_name:
            self.controller.dict.to_csv(file_name)
            self.controller.dict_path = file_name

    def reset(self) -> None:
        self.controller.dict = Dictionary()
        self.list_cluster.clear()
        self.completer = QCompleter(self.controller.dict.get_words())
        self.line_input.setCompleter(self.completer)
        self.line_input.setText("")

        if "list" in self.controller.windows:
            self.controller.windows["list"].clear_item()

    def read_qss(self, path: str) -> str:
        with open(path, "r") as f:
            return f.read()

    def create_list_window(self) -> None:
        self.controller.create_window("list")

    def set_theme(self, path: str) -> None:
        if path == "":
            self.controller.set_theme("")
        else:
            qss = self.read_qss(path)
            self.controller.set_theme(qss)

    # Override
    def closeEvent(self, clost_event: QCloseEvent) -> None:
        self.save()
        self.controller.close_window(self.window_id)

        return super().closeEvent(clost_event)
