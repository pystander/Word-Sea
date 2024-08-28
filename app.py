import sys
import os

from PyQt5.QtWidgets import QApplication

from controllers.window import WindowController

OS_PATH = os.path.dirname(__file__)
DATA_DIR = OS_PATH + "\\data"
DICT_PATH = DATA_DIR + "\\dictionary.csv"
SETTINGS_PATH = DATA_DIR + "\\settings.csv"


if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    app = QApplication(sys.argv)
    controller = WindowController(DICT_PATH, SETTINGS_PATH)
    controller.create_window("dict")

    sys.exit(app.exec_())
