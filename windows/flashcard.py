from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

from models.dictionary import Vocabulary
from models.flashcard import FlashCard

if TYPE_CHECKING:
    from app import WindowController


class FlashCardWindow(QMainWindow):
    def __init__(self, controller: "WindowController", window_id="flashcard") -> None:
        super(FlashCardWindow, self).__init__()
        uic.loadUi("ui/flashcard.ui", self)

        self.controller = controller
        self.window_id = window_id

        self.flashcard = FlashCard(self.controller.dict)

        # Widgets
        self.button_learn = self.findChild(QPushButton, "button_learn")
        self.button_unlearn = self.findChild(QPushButton, "button_unlearn")
        self.list_cluster = self.findChild(QListWidget, "list_cluster")
        self.progress_learned = self.findChild(QProgressBar, "progress_learned")

        self.button_learn.clicked.connect(lambda: self.progress(True))
        self.button_unlearn.clicked.connect(lambda: self.progress(False))

        self.progress_learned.setRange(0, len(self.flashcard.learning))
        self.progress_learned.setValue(0)

        # Window settings
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def progress(self, is_learn: bool) -> None:
        vocab = self.flashcard.get_next_vocab()
        self.show_vocab(vocab)

        if is_learn:
            self.flashcard.learn(vocab)
        else:
            self.flashcard.unlearn(vocab)

        if self.flashcard.is_completed:
            self.controller.close_window(self.window_id)

        self.update_progress_bar()

    def update_progress_bar(self) -> None:
        self.progress_learned.setValue(len(self.flashcard.learned))

    def show_vocab(self, vocab: "Vocabulary") -> None:
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
