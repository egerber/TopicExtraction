from collections import Counter, defaultdict

from src.EntityLinker.Utils import get_entity_name


class EntityCollection:

    def __init__(self, entities):
        self.entities = entities

    def __iter__(self):
        for entity in self.entities:
            yield entity

    def __getitem__(self, item):
        return self.entities[item]

    def __len__(self):
        return len(self.entities)

    def get_categories(self, max_depth=1):
        categories = []
        for entity in self.entities:
            categories += entity.get_categories(max_depth)

        return categories

    def print_categories(self, max_depth=1, limit=10):
        all_categories = []
        category_to_entites = defaultdict(list)

        for e in self.entities:
            for category in e.get_categories(max_depth):
                category_to_entites[category].append(e)
                all_categories.append(category)

        counter = Counter()
        counter.update(all_categories)

        for category, frequency in counter.most_common(limit):
            print("{} ({}) : {}".format(get_entity_name(category), frequency,
                                        ','.join([str(e) for e in category_to_entites[category]])))

    def pretty_print(self):
        for entity in self.entities:
            entity.pretty_print()

    def grouped_by_category(self, max_depth=1):
        counter = Counter()
        counter.update(self.get_categories(max_depth))

        return counter

    def get_distinct_categories(self, max_depth=1):
        return list(set(self.get_categories(max_depth)))

    def most_frequent_categories(self):
        pass

    def get_most_significant_categories(self, priors):
        pass
