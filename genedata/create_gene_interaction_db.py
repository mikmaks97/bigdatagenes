from py2neo import Node, Relationship, Graph

graph = Graph(auth=())


tx = '''
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM “file:///PPI.csv” as ppirow
MERGE (ga:Gene {id: toInt(ppirow.interactor_A)})
MERGE (gb:Gene {id: toInt(ppirow.interactor_B)})
'''


