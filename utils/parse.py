import json
from dict import *

def read_dict(path: str) -> Dictionary:
    """
    Parse JSON formated string to Dictionary object.
    """

    with open(path, "r") as f:
        dict = Dictionary()
        data = json.load(f)

        for word, cluster_dict in data.items():
            vocab = Vocabulary(word)

            for pos, cluster in cluster_dict.items():
                meanings = cluster["meanings"]
                examples = cluster["examples"]
                synonyms = cluster["synonyms"]
                related = cluster["related"]

                vocab.add_cluster(pos, Cluster(meanings, examples, synonyms, related))

            dict.add_vocab(vocab)

        return dict
