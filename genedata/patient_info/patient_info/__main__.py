import argparse
import sys
import pprint

import info

def main():
    parser = argparse.ArgumentParser(description='CLI for populating and querying patient info DB')
    parser.add_argument('operation', type=str, help='populate/query')
    parser.add_argument('-id', '--patient_id', dest='id', type=str, help='Patient to get info for (patient id)')

    args = parser.parse_args()
    if args.operation != 'populate' and args.operation != 'query':
        parser.print_usage(sys.stderr)
        raise ValueError('operation must be populate or query')
    if args.operation == 'query' and args.id == None:
        parser.print_usage(sys.stderr)
        raise ValueError('target must be specified for query operation')

    if args.operation == 'populate':
        info.populate()
    elif args.operation == 'query':
        result = info.query(args.id)
        if isinstance(result, str):
            print result
        else:
            print 'Info for patient {}:'.format(args.id)
            print '  age: {}'.format(result['age'])
            print '  gender: {}'.format(result['gender'])
            print '  education: {}'.format(result['education'])


if __name__ == '__main__':
    main()
