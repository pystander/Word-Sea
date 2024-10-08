from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QCheckBox, QListWidget, QListWidgetItem, QStatusBar, QAction, QFileDialog, QMessageBox, QCompleter
from PyQt5.QtGui import QFont, QCloseEvent, QIcon
from playsound import playsound

from api.cambridge import fetch, BASE_URL
from models.vocab.dictionary import Vocabulary
from windows.window import Window


if TYPE_CHECKING:
    from app import WindowController


class DictionaryWindow(Window):
    """
    A window for searching words in the dictionary. Act as the main window.
    """

    def __init__(self, controller: "WindowController", window_id="dict") -> None:
        super(DictionaryWindow, self).__init__(controller, window_id)
        uic.loadUi("ui/dictionary.ui", self)

        # Widgets
        self.line_input = self.findChild(QLineEdit, "line_input")
        self.button_search = self.findChild(QPushButton, "button_search")
        self.button_clear = self.findChild(QPushButton, "button_clear")
        self.button_remove = self.findChild(QPushButton, "button_remove")
        self.checkbox_learn = self.findChild(QCheckBox, "checkbox_learn")
        self.list_cluster = self.findChild(QListWidget, "list_cluster")
        self.status_bar = self.findChild(QStatusBar, "status_bar")

        self.line_input.returnPressed.connect(self.search)
        self.button_search.clicked.connect(self.search)
        self.button_clear.clicked.connect(self.clear)
        self.button_remove.clicked.connect(self.remove)

        self.completer = QCompleter(self.controller.dict.get_words())
        self.line_input.setCompleter(self.completer)
        self.list_cluster.itemClicked.connect(self.play_audio)

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
        self.action_flashcard = self.findChild(QAction, "action_flashcard")
        self.action_import_qss = self.findChild(QAction, "action_import_qss")

        self.action_theme_default.triggered.connect(lambda: self.controller.set_theme(""))
        self.action_theme_dark.triggered.connect(lambda: self.controller.set_theme("ui/qss/dark.qss"))
        self.action_list.triggered.connect(lambda: self.controller.create_window("list"))
        self.action_flashcard.triggered.connect(lambda: self.controller.create_window("flashcard"))
        self.action_import_qss.triggered.connect(lambda: self.import_qss())

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
            pronunciation = cluster.pronunciation
            meanings = cluster.meanings
            examples = cluster.examples
            synonyms = cluster.synonyms
            antonyms = cluster.antonyms
            related = cluster.related
            audio_source = cluster.audio_source

            item = QListWidgetItem()

            cluster_text = pos + "\n" + pronunciation + "\n"

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
            item.setData(Qt.UserRole, audio_source)
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
        self.status_bar.showMessage("File saved to %s" % self.controller.dict_path)

    def save_as(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("csv")
        file_name, _ = dialog.getSaveFileName(self, "Save", "", "CSV (*.csv)")

        if file_name:
            self.controller.dict.to_csv(file_name)
            self.controller.dict_path = file_name
            self.status_bar.showMessage("File saved to %s" % file_name)

    def reset(self) -> None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Reset")
        msg_box.setWindowIcon(QIcon("ui/icons/fluent-emoji-flat--broom"))
        msg_box.setText("Are you sure you want to reset the dictionary?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setWindowFlags(Qt.WindowStaysOnTopHint)

        if msg_box.exec() == QMessageBox.No:
            return

        self.controller.dict.reset()
        self.status_bar.showMessage("Dictionary reset")

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
            self.show_status("QSS imported")

    def show_status(self, message: str) -> None:
        self.status_bar.showMessage(message)

    def play_audio(self, item: QListWidgetItem) -> None:
        audio_source = item.data(Qt.UserRole)

        if audio_source != None:
            playsound(BASE_URL + audio_source)

    # Override
    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.save()
        return super().closeEvent(close_event)
