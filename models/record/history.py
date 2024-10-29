from typing import Tuple
from collections import deque

from models.vocab.dictionary import Vocabulary
from models.record.action import Action

HISTORY_LEN = 5


class History:
    """
    A class for storing the history of actions.
    """

    def __init__(self) -> None:
        self.records = deque[Tuple[Action, Vocabulary]](maxlen=HISTORY_LEN)

    def add(self, action: Action, vocab: Vocabulary) -> None:
        self.records.append((action, vocab))

    def pop(self) -> Tuple[Action, Vocabulary] | None:
        if not self.records:
            return None

        return self.records.pop()
