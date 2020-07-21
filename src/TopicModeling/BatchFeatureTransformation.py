import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer


def identity(words):
    return words


class BatchFeatureTransformation:
    def __init__(self, dictionaries_doc, labels, features, batch_size=100):
        self.batch_size = batch_size
        self.features = features

        self.labels = labels

        self.dictionaries_doc = []

        if type(dictionaries_doc) == dict:
            entities = dictionaries_doc["linkedEntities"]
            tokens = dictionaries_doc["tokens"]
            for e, t in zip(entities, tokens):
                self.dictionaries_doc.append(e + t)
        else:
            self.dictionaries_doc = dictionaries_doc

    def __iter__(self):
        X_data = []
        Y_data = []

        vectorizer = CountVectorizer(preprocessor=None, tokenizer=identity, lowercase=False)
        X = vectorizer.fit_transform(self.dictionaries_doc)
        
        yield (X.toarray(), np.asarray(self.labels))
        """
        for i, (entities, label) in enumerate(zip(self.dictionaries_doc, self.labels)):

            row = []
            counter_entities = Counter()
            counter_entities.update(entities)

            for entity in self.features:
                row.append(counter_entities[entity])

            X_data.append(row)
            Y_data.append(label)

            if i > 0 and i % self.batch_size == 0:
                np_x = np.asarray(X_data)
                np_y = np.asarray(Y_data)

                X_data = []
                Y_data = []
                yield (np_x, np_y)

        if len(X_data):
            yield (np.asarray(X_data), np.asarray(Y_data))
        """
