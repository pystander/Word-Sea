import os
import csv

from utils.search import bisect_left


class Cluster:
    """
    The basic unit of definition(s) and info of a word.
    """

    def __init__(self, meanings: list[str] = [], examples: list[str] = [], synonyms: list[str] = [], antonyms: list[str] = [], related: list[str] = []) -> None:
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


class Vocabulary:
    """
    A word defined by Cluster(s).
    """

    def __init__(self, word: str = "") -> None:
        self.word = word
        self.clusters = {}

    def __gt__(self, other) -> bool:
        return self.word > other.word

    def __lt__(self, other) -> bool:
        return self.word < other.word

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vocabulary):
            return False

        return self.word == other.word

    def __hash__(self) -> int:
        return hash(self.word)

    def add_cluster(self, pos: str, cluster: Cluster) -> None:
        self.clusters[pos] = cluster

    def get_cluster(self, pos: str) -> Cluster | None:
        return self.clusters.get(pos, None)

    def get_size(self) -> int:
        return len(self.clusters)


class Dictionary:
    """
    A collection of Vocabulary(s).
    """

    def __init__(self) -> None:
        self.vocabs = {}

    def __len__(self) -> int:
        return len(self.vocabs)

    def add_vocab(self, vocab: Vocabulary) -> None:
        self.vocabs[vocab.word] = vocab

    def remove_word(self, word: str) -> None:
        del self.vocabs[word]

    def clear(self) -> None:
        self.vocabs.clear()

    def get_vocab(self, word: str) -> Vocabulary | None:
        return self.vocabs.get(word, None)

    def get_vocabs(self) -> list[Vocabulary]:
        return [self.vocabs[word] for word in self.vocabs]

    def get_vocabs_by_prefix(self, prefix: str) -> list[Vocabulary]:
        words = list(self.vocabs.keys())

        if prefix == "":
            return [self.vocabs[word] for word in words]

        left = bisect_left(words, prefix)
        right = bisect_left(words, prefix[:-1] + chr(ord(prefix[-1]) + 1))

        return [self.vocabs[word] for word in words[left:right]]

    def get_words(self) -> list[str]:
        return [word for word in self.vocabs]

    def sort(self) -> None:
        self.vocabs = dict(sorted(self.vocabs.items()))

    def to_csv(self, path: str, delim: str = "|") -> None:
        with open(path, "w+", newline="") as f:
            fields = ["word", "pos", "meanings", "examples", "synonyms", "antonyms", "related"]
            writer = csv.writer(f, fields)

            for word in self.vocabs:
                vocab = self.vocabs[word]

                for pos, cluster in vocab.clusters.items():
                    meanings = delim.join(cluster.meanings)
                    examples = delim.join(cluster.examples)
                    synonyms = delim.join(cluster.synonyms)
                    antonyms = delim.join(cluster.antonyms)
                    related = delim.join(cluster.related)

                    writer.writerow([word, pos, meanings, examples, synonyms, antonyms, related])

    def from_csv(self, path: str, delim: str = "|") -> None:
        if not os.path.exists(path):
            return

        with open(path, "r", newline="") as f:
            reader = csv.reader(f)

            for row in reader:
                word, pos, meanings, examples, synonyms, antonyms, related = row
                meanings = meanings.split(delim)
                examples = examples.split(delim)
                synonyms = synonyms.split(delim)
                antonyms = antonyms.split(delim)
                related = related.split(delim)

                vocab = self.get_vocab(word)

                if vocab == None:
                    vocab = Vocabulary(word)

                vocab.add_cluster(pos, Cluster(meanings, examples, synonyms, antonyms, related))
                self.add_vocab(vocab)
