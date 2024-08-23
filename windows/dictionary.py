from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QCloseEvent, QIcon

from api.cambridge import fetch
from models.dictionary import Vocabulary
from windows.window import Window

if TYPE_CHECKING:
    from app import WindowController


class DictionaryWindow(Window):
    def __init__(self, controller: "WindowController", window_id="dict") -> None:
        super(DictionaryWindow, self).__init__(controller, window_id)
        uic.loadUi("ui/dictionary.ui", self)

        # Window settings
        self.setWindowIcon(QIcon("ui/icons/uil--book-reader.png"))

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

        self.action_open.setIcon(QIcon("ui/icons/uil--folder-open.png"))
        self.action_save.setIcon(QIcon("ui/icons/bx--save.png"))
        self.action_save_as.setIcon(QIcon("ui/icons/bxs--save.png"))
        self.action_reset.setIcon(QIcon("ui/icons/uil--trash-alt.png"))

        # View menu
        self.action_theme_default = self.findChild(QAction, "action_theme_default")
        self.action_theme_dark = self.findChild(QAction, "action_theme_dark")
        self.action_list = self.findChild(QAction, "action_list")
        self.action_flashcard = self.findChild(QAction, "action_flashcard")
        self.action_import_qss = self.findChild(QAction, "action_import_qss")

        self.action_theme_default.triggered.connect(lambda: self.controller.set_theme(""))
        self.action_theme_dark.triggered.connect(lambda: self.controller.set_theme("ui/qss/dark.qss"))
        self.action_list.triggered.connect(lambda: self.controller.create_window("list"))
        self.action_flashcard.triggered.connect(lambda: self.controller.create_window("flashcard"))
        self.action_import_qss.triggered.connect(lambda: self.import_qss())

        self.menu_theme = self.findChild(QMenu, "menu_theme")
        self.menu_theme.setIcon(QIcon("ui/icons/uil--brush-alt.png"))
        self.action_list.setIcon(QIcon("ui/icons/uil--list-ul.png"))
        self.action_flashcard.setIcon(QIcon("ui/icons/mingcute--board-line.png"))
        self.action_import_qss.setIcon(QIcon("ui/icons/uil--import.png"))

        # Window settings
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Disable resizing
        self.setFixedSize(self.size())

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
        file_name, _ = dialog.getOpenFileName(self, "Open", "", "CSV (*.csv)")

        if file_name:
            self.controller.dict.reset()
            self.controller.dict.from_csv(file_name)

            self.completer.model().setStringList(self.controller.dict.get_words())
            self.controller.dict_path = file_name

    def save(self) -> None:
        self.controller.dict.to_csv(self.controller.dict_path)

    def save_as(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("csv")
        file_name, _ = dialog.getSaveFileName(self, "Save", "", "CSV (*.csv)")

        if file_name:
            self.controller.dict.to_csv(file_name)
            self.controller.dict_path = file_name

    def reset(self) -> None:
        self.controller.dict.reset()
        self.list_cluster.clear()
        self.completer = QCompleter(self.controller.dict.get_words())
        self.line_input.setCompleter(self.completer)
        self.line_input.setText("")

        if "list" in self.controller.windows:
            self.controller.windows["list"].clear_item()

    def import_qss(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("qss")
        file_name, _ = dialog.getOpenFileName(self, "Import", "", "Qt Style Sheet (*.qss)")

        if file_name:
            self.controller.set_theme(file_name)

    # Override
    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.save()
        return super().closeEvent(close_event)
