import requests
import re

from bs4 import BeautifulSoup

from models.dictionary import Cluster, Vocabulary

BASE_URL = "https://dictionary.cambridge.org/dictionary/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}


def fetch(search_word: str, trans: str = "english") -> Vocabulary | None:
    """
    Fetch and parse info of a word into Vocabulary from Cambridge Dictionary.
    """

    try:
        res = requests.get(BASE_URL + trans + "/" + search_word, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        # Only include definitions from the first dictionary
        dictionary = soup.find("div", class_="dictionary")

        if dictionary is None:
            dictionary = soup.find("div", class_="entry-body")

        entries = dictionary.find_all("div", class_="entry-body__el")
        vocab = Vocabulary(search_word)

        for entry in entries:
            word = entry.find("div", class_="di-title").text

            if word != search_word:
                vocab.word = word

            pos = entry.find("span", class_="pos dpos").text
            gram = entry.find("span", class_="gram dgram")

            if gram is not None:
                pos += " " + gram.text

            meanings = []
            examples = []
            synonyms = []
            antonyms = []
            related = []

            xref_synonym = entry.find("div", class_=re.compile("^xref synonym "))
            xref_synonyms = entry.find("div", class_=re.compile("^xref synonyms "))
            xref_opposite = entry.find("div", class_=re.compile("^xref opposite "))
            xref_see = entry.find("div", class_=re.compile("^xref see "))
            xref_see_also = entry.find("div", class_=re.compile("^xref see_also "))
            xref_compare = entry.find("div", class_=re.compile("^xref compare "))
            xref_related = entry.find("div", class_=re.compile("^xref related "))
            xref_related_word = entry.find("div", class_=re.compile("^xref related_word "))

            if xref_synonym != None:
                syn = xref_synonym.find("span", class_="x-h dx-h")
                synonyms.append(syn.text)

            if xref_synonyms != None:
                syns = xref_synonyms.find_all("span", class_="x-h dx-h")

                for syn in syns:
                    synonyms.append(syn.text)

            if xref_opposite != None:
                ants = xref_opposite.find_all("span", class_="x-h dx-h")

                for ant in ants:
                    antonyms.append(ant.text)

            if xref_see != None:
                sees = xref_see.find_all("span", class_="x-h dx-h")

                for see in sees:
                    related.append(see.text)

            if xref_see_also != None:
                see_alsos = xref_see_also.find_all("span", class_="x-h dx-h")

                for see_also in see_alsos:
                    related.append(see_also.text)

            if xref_compare != None:
                compares = xref_compare.find_all("span", class_="x-h dx-h")

                for compare in compares:
                    related.append(compare.text)

            if xref_related != None:
                rels = xref_related.find_all("span", class_="x-h dx-h")

                for rel in rels:
                    related.append(rel.text)

            if xref_related_word != None:
                related_words = xref_related_word.find_all("span", class_="x-h dx-h")

                for related_word in related_words:
                    related.append(related_word.text)

            def_blocks = entry.find_all("div", class_=re.compile("^def-block ddef_block"))

            for def_block in def_blocks:
                ddef = def_block.find("div", class_="def ddef_d db")
                dexamp = def_block.find("div", class_="examp dexamp")

                if ddef:
                    meanings.append(ddef.text.lstrip().rstrip(": ").replace("\n", ""))

                if dexamp:
                    examples.append(dexamp.text.lstrip().rstrip(": ").replace("\n", ""))

            vocab.add_cluster(pos, Cluster(meanings, examples, synonyms, antonyms, related))

        return vocab

    except Exception as e:
        return None
