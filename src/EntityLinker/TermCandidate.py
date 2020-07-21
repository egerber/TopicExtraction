from src.EntityLinker.EntityCandidates import EntityCandidates
from src.EntityLinker.EntityElement import EntityElement
from src.EntityLinker.Utils import *


class TermCandidate:
    def __init__(self, span):
        self.variations = [span]

    def pretty_print(self):
        print("Term Candidates are [{}]".format(self))

    def append(self, span):
        self.variations.append(span)

    def has_plural(self, variation):
        return any([t.tag_ == "NNS" for t in variation])

    def get_singular(self, variation):
        return ' '.join([t.text if t.tag_ != "NNS" else t.lemma_ for t in variation])

    def __str__(self):
        return ', '.join([variation.text for variation in self.variations])

    def get_entity_candidates(self):

        entities_by_variation = {}
        for variation in self.variations:
            entities_by_variation[variation] = get_entities_from_alias(variation.text)
            if self.has_plural(variation):
                entities_by_variation[variation] += get_entities_from_alias(self.get_singular(variation))

        entity_elements = []
        for variation, entities in entities_by_variation.items():
            entity_elements += [EntityElement(entity, variation) for entity in entities]

        return EntityCandidates(entity_elements)
