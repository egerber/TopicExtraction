import sqlite3
import os

MAX_DEPTH_CHAIN = 10
P_INSTANCE_OF = 31
P_SUBCLASS = 279

conn = None
entity_cache = {}
chain_cache = {}
name_cache = {}

DB_PATH = os.path.abspath('data/wikidb_filtered.db')


def init_database_connection(path=DB_PATH):
    global conn, DB_PATH
    clear_cache()

    conn = sqlite3.connect(path)


def print_linked_entities(doc):
    for e in doc._.linkedEntities:
        print(e.pretty_string())


def print_candidates(alias):
    global conn, entity_cache
    c = conn.cursor()
    query_alias = """SELECT i.item_id,i.en_label,i.views,i.en_description,a.en_alias from aliases as a
        LEFT JOIN joined as i ON a.item_id = i.item_id
        WHERE a.en_alias_lowercase = ? and i.item_id NOT NULL ORDER BY views DESC"""

    c.execute(query_alias, [alias.lower()])
    rows = c.fetchall()

    for row in rows:
        print("https://www.wikidata.org/wiki/Q{}  , {} , {} <{}>".format(row[0], row[1], row[2], row[3]))


def get_entities_from_alias(alias):
    global conn, entity_cache
    c = conn.cursor()
    if alias in entity_cache:
        return entity_cache[alias].copy()

    query_alias = """SELECT j.item_id,j.en_label, j.en_description,j.views,j.inlinks,a.en_alias from aliases as a
        LEFT JOIN joined as j ON a.item_id = j.item_id
        WHERE a.en_alias_lowercase = ? and j.item_id NOT NULL"""

    c.execute(query_alias, [alias.lower()])
    fetched_rows = c.fetchall()

    entity_cache[alias] = fetched_rows
    return fetched_rows


def clear_cache():
    global entity_cache, chain_cache, name_cache
    entity_cache.clear()
    chain_cache.clear()
    name_cache.clear()


def get_instances_of(item_id, properties=[P_INSTANCE_OF, P_SUBCLASS], count=1000):
    global conn, name_cache

    query = "SELECT source_item_id from statements where target_item_id={} and edge_property_id IN ({}) LIMIT {}".format(
        item_id, ",".join([str(prop) for prop in properties]), count)

    c = conn.cursor()
    c.execute(query)

    res = c.fetchall()

    return [e[0] for e in res]


def get_entity_name(item_id):
    global conn, name_cache

    if item_id in name_cache:
        return name_cache[item_id]

    c = conn.cursor()
    query = "SELECT en_label from joined WHERE item_id=?"
    c.execute(query, [item_id])
    res = c.fetchone()

    if res and len(res):
        if res[0] == None:
            name_cache[item_id] = 'no label'
        else:
            name_cache[item_id] = res[0]
    else:
        name_cache[item_id] = '<none>'

    return name_cache[item_id]


def get_entity(item_id):
    global conn, name_cache

    c = conn.cursor()
    query = "SELECT j.item_id,j.en_label,j.en_description,j.views,j.inlinks from joined as j " \
            "WHERE j.item_id=={}".format(item_id)

    res = c.execute(query)

    return res.fetchone()


def get_children(item_id, limit=100):
    global conn, name_cache

    c = conn.cursor()
    query = "SELECT j.item_id,j.en_label,j.en_description,j.views,j.inlinks from joined as j " \
            "JOIN statements as s on j.item_id=s.source_item_id " \
            "WHERE s.target_item_id={} and s.edge_property_id IN (279,31) LIMIT {}".format(item_id, limit)

    res = c.execute(query)

    return res.fetchall()


def get_parents(item_id, limit=100):
    global conn, name_cache

    c = conn.cursor()
    query = "SELECT j.item_id,j.en_label,j.en_description,j.views,j.inlinks from joined as j " \
            "JOIN statements as s on j.item_id=s.target_item_id " \
            "WHERE s.source_item_id={} and s.edge_property_id IN (279,31) LIMIT {}".format(item_id, limit)

    res = c.execute(query)

    return res.fetchall()


def get_categories(item_id, max_depth=10):
    chain = []
    edges = []
    append_chain_elements(item_id, 0, chain, edges, max_depth, [P_INSTANCE_OF, P_SUBCLASS])
    return [el[0] for el in chain]


def get_chain(item_id, max_depth=10, property=P_INSTANCE_OF):
    chain = []
    edges = []
    append_chain_elements(item_id, 0, chain, edges, max_depth, property)
    return chain


def get_recursive_edges(item_id):
    chain = []
    edges = []
    append_chain_elements(item_id, 0, chain, edges)
    return edges


def append_chain_elements(item_id, level=0, chain=[], edges=[], max_depth=10, property=P_INSTANCE_OF):
    global conn, chain_cache

    properties = property
    if type(property) != list:
        properties = [property]

    if (item_id, max_depth) in chain_cache:
        chain += chain_cache[(item_id, max_depth)].copy()
        return

    # prevent infinite recursion
    if level >= max_depth:
        return

    # if item_id in chain_cache:
    #    return chain_cache[item_id]
    c = conn.cursor()

    query = "SELECT target_item_id,edge_property_id from statements where source_item_id={} and edge_property_id IN ({})".format(
        item_id, ",".join([str(prop) for prop in properties]))

    # set value for current item in order to prevent infinite recursion
    chain_cache[(item_id, max_depth)] = []

    for target_item in c.execute(query):

        chain_ids = [el[0] for el in chain]

        if not (target_item[0] in chain_ids):
            chain += [(target_item[0], level + 1)]
            edges.append((item_id, target_item[0], target_item[1]))
            append_chain_elements(target_item[0], level=level + 1, chain=chain, edges=edges, max_depth=max_depth,
                                  property=property)

    chain_cache[(item_id, max_depth)] = chain


if __name__ == '__main__':
    init_database_connection()
    print(get_categories(13191, max_depth=1))
    print(get_categories(13191, max_depth=1))
    print(get_categories(13191, max_depth=2))
    print(get_categories(13191, max_depth=2))
    print(get_categories(13191, max_depth=1))
