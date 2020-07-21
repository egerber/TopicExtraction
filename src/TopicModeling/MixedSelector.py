from collections import Counter
from src.NewsGroup.Utils import flatten


class MixedSelector:
    def __init__(self, count_entities, count_tokens):
        self.count_entities = count_entities
        self.count_tokens = count_tokens

    def __call__(self, values_by_doc):
        counter_entities = Counter()
        counter_tokens = Counter()

        flattened_entities = flatten(values_by_doc["linkedEntities"])

        flattened_tokens = flatten(values_by_doc["tokens"])

        counter_entities.update(flattened_entities)
        counter_tokens.update(flattened_tokens)

        top_elements = []
        for element, frequency in counter_entities.most_common(self.count_entities):
            top_elements.append(element)

        for element, frequency in counter_tokens.most_common(self.count_tokens):
            top_elements.append(element)

        return top_elements
