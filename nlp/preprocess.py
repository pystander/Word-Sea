def build_vocab_set(train_lines: list[str], threshold: int = 3) -> set:
    """
    Build vocabulary from corpus.
    """

    counter = {}

    for line in train_lines:
        tokens = line.strip().split()

        for token in tokens:
            if token in counter:
                counter[token] += 1
            else:
                counter[token] = 1

    vocab_set = set()

    for token, count in counter.items():
        if count >= threshold:
            vocab_set.add(token)

    return vocab_set
