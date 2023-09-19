from dict import Vocabulary, Dictionary
import json

def parse_dict(dict: Dictionary) -> dict:
    json_dict = {}
    vocabs = dict.vocabs

    for word in vocabs:
        json_dict[word] = vocabs[word].meanings

    return json_dict

def save_dict(dict: Dictionary, path: str) -> None:
    json_dict = parse_dict(dict)

    with open(path, 'w') as f:
        json.dump(json_dict, f, indent=4)

    print("Saved dictionary to %s" % path)

def load_dict(path: str) -> Dictionary:
    with open(path, 'r') as f:
        json_dict = json.load(f)

    dict = Dictionary()

    for word in json_dict:
        vocab = Vocabulary(word)

        for pos in json_dict[word]:
            for meaning in json_dict[word][pos]:
                vocab.add_meaning(pos, meaning)

        dict.add_vocab(vocab)

    print("Loaded dictionary from %s" % path)

    return dict
