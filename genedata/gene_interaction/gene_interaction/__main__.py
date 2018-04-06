import argparse
import sys
import pprint

import populate_neo4j, query_neo4j

def main():
    parser = argparse.ArgumentParser(description='CLI for populating and querying Neo4J DB')
    parser.add_argument('operation', type=str, help='populate/query')
    parser.add_argument('-t', '--target', dest='target', type=int, help='Gene to run query on (entrez id)')
    parser.add_argument('-o', '--order', dest='order', type=int, default=1, help='Order of interacting genes away from target')

    args = parser.parse_args()
    if args.operation != 'populate' and args.operation != 'query':
        parser.print_usage(sys.stderr)
        raise ValueError('operation must be populate or query')
    if args.operation == 'query' and args.target == None:
        parser.print_usage(sys.stderr)
        raise ValueError('target must be specified for query operation')

    if args.operation == 'populate':
        populate_neo4j.populate()
    elif args.operation == 'query':
        result = query_neo4j.query(args.target, args.order)
        msg = '{}-order interacting genes with gene {}:'.format(args.order, args.target)
        genes = []
        for d in result:
            genes.append(d['n_order_gene.id'])
        print msg, ', '.join(map(str,genes))


if __name__ == '__main__':
    main()
