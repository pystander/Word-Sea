import sys
from PyQt5 import QtWidgets, uic
from dict import *
from parse import *

class DictionaryUI(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(DictionaryUI, self).__init__()
        uic.loadUi("ui/dictionary.ui", self)

        self.dict = read_dict("test.json")

        self.word_input = self.findChild(QtWidgets.QLineEdit, "word_input")
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.cluster_list = self.findChild(QtWidgets.QListWidget, "cluster_list")
        self.menu = self.findChild(QtWidgets.QMenuBar, "menu")
        self.action_add = self.findChild(QtWidgets.QAction, "action_add")

        self.search_button.clicked.connect(self.search)
        self.action_add.triggered.connect(self.add)

    # TODO: Create and add Vocabulary to self.dict

    def search(self) -> None:
        word = self.word_input.text()
        vocab = self.dict.get_vocab(word)

        if vocab is None:
            return

        self.cluster_list.clear()

        for cluster in vocab.clusters:
            pos = cluster.pos
            meaning = cluster.meaning
            examples = cluster.examples
            synonyms = cluster.synonyms
            related = cluster.related

            item = QtWidgets.QListWidgetItem()

            cluster_text = "[%s]" % pos + "\n"
            cluster_text += "%s" % meaning + "\n"
            cluster_text += "Examples: " + str(examples) + "\n"
            cluster_text += "Synonyms: " + str(synonyms) + "\n"
            cluster_text += "Related: " + str(related) + "\n"

            item.setText(cluster_text)
            self.cluster_list.addItem(item)

    # TODO: Parse and save self.dict to path

    # TODO: Open AddUI by action in menu

class AddUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddUI, self).__init__()
        uic.loadUi("ui/add.ui", self)

        self.pos_input = self.findChild(QtWidgets.QLineEdit, "pos_input")
        self.meaning_input = self.findChild(QtWidgets.QLineEdit, "meaning_input")
        self.examples_input = self.findChild(QtWidgets.QLineEdit, "examples_input")
        self.synonyms_input = self.findChild(QtWidgets.QLineEdit, "synonyms_input")
        self.related_input = self.findChild(QtWidgets.QLineEdit, "related_input")
        self.add_button = self.findChild(QtWidgets.QPushButton, "add_button")

        self.add_button.clicked.connect(self.submit)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DictionaryUI()
    window.show()
    sys.exit(app.exec_())
