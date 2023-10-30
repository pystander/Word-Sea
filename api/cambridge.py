import requests
from bs4 import BeautifulSoup

BASE_URL = "https://dictionary.cambridge.org/dictionary/english/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}

def fetch(word: str) -> dict | None:
    res = requests.get(BASE_URL + word, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    dict = {}

    # Only include definitions from the first dictionary
    dictionary = soup.find("div", class_="pr dictionary")
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
                dsyns = def_block.find("div", class_="xref synonym hax dxref-w lmt-25")
                dsee = def_block.find("div", class_="xref see hax dxref-w lmt-25")

                meanings.append(ddef.text.lstrip())

                for dexamp in dexamps:
                    examples.append(dexamp.text.lstrip())

                if dsyns != None:
                    synonyms = dsyns.find("div", class_="item lc lc1 lpb-10 lpr-10").text.split(", ")

                if dsee != None:
                    related = dsee.find("div", class_="item lc lc1 lpb-10 lpr-10").text.split(", ")

            dict[pos] = {
                "meanings": meanings,
                "examples": examples,
                "synonyms": synonyms,
                "related": related
            }

        except Exception as e:
            print(e)

    return dict
