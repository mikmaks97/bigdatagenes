from datetime import datetime

from py2neo import Node, Relationship, authenticate, Graph

from genedata.config import config

start = datetime.now()

host_port = '{}:{}'.format(config.get_setting('neo4j', 'host'),
                           config.get_setting('neo4j', 'port'))
authenticate(host_port, config.get_setting('neo4j', 'user'),
             config.get_setting('neo4j', 'pass'))
graph = Graph('http://{}/db/data/'.format(host_port))

try:
    graph.schema.create_uniqueness_constraint('Gene', 'id')
except Exception as e:
    print(e)

create_nodes = '''
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///PPI.csv" as ppirow
MERGE (ga:Gene {id: toInt(ppirow.interactor_A)})
MERGE (gb:Gene {id: toInt(ppirow.interactor_B)})
'''
graph.run(create_nodes)

create_relationships = '''
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///PPI.csv" AS ppirow
MATCH (ga:Gene {id: toInt(ppirow.interactor_A)})
MATCH (gb:Gene {id: toInt(ppirow.interactor_B)})
MERGE (ga)-[:INTERACTS]->(gb)
'''
graph.run(create_relationships)

print(datetime.now()-start)
