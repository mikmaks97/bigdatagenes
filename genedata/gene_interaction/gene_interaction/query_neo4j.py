from py2neo import Node, Relationship, authenticate, Graph

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'config')))
import config

def query(n_id, order):
    if order <= 0: return None

    host_port = '{}:{}'.format(config.get_setting('neo4j', 'host'),
                               config.get_setting('neo4j', 'port'))
    authenticate(host_port, config.get_setting('neo4j', 'user'),
                 config.get_setting('neo4j', 'pass'))
    graph = Graph('http://{}/db/data/'.format(host_port))


    query_n_order = '''
    MATCH (g:Gene {{id: {}}})-[:INTERACTS*{}]->(n_order_gene) WHERE NOT((g)-[:INTERACTS]->(n_order_gene))
    RETURN g.id, n_order_gene.id
    '''.format(n_id, order) if order > 1 else '''
    MATCH (g:Gene {{id: {}}})-[:INTERACTS]->(n_order_gene)
    RETURN g.id, n_order_gene.id
    '''.format(n_id)
    return graph.data(query_n_order)


