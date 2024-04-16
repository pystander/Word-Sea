import math


class NGram:
    """
    N-gram language model.
    """

    def __init__(self, n: int, vocab_set: set) -> None:
        assert n >= 1

        self.n = n
        self.vocab_set = vocab_set
        self.counter = None

    def tokenize(self, sentence: str) -> list[str]:
        start = ["<START>"] * (self.n - 1) if self.n > 1 else ["<START>"]
        end = ["<END>"] * (self.n - 1) if self.n > 1 else ["<END>"]
        tokens = start + sentence.strip().split() + end

        for i in range(len(tokens)):
            if tokens[i] not in self.vocab_set:
                tokens[i] = "<UNK>"

        return tokens

    def fit(self, train_lines: list[str]) -> None:
        counter = {}

        for line in train_lines:
            tokens = self.tokenize(line)

            for i in range(len(tokens) - self.n + 1):
                token_set = tuple(tokens[i : i + self.n])
                subset = tuple(token_set[:-1])

                if token_set in counter:
                    counter[token_set] += 1
                else:
                    counter[token_set] = 1

                if subset in counter:
                    counter[subset] += 1
                else:
                    counter[subset] = 1

        self.counter = counter

    def get_log_prob(self, token_set: tuple) -> float:
        subset = tuple(token_set[:-1])
        return math.log2(self.counter[token_set] / self.counter[subset])

    def get_perplexity(self, test_lines: list[str]) -> float:
        assert self.counter != None

        log_sum = 0
        N = 0

        for line in test_lines:
            tokens = self.tokenize(line)
            N += len(tokens)

            for i in range(len(tokens) - self.n + 1):
                token_set = tuple(tokens[i : i + self.n])

                if token_set in self.counter:
                    log_sum += self.get_log_prob(token_set)
                else:
                    return float("inf")

        return pow(2, (-1 / N) * log_sum)

    def predict(self, context: tuple) -> str:
        assert self.counter != None

        max_prob = 0
        next_token = "<UNK>"

        for token in self.vocab_set:
            token_set = context + (token, )

            if token_set in self.counter:
                prob = self.counter[token_set] / self.counter[context]

                if prob > max_prob:
                    max_prob = prob
                    next_token = token

        return next_token

    def predict_sequence(self, context: tuple, max_length: int = 50) -> list[str]:
        assert self.counter != None

        tokens = list(context)
        max_length -= len(context)

        for _ in range(max_length):
            next_token = self.predict(tuple(tokens[-self.n + 1 : ]))
            tokens.append(next_token)

        return tokens


class SmoothedNGram(NGram):
    """
    N-gram language model with add-k smoothing.
    """

    def __init__(self, n: int, vocab_set: set) -> None:
        super().__init__(n, vocab_set)

        self.V = len(vocab_set)

    def get_log_prob(self, token_set: tuple, k: float = 0) -> float:
        assert self.counter != None

        subset = tuple(token_set[:-1])

        if token_set in self.counter:
            return math.log2((self.counter[token_set] + k) / (self.counter[subset] + k * self.V))
        else:
            subset_count = 0

            if subset in self.counter:
                subset_count = self.counter[subset]

            return math.log2(k / (subset_count + k * self.V))

    # Override
    def get_perplexity(self, test_lines: list[str], k: float) -> float:
        assert self.counter != None

        log_sum = 0
        N = 0

        for line in test_lines:
            tokens = self.tokenize(line)
            N += len(tokens)

            for i in range(len(tokens) - self.n + 1):
                token_set = tuple(tokens[i : i + self.n])
                log_sum += self.get_log_prob(token_set, k)

        return pow(2, (-1 / N) * log_sum)
