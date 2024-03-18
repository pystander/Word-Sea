import random

from models.dictionary import Vocabulary, Dictionary


class FlashCard:
    """
    A model class for revising saved Vocabulary(s).
    """

    def __init__(self, dict: Dictionary) -> None:
        self.learning = set()
        self.learned = set()
        self.is_completed = False
        self.learning_ratio = 0.8

        for vocab in dict.vocabs.values():
            self.learning.add(vocab)

    def get_next_vocab(self) -> Vocabulary:
        if len(self.learning) == 0:
            return None

        if len(self.learned) == 0:
            return random.choice(list(self.learning))

        # Larger learning ratio means higher chance of learning
        rand = random.random()

        if rand <= self.learning_ratio:
            return random.choice(list(self.learning))
        else:
            return random.choice(list(self.learned))

    def learn(self, vocab: Vocabulary) -> None:
        self.learned.add(vocab)
        self.learning.discard(vocab)

        if len(self.learning) == 0:
            self.is_completed = True

    def unlearn(self, vocab: Vocabulary) -> None:
        self.learning.add(vocab)
        self.learned.discard(vocab)
