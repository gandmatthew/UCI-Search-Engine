import os
import re
import json
from bs4 import BeautifulSoup
import config

class Preprocess():
    def __init__(self):
        pass

    # Recursively gets files in specified folder
    @staticmethod
    def get_files(folder):
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == '.json']
        return result
    
    # Validate html
    @staticmethod
    def is_valid_HTML(content):
        pass

    # Parses json file, use beautiful soup, returns two items: words and url
    @staticmethod
    def parse_and_tokenize_json(json_file, stemmer):
        f = open(json_file)
        file = json.load(f)
        Preprocess.is_valid_HTML(file["content"])
        url = file["url"].split('#')[0]
        # xml library provides a check for broken html tags
        soup = BeautifulSoup(file["content"], features='xml')
        words = Preprocess.tokenize(soup.text, stemmer)
        f.close()
        return {"words" : words, "url": url}

    # Tokenization, lowers text and removes numbers, returns list of tokens
    @staticmethod
    def tokenize(text, stemmer):
        text = text.lower()
        result = []
        tokens = re.split("[^a-zA-Z]", text)
        for token in tokens:
            if (token != ''):
                result.append(token)
        result = [stemmer.stem(w) for w in result]
        return result
    
    