import json
import config
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import os
import string

from preprocess import Preprocess

class InvertedIndex():

    def __init__(self, stemmer=PorterStemmer()):
        self.stemmer = stemmer
        self.merged_indexes = {}

    # def export_split(self, index):
    #     size = len(os.listdir(config.indexes_path))
    #     with open(f"{config.indexes_path}I{size}.json", "w") as file:
    #         json.dump(index, file, indent=4)
    #         file.close()

    # def split_invertedindex(self, inverted_index="invertedindex.json"):
    #     index = {}
    #     w = open(inverted_index)
    #     words = json.load(w)
    #     for key in words.keys():
    #         if (len(index) >= 1000):
    #             self.export_split(index)
    #             del index
    #             index = {}
    #         else:
    #             index.update({key : words[key]})
                
    #     self.export_split(index)
    
    def export_split(self, indexes):    
        for letter, index in indexes.items():
            if index:  # Only export if the index for the letter is not empty
                with open(f"{config.indexes_path}{letter.upper()}.json", "w") as file:
                    json.dump(index, file, indent=4)

    def split_invertedindex(self, inverted_index="invertedindex.json"):
        indexes = {letter: {} for letter in string.ascii_lowercase}
        w = open(inverted_index)
        words = json.load(w)
        for key in words.keys():
            first_letter = key[0].lower()
            if first_letter in string.ascii_lowercase:
                indexes[first_letter][key] = words[key]

        self.export_split(indexes)

    # Multithreaded function
    def run(self, document_identifier, partial_index, files, tid, lock):

        # Goes through entire file tree and uses length of files as ID
        while (files):
            lock.acquire()
            id = len(files)
            current = files.pop()
            lock.release()
            if (len(files) % 1000 == 0):
                config.log(len(files), " documents")
            
            parsed = Preprocess.parse_and_tokenize_json(current, self.stemmer)
            id = document_identifier.set_document_id(parsed["url"], id)
            for word in parsed["words"]:
                partial_index.add_word(word, id)

        # Export remaining words that may have not met the threshold
        partial_index.export()

    # def merge_partial_indexes(self, files):
    #     result = defaultdict(dict)

    #     for current in files:
    #         try:
    #             with open(current) as f:
    #                 words = json.load(f)
    #                 for word, word_data in words.items():
    #                     for id in word_data:
    #                         result[word][id] = result[word].get(id, 0) + 1
    #                     result[word] = dict(sorted(result[word].items(), key=lambda x: x[1]))
    #         except Exception as e:
    #             config.log(current, f"MERGING ERROR: {e}")
    
    #     self.merged_indexes = result
    def merge_partial_indexes(self, files):
        result = defaultdict(dict)

        for current in files:
            try:
                with open(current) as f:
                    words = json.load(f)
                    for word, word_data in words.items():
                        for id in word_data:
                            result[word][id] = result[word].get(id, 0) + 1
                        result[word] = dict(sorted(result[word].items()))
            except Exception as e:
                config.log(current, f"MERGING ERROR: {e}")
    
        self.merged_indexes = result

    
    def export(self, name):
        with open(name, "w") as file:
            json.dump(self.merged_indexes, file, indent=4)
            file.close()