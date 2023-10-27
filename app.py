import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMenuBar, QAction, QCompleter
from dict import *
from utils.parse import *

class DictionaryUI(QMainWindow):
    def __init__(self) -> None:
        super(DictionaryUI, self).__init__()
        uic.loadUi("ui/dictionary.ui", self)

        self.dict = read_dict("data/test.json")

        self.word_input = self.findChild(QLineEdit, "word_input")
        self.search_button = self.findChild(QPushButton, "search_button")
        self.cluster_list = self.findChild(QListWidget, "cluster_list")
        self.menu = self.findChild(QMenuBar, "menu")
        self.action_add = self.findChild(QAction, "action_add")

        self.search_button.clicked.connect(self.search)
        self.action_add.triggered.connect(self.show_add_ui)

        completer = QCompleter(self.dict.get_words())
        self.word_input.setCompleter(completer)

    def show_add_ui(self) -> None:
        self.add_ui = AddUI()
        self.add_ui.show()

    def search(self) -> None:
        word = self.word_input.text()
        vocab = self.dict.get_vocab(word)

        if vocab is None:
            return

        self.cluster_list.clear()

        for pos, cluster in vocab.clusters.items():
            meanings = cluster.meanings
            examples = cluster.examples
            synonyms = cluster.synonyms
            related = cluster.related

            item = QListWidgetItem()

            cluster_text = "[%s]" % pos + "\n"

            for i, meaning in enumerate(meanings):
                cluster_text += "%d. %s" % (i + 1, meaning) + "\n"

            for i, example in enumerate(examples):
                cluster_text += "Example %d: %s" % (i + 1, example) + "\n"

            cluster_text += "Synonyms: " + ', '.join(synonyms) + "\n"
            cluster_text += "Related: " + ', '.join(related) + "\n"

            item.setText(cluster_text)
            self.cluster_list.addItem(item)

    # TODO: Parse and save self.dict to path

    # TODO: Open AddUI by action in menu

class AddUI(QMainWindow):
    def __init__(self):
        super(AddUI, self).__init__()
        uic.loadUi("ui/add.ui", self)

        self.pos_input = self.findChild(QLineEdit, "pos_input")
        self.meaning_input = self.findChild(QLineEdit, "meaning_input")
        self.examples_input = self.findChild(QLineEdit, "examples_input")
        self.synonyms_input = self.findChild(QLineEdit, "synonyms_input")
        self.related_input = self.findChild(QLineEdit, "related_input")
        self.add_button = self.findChild(QPushButton, "add_button")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DictionaryUI()
    window.show()

    sys.exit(app.exec_())
