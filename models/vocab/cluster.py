class Cluster:
    """
    The basic unit of definitions and info of a word.
    """

    def __init__(self, pronunciation: str = "", meanings: list[str] = [], examples: list[str] = [], synonyms: list[str] = [], antonyms: list[str] = [], related: list[str] = []) -> None:
        self.pronunciation = pronunciation
        self.meanings = meanings
        self.examples = examples
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.related = related

    def add_meaning(self, meaning: str) -> None:
        self.meanings.append(meaning)

    def add_example(self, example: str) -> None:
        self.examples.append(example)

    def add_synonym(self, synonym: str) -> None:
        self.synonyms.append(synonym)

    def add_antonym(self, antonym: str) -> None:
        self.antonyms.append(antonym)

    def add_related(self, related: str) -> None:
        self.related.append(related)
