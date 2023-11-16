import json
from collections import defaultdict
from typing import Dict, Any

from documents import DocumentStore, DictDocumentStore, Document
from index import BaseIndex
from tokenizer import tokenize


def preprocess_query(query_str: str) -> list[str]:
    return tokenize(query_str)


class FullDocumentsOutputFormatter:
    def format_out(self, results: list[str], document_store: DocumentStore, unused_processed_query):
        output_string = ''
        for doc_id in results:
            doc = document_store.get_by_doc_id(doc_id)
            output_string += f'({doc.doc_id}) {doc.text}\n\n'
        return output_string


class DocIdsOnlyFormatter:
    def format_out(self, results: list[str], document_store: DocumentStore, unused_processed_query):
        return results


def format_out(results: list[str], document_store: DocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


class QueryProcess:
    def __init__(self, document_store: DocumentStore, index: BaseIndex, stopwords: set[str] = None,
                 output_formatter=FullDocumentsOutputFormatter()):
        self.document_store = document_store
        self.index = index
        self.stopwords = stopwords
        self.output_formatter = output_formatter

    # returns a dictionary of the terms along with their synonyms in a dictionary
    def read(self: str):
        # a dictionary that holds a term as a key and its synonyms as its values form the file
        thesaurus = dict()
        with open(self) as fp:
            for line in fp:
                record = json.loads(line)
                thesaurus[record['term']] = record['syns']
        # result = list(thesaurus.items())[:100]
        # print(result)
        return thesaurus
    
    
    def expandQueries(query, thesaurus):
        # Representation for the queries called 'querySyns'
        querySyns = {}
        terms = query.split()
        #Iterate through each term and add synonyms to querySyns
        
        for term in terms:
            synonyms = thesaurus.get(term, [])
            # Add the term itself to the list of synonyms for completeness
            querySyns[term] = [term] + synonyms
            return querySyns 
        
    
   

    def search(self, querySyns: dict, number_of_results: int) -> str:
        doc_IDs = []

        for term, synonyms in querySyns.items():
            if self.stopwords is None:
                processed_query = preprocess_query(term + synonyms)
            else:
                processed_query = [term for term in preprocess_query(term + synonyms)
                               if term not in self.stopwords]
        results = self.index.search(processed_query, number_of_results)
        doc_IDs.extend(results)
        return self.output_formatter.format_out(doc_IDs, self.document_store, processed_query)



