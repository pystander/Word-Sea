import requests
from bs4 import BeautifulSoup

BASE_URL = "https://dictionary.cambridge.org/dictionary/english/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}

def fetch(word: str) -> dict:
    res = requests.get(BASE_URL + word, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    dict = {}

    # Only include definitions from the first dictionary
    dictionary = soup.find("div", class_="pr dictionary")
    entries = dictionary.find_all("div", class_="pr entry-body__el")

    for entry in entries:
        pos_header = entry.find("div", class_="pos-header dpos-h")
        pos = pos_header.find("span", class_="pos dpos").text
        gram = pos_header.find("span", class_="gram dgram")

        if gram != None:
            pos += " " + gram.text

        def_blocks = entry.find_all("div", class_="def-block ddef_block")
        meanings = []
        examples = []

        for def_block in def_blocks:
            ddef = def_block.find("div", class_="def ddef_d db").text
            dexamps = def_block.find_all("div", class_="examp dexamp")

            meanings.append(ddef)

            for dexamp in dexamps:
                examples.append(dexamp.text)

        dict[pos] = {
            "meanings": meanings,
            "examples": examples
        }

    return dict

if __name__ == "__main__":
    result = fetch("test")
    print(result)
