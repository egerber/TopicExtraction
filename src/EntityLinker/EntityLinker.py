import spacy

from src.EntityLinker.EntityClassifier import EntityClassifier
from src.EntityLinker.EntityCollection import EntityCollection
from src.EntityLinker.TermCandidateExtractor import TermCandidateExtractor
from spacy.tokens import Doc, Span


class EntityLinker:

    def __init__(self):
        Doc.set_extension("linkedEntities", default=[], force=True)
        Span.set_extension("linkedEntities", default=[], force=True)

    def __call__(self, doc):
        tce = TermCandidateExtractor(doc)
        classifier = EntityClassifier()

        entities = []
        for termCandidates in tce:
            entityCandidates = termCandidates.get_entity_candidates()
            if len(entityCandidates) > 0:
                entity = classifier(entityCandidates)
                entity.span.sent._.linkedEntities.append(entity)
                entities.append(entity)

        doc._.linkedEntities = EntityCollection(entities)

        return doc


if __name__ == '__main__':
    nlp = spacy.load('en_core_web_md')
    entityLinker = EntityLinker()
    nlp.add_pipe(entityLinker, last=True)
    nlp.disable_pipes("ner")
    from src.EntityLinker.Utils import *

    init_database_connection('../../data/wikidb_filtered.db')
    nlp("This jupyter notebook is about knowledge graphs")._.linkedEntities.pretty_print()
