import json
from dict import *

def read_dict(path: str) -> Dictionary:
    """
    Parse JSON formated string to dictionary.
    """

    with open(path, "r") as f:
        data = json.load(f)
        dict = Dictionary()

        for word, clusters in data.items():
            vocab = Vocabulary(word)

            for cluster in clusters:
                vocab.add_cluster(Cluster(
                    cluster["pos"],
                    cluster["meaning"],
                    cluster["examples"],
                    cluster["synonyms"],
                    cluster["related"]
                ))

            dict.add_vocab(vocab)

        return dict
