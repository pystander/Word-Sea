from collections import defaultdict

class Vocabulary:
    def __init__(self, word: str) -> None:
        self.word = word
        self.meanings = defaultdict(list[str])

    def add_meaning(self, pos: str, meaning: str) -> str:
        return self.meanings[pos].append(meaning)

    def remove_meaning(self, pos: str, index: int) -> str:
        return self.meanings[pos].pop(index)

class Dictionary:
    def __init__(self) -> None:
        self.vocabs = defaultdict(Vocabulary)

    def add_vocab(self, vocab: Vocabulary) -> None:
        self.vocabs[vocab.word] = vocab
