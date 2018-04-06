from py2neo import Node, Relationship, authenticate, Graph

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'config')))
import config

def populate():
    host_port = '{}:{}'.format(config.get_setting('neo4j', 'host'),
                               config.get_setting('neo4j', 'port'))
    authenticate(host_port, config.get_setting('neo4j', 'user'),
                 config.get_setting('neo4j', 'pass'))
    graph = Graph('http://{}/db/data/'.format(host_port))

    try:
        graph.schema.create_uniqueness_constraint('Gene', 'id')
    except Exception as e:
        print e

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
