import json
from collections import defaultdict
from utils.sorted_list import SortedList

class Cluster:
    """
    The basic unit of definition(s) and info of a word.
    """

    def __init__(self, pos: str, meaning: str, examples: list[str], synonyms: list[str], related: list[str]) -> None:
        self.pos = pos
        self.meaning = meaning
        self.examples = examples
        self.synonyms = synonyms
        self.related = related

class Vocabulary:
    """
    A word defined by Cluster(s).
    """

    def __init__(self, word: str) -> None:
        self.word = word
        self.clusters = []

    def __gt__(self, other) -> bool:
        return self.word > other.word

    def __lt__(self, other) -> bool:
        return self.word < other.word

    def add_cluster(self, cluster: Cluster) -> None:
        self.clusters.append(cluster)

    def get_size(self) -> int:
        return len(self.clusters)

class Dictionary:
    """
    A collection of Vocabulary(s).
    """

    def __init__(self) -> None:
        self.vocabs = SortedList()

    def add_vocab(self, vocab: Vocabulary) -> None:
        self.vocabs.insort(vocab)

    def get_vocab(self, word: str) -> Vocabulary | None:
        left, right = 0, len(self.vocabs) - 1
        mid = right + (left - right) // 2

        while left <= right:
            if self.vocabs[mid].word == word:
                return self.vocabs[mid]
            elif self.vocabs[mid].word < word:
                left = mid + 1
            else:
                right = mid - 1

            mid = right + (left - right) // 2

        return None

    def to_json(self, path) -> None:
        data = defaultdict(list)

        for vocab in self.vocabs:
            for cluster in vocab.clusters:
                data[vocab.word].append({
                    "pos": cluster.pos,
                    "meaning": cluster.meaning,
                    "examples": cluster.examples,
                    "synonyms": cluster.synonyms,
                    "related": cluster.related
                })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)