import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from dict.dictionary import Vocabulary, Dictionary
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

        self.menu = self.findChild(QMenuBar, "menu")
        self.open_action = self.findChild(QAction, "open_action")
        self.save_action = self.findChild(QAction, "save_action")
        self.save_as_action = self.findChild(QAction, "save_as_action")
        self.view_action = self.findChild(QAction, "view_action")

        self.word_input.returnPressed.connect(self.search)
        self.search_button.clicked.connect(self.search)

        self.open_action.triggered.connect(self.open)
        self.save_action.triggered.connect(self.save)
        self.save_as_action.triggered.connect(self.save_as)
        self.view_action.triggered.connect(self.view)

        self.save_action.setShortcut("Ctrl+S")

        self.completer = QCompleter(self.dict.get_words())
        self.word_input.setCompleter(self.completer)

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

class ViewUI(QMainWindow):
    def __init__(self, dict_ui: DictionaryUI) -> None:
        super(ViewUI, self).__init__()
        uic.loadUi("ui/view.ui", self)

        self.vocab_ui = None

        self.words = dict_ui.dict.get_words()
        self.vocabs = dict_ui.dict.vocabs

        self.word_input = self.findChild(QLineEdit, "word_input")
        self.search_button = self.findChild(QPushButton, "search_button")
        self.vocab_list = self.findChild(QListWidget, "vocab_list")

        self.word_input.returnPressed.connect(self.search)
        self.search_button.clicked.connect(self.search)
        self.vocab_list.itemDoubleClicked.connect(self.view_vocab)

        self.completer = QCompleter(self.words)
        self.word_input.setCompleter(self.completer)

        for vocab in self.vocabs:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, vocab)
            item.setText(vocab.word)
            self.vocab_list.addItem(item)

    def search(self) -> None:
        # TODO: Implement search
        raise NotImplementedError

    def view_vocab(self, item: QListWidgetItem):
        vocab = item.data(Qt.UserRole)

        if self.vocab_ui != None:
            self.vocab_ui.close()

        self.vocab_ui = VocabularyUI(vocab)
        self.vocab_ui.show()

class VocabularyUI(QMainWindow):
    def __init__(self, vocab: Vocabulary):
        super(VocabularyUI, self).__init__()
        uic.loadUi("ui/vocabulary.ui", self)

        self.clusters = vocab.clusters

        self.word_label = self.findChild(QLabel, "word_label")
        self.cluster_list = self.findChild(QListWidget, "cluster_list")

        self.word_label.setText(vocab.word)

        for pos, cluster in self.clusters.items():
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DictionaryUI()
    window.show()

    sys.exit(app.exec_())
