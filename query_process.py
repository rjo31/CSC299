from documents import ListDocumentStore
from index import Index


def preprocess_query(query_str: str):
    return query_str.lower().split()


def format_out(results: list[str], document_store: ListDocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


def query_process(document_store: ListDocumentStore, index: Index, query: str, number_of_results: int) -> str:
    processed_query = preprocess_query(query)
    results = index.search(processed_query, number_of_results)
    return format_out(results, document_store, processed_query)
