import os
import csv

from utils.search import bisect_left
from models.vocab.vocabulary import Cluster, Vocabulary


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

    def reset(self) -> None:
        self.vocabs.clear()

    def to_csv(self, path: str, delim: str = "|") -> None:
        with open(path, "w+", newline="", encoding="utf-8") as f:
            fields = ["word", "pos", "pronunciation", "meanings", "examples", "synonyms", "antonyms", "related", "audio_source"]
            writer = csv.writer(f, fields)

            for word in self.vocabs:
                vocab = self.vocabs[word]

                for pos, cluster in vocab.clusters.items():
                    pronunciation = cluster.pronunciation
                    meanings = delim.join(cluster.meanings)
                    examples = delim.join(cluster.examples)
                    synonyms = delim.join(cluster.synonyms)
                    antonyms = delim.join(cluster.antonyms)
                    related = delim.join(cluster.related)
                    audio_source = cluster.audio_source

                    writer.writerow([word, pos, pronunciation, meanings, examples, synonyms, antonyms, related, audio_source])

    def from_csv(self, path: str, delim: str = "|") -> None:
        if not os.path.exists(path):
            return

        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                word, pos, pronunciation, meanings, examples, synonyms, antonyms, related, audio_source = row
                meanings = meanings.split(delim)
                examples = examples.split(delim)
                synonyms = synonyms.split(delim)
                antonyms = antonyms.split(delim)
                related = related.split(delim)

                vocab = self.get_vocab(word)

                if vocab == None:
                    vocab = Vocabulary(word)

                vocab.add_cluster(pos, Cluster(pronunciation, meanings, examples, synonyms, antonyms, related, audio_source))
                self.add_vocab(vocab)
