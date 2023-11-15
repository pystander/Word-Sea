import json

class Cluster:
    """
    The basic unit of definition(s) and info of a word.
    """

    def __init__(self, meanings: list[str] = [], examples: list[str] = [], synonyms: list[str] = [], related: list[str] = []) -> None:
        self.meanings = meanings
        self.examples = examples
        self.synonyms = synonyms
        self.related = related

    def add_meaning(self, meaning: str) -> None:
        self.meanings.append(meaning)

    def add_example(self, example: str) -> None:
        self.examples.append(example)

    def add_synonym(self, synonym: str) -> None:
        self.synonyms.append(synonym)

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

    def add_cluster(self, pos: str, cluster: Cluster) -> None:
        self.clusters[pos] = cluster

    def get_size(self) -> int:
        return len(self.clusters)

class Dictionary:
    """
    A collection of Vocabulary(s).
    """

    def __init__(self) -> None:
        self.vocabs = {}

    def add_vocab(self, vocab: Vocabulary) -> None:
        self.vocabs[vocab.word] = vocab

    def get_vocab(self, word: str) -> Vocabulary | None:
        return self.vocabs.get(word, None)

    def get_vocabs_by_prefix(self, prefix: str) -> list[Vocabulary]:
        return [self.vocabs[word] for word in self.vocabs if word.startswith(prefix)]

    def get_words(self) -> list[str]:
        return [word for word in self.vocabs]

    def read_json(self, path: str) -> None:
        with open(path, "r") as f:
            data = json.load(f)

        for word, cluster_dict in data.items():
            vocab = Vocabulary(word)

            for pos, cluster in cluster_dict.items():
                meanings = cluster["meanings"]
                examples = cluster["examples"]
                synonyms = cluster["synonyms"]
                related = cluster["related"]

                vocab.add_cluster(pos, Cluster(meanings, examples, synonyms, related))

            self.add_vocab(vocab)

    def to_json(self, path) -> None:
        data = {}

        for word in self.vocabs:
            cluster_dict = {}

            for pos, cluster in self.vocabs[word].clusters.items():
                cluster_dict[pos] = {
                    "meanings": cluster.meanings,
                    "examples": cluster.examples,
                    "synonyms": cluster.synonyms,
                    "related": cluster.related
                }

                data[word] = cluster_dict

        with open(path, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
