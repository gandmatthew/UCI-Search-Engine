import json
import os

import config

class PartialIndex():

    def __init__(self):
        self.words = {}

    # Add single word, with page id, also checks if threshold has exceeded then exports
    def add_word(self, word, id):
        if (self.get_size() >= config.word_threshold):
            config.log("WORD THRESHOLD REACHED")
            self.export()
        if (word in self.words.keys()):
            self.words[word].append(id)
        else:
            self.words[word] = [id]

    # Returns length of words in the dictionary
    def get_size(self):
        return len(self.words)
    
    # Exports words to json formatted file and deletes items in word list
    def export(self):
        size = len(os.listdir(config.partitions_path))
        with open(f"{config.partitions_path}L{size}.json", "w") as file:
            json.dump(self.words, file, indent=4)
        del self.words
        self.words = {}