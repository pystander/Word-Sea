import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from dict.dictionary import Dictionary
from api.cambridge import fetch

DICT_PATH = "data/dictionary.json"

class DictionaryUI(QMainWindow):
    def __init__(self) -> None:
        super(DictionaryUI, self).__init__()
        uic.loadUi("ui/dictionary.ui", self)

        self.dict_path = DICT_PATH
        self.view_ui = None

        self.dict = Dictionary()
        self.dict.read_json(DICT_PATH)

        self.word_input = self.findChild(QLineEdit, "word_input")
        self.search_button = self.findChild(QPushButton, "search_button")
        self.cluster_list = self.findChild(QListWidget, "cluster_list")
        self.learn_checkbox = self.findChild(QCheckBox, "learn_checkbox")
        self.top_checkbox = self.findChild(QCheckBox, "top_checkbox")

        self.open_action = self.findChild(QAction, "open_action")
        self.save_action = self.findChild(QAction, "save_action")
        self.save_as_action = self.findChild(QAction, "save_as_action")
        self.view_action = self.findChild(QAction, "view_action")
        self.clear_action = self.findChild(QAction, "clear_action")

        self.open_action.triggered.connect(self.open)
        self.save_action.triggered.connect(self.save)
        self.save_as_action.triggered.connect(self.save_as)
        self.view_action.triggered.connect(self.view)
        self.clear_action.triggered.connect(self.clear)

        self.theme_default_action = self.findChild(QAction, "theme_default_action")
        self.theme_dark_action = self.findChild(QAction, "theme_dark_action")

        self.theme_default_action.triggered.connect(lambda: self.set_theme(""))
        self.theme_dark_action.triggered.connect(lambda: self.set_theme("qss/dark.qss"))

        self.word_input.returnPressed.connect(self.search)
        self.search_button.clicked.connect(self.search)
        self.top_checkbox.stateChanged.connect(self.set_window_flag)

        self.save_action.setShortcut("Ctrl+S")

        self.completer = QCompleter(self.dict.get_words())
        self.word_input.setCompleter(self.completer)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def search(self) -> None:
        word = self.word_input.text()

        if word == "":
            return

        vocab = self.dict.get_vocab(word)

        if vocab == None:
            vocab = fetch(word)

            if vocab == None:
                return

            if self.learn_checkbox.isChecked():
                self.dict.add_vocab(vocab)
                self.completer.model().setStringList(self.dict.get_words())

        self.cluster_list.clear()

        font = QFont()
        font.setBold(True)

        item = QListWidgetItem()
        item.setText(vocab.word)
        item.setFont(font)
        self.cluster_list.addItem(item)

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

            if examples:
                cluster_text += "\n" + "Examples:" + "\n"

                for example in examples:
                    cluster_text += "    " + "- %s" % example + "\n"

            if synonyms:
                cluster_text += "\n" + "Synonyms: " + ', '.join(synonyms) + "\n"

            if antonyms:
                cluster_text += "\n" + "Antonyms: " + ', '.join(antonyms) + "\n"

            if related:
                cluster_text += "\n" + "Related: " + ', '.join(related) + "\n"

            item.setText(cluster_text)
            self.cluster_list.addItem(item)

    def open(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("json")
        file_name, _ = dialog.getOpenFileName(self, "QFileDialog.getSaveFileName()", "", "JSON (*.json)")

        if file_name:
            self.dict = Dictionary()
            self.dict.read_json(file_name)

        self.completer.model().setStringList(self.dict.get_words())

    def save(self) -> None:
        self.dict.to_json(self.dict_path)

    def save_as(self) -> None:
        dialog = QFileDialog()
        dialog.setDefaultSuffix("json")
        file_name, _ = dialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "JSON (*.json)")

        if file_name:
            self.dict.to_json(file_name)
            self.dict_path = file_name

    def view(self) -> None:
        if self.view_ui != None:
            self.view_ui.close()

        self.view_ui = ViewUI(self)
        self.view_ui.show()

    def clear(self) -> None:
        self.dict = Dictionary()
        self.completer = QCompleter(self.dict.get_words())
        self.word_input.setCompleter(self.completer)

    def set_window_flag(self) -> None:
        if self.top_checkbox.isChecked():
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.Window)

        self.show()

    def read_qss(self, path: str) -> str:
        with open(path, "r") as f:
            return f.read()

    def set_theme(self, path: str) -> None:
        if path == "":
            self.setStyleSheet("")

            if self.view_ui != None:
                self.view_ui.setStyleSheet(self.styleSheet())
        else:
            qss = self.read_qss(path)
            self.setStyleSheet(qss)

            if self.view_ui != None:
                self.view_ui.setStyleSheet(qss)

class ViewUI(QMainWindow):
    def __init__(self, dict_ui: DictionaryUI) -> None:
        super(ViewUI, self).__init__()
        uic.loadUi("ui/view.ui", self)

        self.dict_ui = dict_ui
        self.dict = dict_ui.dict

        self.word_input = self.findChild(QLineEdit, "word_input")
        self.search_button = self.findChild(QPushButton, "search_button")
        self.vocab_list = self.findChild(QListWidget, "vocab_list")

        self.word_input.returnPressed.connect(self.search)
        self.word_input.textChanged.connect(self.search)
        self.search_button.clicked.connect(self.search)
        self.vocab_list.itemDoubleClicked.connect(self.view_vocab)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setStyleSheet(dict_ui.styleSheet())

        for word in self.dict.vocabs:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, self.dict.vocabs[word])
            item.setText(word)
            self.vocab_list.addItem(item)

    def view_vocab(self, item: QListWidgetItem) -> None:
        self.dict_ui.word_input.setText(item.text())
        self.dict_ui.search()

    def search(self) -> None:
        word = self.word_input.text()

        if word == "":
            self.reset_list()

        vocabs = self.dict.get_vocabs_by_prefix(word)

        self.vocab_list.clear()

        for vocab in vocabs:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, self.dict.vocabs[vocab.word])
            item.setText(vocab.word)
            self.vocab_list.addItem(item)

    def reset_list(self) -> None:
        self.vocab_list.clear()

        for word in self.dict.vocabs:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, self.dict.vocabs[word])
            item.setText(word)
            self.vocab_list.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DictionaryUI()
    window.show()

    sys.exit(app.exec_())
