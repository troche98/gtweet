#!/usr/bin/env python3

import os
import sys
import glob
from whoosh import qparser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import Schema, STORED, ID, TEXT
from whoosh.qparser import QueryParser

class IR:
    def __init__(self):
        self.schema = Schema(company=TEXT(stored=True), tweet=TEXT(stored=True), content=TEXT)
        if not os.path.exists("index"):
            os.mkdir("index")
        create_in("index", self.schema)
        self.ix = open_dir("index")

    #index tweets stored in.txt files
    def addDocuments(self, writer, company_name):
        i = 0
        for filename in glob.glob("./modules/" + company_name + "/*.txt"):
            f = open(filename, "r", encoding='utf-8')
            writer.add_document(company=company_name, tweet=str(i), content=f.read())
            i+=1
    
    #add indexed documents to index folder
    def indexer(self):
        writer = self.ix.writer()
        self.addDocuments(writer, "Amazon")
        self.addDocuments(writer, "Facebook")
        self.addDocuments(writer, "Google")
        self.addDocuments(writer, "Microsoft")
        self.addDocuments(writer, "Netflix")
        self.addDocuments(writer, "Starbucks")
        writer.commit()

    #retrieve the content with most similarity
    def searcher(self, tweet):
        qp = QueryParser("content", schema=self.ix.schema, group=qparser.OrGroup)
        q = qp.parse(tweet)
        s = self.ix.searcher()
        if s.search(q):
            return s.search(q)[0]['company']
        else:
            return "Doesn't match"
        
# if __name__ == '__main__':
#     IR()
def main():
    try:
        i = IR()
        i.indexer()
        i.searcher("Lauren, her daughter Bailey and her son Brody")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()