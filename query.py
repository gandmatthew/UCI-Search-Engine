import json
import nltk
import math
from preprocess import Preprocess
from nltk.stem import PorterStemmer
import config
import os

stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']


class Query():
    def __init__(self, inverted_index=f"{config.indexes_path}A.json", document_ids="ids.json"):
        self.words_files = {letter: open(config.indexes_path + letter.upper() + ".json") for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

        w = open(inverted_index)
        i = open(document_ids)

        self.words = {}
        self.ids = json.load(i)
        self.query = ''

        self.ps = PorterStemmer()

    def parse_input(self, i):
        return i.split(" ")
    
    def find_match(self, pages):
        result = pages.pop()
        while (pages):
            a = 0
            b = 0
            index_b = pages.pop()
            temp = []
            while a != len(result) and b != len(index_b):
                if int(result[a][0]) < int(index_b[b][0]):
                    a += 1
                elif int(index_b[b][0]) < int(result[a][0]):
                    b += 1
                else:
                    temp.append((result[a][0], result[a][1] + index_b[b][1]))
                    a += 1
                    b += 1
            result = temp

        return result
    
    def look_in_indexes(self, word):
        """
            "zultak": {
            "49537": 1
            },
        """
        first_letter = word[0].lower()
        
        file_obj = self.words_files.get(first_letter.upper())
        if file_obj is None:
            print("File not found")
            return None

        file = file_obj  # Assign file_obj to file variable
        index = json.load(file)
        file.seek(0)  # Reset the file pointer to the beginning for future reads
        if word in index:
            self.words.update({word : index[word]})
            return index[word]
        else:
            return None

    # Gets matching word from inverted index
    def get_word(self, word):
        results = []
        #if (word in self.words.keys()):
        if (self.look_in_indexes(word)):
            # Sorts by pages greatest to least for simple intersection
            results = sorted(self.words[word].items(), key=lambda x : x[0])
        return results
    
    # Returns pages containing words
    def get_pages(self, args):
        pages = []
        for arg in args:
            a = self.ps.stem(arg)
            pages.append(self.get_word(a))
        return pages

    def intersect_pages(self, pages):
        # Sorts results list length of least to greatest for simple intersection
        pages = sorted(pages, key=lambda x : len(x), reverse=False)
        result = sorted(self.find_match(pages), key=lambda x : x[1], reverse=True)
        return result
    
    def parse_query(self, query):
        query = self.parse_input(query)
        query_no_sw = [word for word in query if word not in stopwords]

        if len(query_no_sw) < 1:
            self.query = query
            return query
        else:
            self.query = query_no_sw
            return query_no_sw
        

    def compute_tf_idf(self, current_page, total_files):
        score = 0
        for word in self.query:
            try:
                tf = self.words[word][current_page]
                df = len(self.words[word].keys())
                tf_idf = (1 + math.log10(tf)) * (math.log10(total_files / df))
                score += tf_idf
            except KeyError:
                continue
        return score

    def get_top_ten(self):
        # total_files = len(Preprocess.get_files())
        total_files = 55000
        relevant_pages = set()
        tf_idf_scores = dict()
        # print([x for x in self.get_pages('pooja')])
        '''
            "glvlsi": {
            "51351": 1,
            "5021": 2,
            "5060": 2
            },
        '''
        for word in self.query:
            #pages = set(self.words[self.ps.stem(word)].keys())
            pages = set(self.look_in_indexes(self.ps.stem(word)))
            relevant_pages.update(pages)

        while (len(relevant_pages) != 0):
            page = relevant_pages.pop()
            tf_idf_scores[page] = self.compute_tf_idf(page, total_files)

        tf_idf_scores = dict(sorted(tf_idf_scores.items(), key=lambda x: (x[1], x[0]), reverse=True))
        top_ten = {}
        for i, key in enumerate(tf_idf_scores.keys()):
            if i >= 10:
                break
            top_ten[self.ids[key]] = key
        return top_ten
        