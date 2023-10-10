from documents import TransformedDocument



def count_terms(list_terms):
    result = dict()
    for item in list_terms:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1
    return result


def combine_term_scores(list_terms, dict_terms):
    result = 0
    for item in list_terms:
        if item in dict_terms:
            result += dict_terms[item]
    return result


class Index:
    def __init__(self):
        self.id_to_terms_counts = dict()

    def add_document(self, doc: TransformedDocument):
        self.id_to_terms_counts[doc.doc_id] = count_terms(doc.terms)

    def search(self, processed_query: list[str], result_count: int) -> list[str]:

        results = dict()

        for doc_id in self.id_to_terms_counts:
            score = combine_term_scores(processed_query, self.id_to_terms_counts)
            results[doc_id] = score

        sorted_list = sorted(results, key=results.get, reverse=True)[:result_count]

        return sorted_list
