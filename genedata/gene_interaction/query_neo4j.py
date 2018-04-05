from py2neo import Node, Relationship, authenticate, Graph
from ..config import config

host_port = '{}:{}'.format(config.get_setting('neo4j', 'host'),
                           config.get_setting('neo4j', 'port'))
authenticate(host_port, config.get_setting('neo4j', 'user'),
             config.get_setting('neo4j', 'pass'))
graph = Graph('http://{}/db/data/'.format(host_port))


query_n_order = '''
MATCH (g:Gene {id: 2})-[:INTERACTS*2]->(n_order_genes) WHERE NOT((g)-[:INTERACTS]->(n_order_genes))
RETURN g.id, n_order_genes.id
'''
print(graph.data(query_n_order))


