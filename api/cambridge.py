import requests
from bs4 import BeautifulSoup
from dict import Cluster, Vocabulary

BASE_URL = "https://dictionary.cambridge.org/dictionary/english/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}

def fetch(word: str) -> Vocabulary | None:
    """
    Fetch and parse info of a word into Vocabulary from Cambridge Dictionary.
    """

    res = requests.get(BASE_URL + word, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    # Only include definitions from the first dictionary
    dictionary = soup.find("div", class_="pr dictionary")

    if dictionary == None:
        return None

    vocab = Vocabulary(word)
    entries = dictionary.find_all("div", class_="pr entry-body__el")

    for entry in entries:
        try:
            pos_header = entry.find("div", class_="pos-header dpos-h")

            pos = pos_header.find("span", class_="pos dpos").text
            gram = pos_header.find("span", class_="gram dgram")

            if gram != None:
                pos += " " + gram.text

            def_blocks = entry.find_all("div", class_="def-block ddef_block")

            meanings = []
            examples = []
            synonyms = []
            related = []

            for def_block in def_blocks:
                ddef = def_block.find("div", class_="def ddef_d db")
                dexamps = def_block.find_all("div", class_="examp dexamp")

                meanings.append(ddef.text.lstrip())

                for dexamp in dexamps:
                    examples.append(dexamp.text.lstrip())

                dsyn = def_block.find("div", class_="xref synonyms hax dxref-w lmt-25")
                dsee = def_block.find("div", class_="xref see hax dxref-w lmt-25")
                drelated = def_block.find("div", class_="xref related hax dxref-w lmt-25")

                if dsyn != None:
                    syns = dsyn.find_all("span", class_="x-h dx-h")

                    for syn in syns:
                        synonyms.append(syn.text)

                if dsee != None:
                    sees = dsee.find_all("span", class_="x-h dx-h")

                    for see in sees:
                        related.append(see.text)

                if drelated != None:
                    rels = drelated.find_all("span", class_="x-h dx-h")

                    for rel in rels:
                        related.append(rel.text)

            vocab.add_cluster(pos, Cluster(meanings, examples, synonyms, related))

        except Exception as e:
            print(e)

    return vocab
