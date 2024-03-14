import json
from bs4 import BeautifulSoup

import config

class DocumentIdentifier():

    def __init__(self):
        self.documents = {}

    # Sets document id to dictionary
    def set_document_id(self, url, id):
        if (url in self.documents.values()):
            keys = list(self.documents.keys())
            vals = list(self.documents.values())
            pos = vals.index(url)
            return keys[pos]
        elif (id not in self.documents.keys()):
            self.documents[id] = url
        else:
            config.log("DOCUMENT ID ERROR", id, url)

        return id
        

    # Returns document id
    def get_document_id(self, url):
        pass
    
    # Returns document url
    def get_document_id(self, id):
        return self.documents[id]
    
    # Exports corresponding urls and ids to json file
    def export(self):
        with open("ids.json", "w") as file:
            json.dump(self.documents, file, indent=4)