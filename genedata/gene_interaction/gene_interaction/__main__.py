import argparse

import populate_neo4j, query_neo4j

def main():
    parser = argparse.ArgumentParser(description='CLI for populating and querying Neo4J DB')
    parser.add_argument('operation', type=str, help='create/query')
    parser.add_argument('--t', '--target', dest='target', help='Gene to run query on (entrez id/symbol/name')
    parser.add_argument('-o', '--order', dest='order', type=int, default=1, help='Order of interacting genes away from target')
    print(parser.parse_args())
