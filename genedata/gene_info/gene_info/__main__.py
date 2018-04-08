import argparse
import sys
import pprint
import xml.dom.minidom as mini_dom

import info

def main():
    parser = argparse.ArgumentParser(description='CLI for populating and querying for gene information')
    parser.add_argument('operation', type=str, help='populate/query')
    parser.add_argument('-id', '--entrez_id', dest='id', type=str, help='Gene to get info for (entrez id)')

    args = parser.parse_args()
    if args.operation != 'populate' and args.operation != 'query':
        parser.print_usage(sys.stderr)
        raise ValueError('operation must be populate or query')
    if args.operation == 'query' and args.id == None:
        parser.print_usage(sys.stderr)
        raise ValueError('target must be specified for query operation')

    if args.operation == 'populate':
        info.delete_tables()
        info.create_tables()
        info.insert_data()
    elif args.operation == 'query':
        result = info.query_gene(args.id)
        if isinstance(result, str):
            print result
        else:
            for row in result:
                xml = mini_dom.parseString(row[4])
                pretty_xml = xml.toprettyxml(indent="  ")
                print 'Info for gene {}:'.format(row[3])
                print '  entrez id: {}'.format(row[0])
                print '  gene symbol: {}'.format(row[1])
                print '  gene name: {}'.format(row[2])
                print '  uniprot id: {}'.format(row[3])
                print '  uniprot information: {}'.format(pretty_xml)

if __name__ == '__main__':
    main()
