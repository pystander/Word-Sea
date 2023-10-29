import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMenuBar, QAction, QCompleter
from dict import *

class DictionaryUI(QMainWindow):
    def __init__(self) -> None:
        super(DictionaryUI, self).__init__()
        uic.loadUi("ui/dictionary.ui", self)

        self.dict = Dictionary()
        self.dict.read_json("data/test.json")

        self.word_input = self.findChild(QLineEdit, "word_input")
        self.search_button = self.findChild(QPushButton, "search_button")
        self.cluster_list = self.findChild(QListWidget, "cluster_list")
        self.menu = self.findChild(QMenuBar, "menu")

        self.search_button.clicked.connect(self.search)

        completer = QCompleter(self.dict.get_words())
        self.word_input.setCompleter(completer)

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

            cluster_text = pos + "\n"

            for i, meaning in enumerate(meanings):
                cluster_text += "%d. %s" % (i + 1, meaning) + "\n"

            cluster_text += "\n" + "Examples:" + "\n"

            for example in examples:
                cluster_text += "    " + "- %s" % example + "\n"

            cluster_text += "\n" + "Synonyms: " + ', '.join(synonyms) + "\n"
            cluster_text += "\n" + "Related: " + ', '.join(related) + "\n"

            item.setText(cluster_text)
            self.cluster_list.addItem(item)

    def save_dict(self, path: str) -> None:
        try:
            self.dict.to_json(path)
        except:
            print("[Error] Failed to save dictionary.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DictionaryUI()
    window.show()

    sys.exit(app.exec_())
