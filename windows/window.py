from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCloseEvent

if TYPE_CHECKING:
    from controllers.window import WindowController


class Window(QMainWindow):
    """
    The base class for all windows.
    """

    def __init__(self, controller: "WindowController", window_id: str) -> None:
        super(Window, self).__init__()

        self.controller = controller
        self.window_id = window_id

    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.controller.close_window(self.window_id)
        return super().closeEvent(close_event)
