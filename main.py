import os
import time

import json
from bs4 import BeautifulSoup
import re
from threading import Thread
from threading import Lock

import config
from query import Query
from preprocess import Preprocess
from partialindex import PartialIndex
from documentidentifier import DocumentIdentifier
from invertedindex import InvertedIndex

#import summarize

if __name__ == "__main__":

    option = input("Choose: ")

    if (option == "abc"):
        inverted_index = InvertedIndex()
        config.log("Start merging files")

        inverted_index.split_invertedindex("invertedindex.json")

    elif (option == "merge"):
        inverted_index = InvertedIndex()
        config.log("Start merging files")

        # Merging partial indexes into inverted index
        partition_files = Preprocess.get_files(config.partitions_path)
        inverted_index.merge_partial_indexes(partition_files)
        inverted_index.export("invertedindex.json")
        inverted_index.split_invertedindex("invertedindex.json")

        config.log("Finished merging files", len(inverted_index.merged_indexes))

    elif (option == "index"):
        config.log("Starting inverted index")

        # Inititalize necessary modules

        # commenting this and initializing it globally to use in the query process
        inverted_index = InvertedIndex()
        document_identifier = DocumentIdentifier()
        dev_files = Preprocess.get_files(config.dev_path)

        # Create threads
        partial_indexes = []
        threads = []
        lock = Lock()
        for i in range(config.threads):
            partial_indexes.append(PartialIndex())
            threads.append(Thread(target=inverted_index.run, args=(document_identifier, partial_indexes[i], dev_files, i, lock)))
            threads[i].start()
        for thread in threads:
            thread.join()

        # Exports all urls corresponding to document ids
        document_identifier.export()

        config.log("Finished inverted index")
    
    elif (option == "query"):
        '''
        "hepatocellular": {
            "1541": 1,
            "47504": 6,
            "48900": 6,
            "49453": 4
        },

        "themefish": {
            "763": 1,
            "24043": 1,
            "28980": 1,
            "51395": 1,
            "51394": 1,
            "51393": 1
        },
        "pooja": {
            "1541": 2,
            "5649": 1,
            "24043": 1,
            "28980": 1,
            "32023": 1,
            "51394": 1,
            "51393": 1,
            "51395": 1
        },
        '''
        query = Query(f"{config.indexes_path}A.json", "ids.json")   
        option = input("Search for: ")

        while (True):
            try:
                option = query.parse_query(option)
                pages = query.get_top_ten()

                # pages = query.get_pages(option)
                # print(pages[:5])
                # result = [(query.ids[page[0]], page[1]) for page in pages][:5]
                
                # print(result)
                for i in pages:
                    print(i)
            except:
                print("error")
            
            option = input("Search for: ")

    elif (option == "summarize"):
        pass
        #summarize.summarize()
