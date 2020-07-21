from collections import Counter
from src.NewsGroup.Utils import flatten


class TopSelector:
    def __init__(self, count_features):
        self.count_features = count_features

    def __call__(self, values_by_doc):
        items = flatten(values_by_doc)

        frequencies = []
        top_entities = []

        counter = Counter()
        counter.update(items)
        for element, frequency in counter.most_common(self.count_features):
            frequencies.append(frequency)
            top_entities.append(element)

        return top_entities
