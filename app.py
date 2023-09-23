import sys
from PyQt5 import QtWidgets, uic
from dict import *

class DictionaryUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(DictionaryUI, self).__init__()
        uic.loadUi("ui/dictionary.ui", self)

    # TODO: Build and connect events with widgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DictionaryUI()
    window.show()
    sys.exit(app.exec_())
