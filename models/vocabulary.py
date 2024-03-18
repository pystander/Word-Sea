from models.cluster import Cluster


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

    def __repr__(self) -> str:
        return self.word

    def add_cluster(self, pos: str, cluster: Cluster) -> None:
        self.clusters[pos] = cluster

    def get_cluster(self, pos: str) -> Cluster | None:
        return self.clusters.get(pos, None)

    def get_size(self) -> int:
        return len(self.clusters)
