import argparse
import sys

import stats

def main():
    parser = argparse.ArgumentParser(description='CLI for populating and querying gene mean/stdev DB')
    parser.add_argument('operation', type=str, help='populate/query')
    parser.add_argument('-g', '--gene', dest='gene', type=int, help='Gene to run query on (entrez id)')

    args = parser.parse_args()
    if args.operation != 'populate' and args.operation != 'query':
        parser.print_usage(sys.stderr)
        print 'Error: operation must be populate or query'
    if args.operation == 'query' and args.gene == None:
        parser.print_usage(sys.stderr)
        print 'Error: gene id must be specified for query operation'

    if args.operation == 'populate':
        stats.populate()
    elif args.operation == 'query':
        diagnoses = ['1 NCI, No cognitive impairment (No impaired domains)',
                     '2 MCI, Mild cognitive impairment (One impaired domain) and NO other cause of CI',
                     '3 MCI, Mild cognitive impairment (One impaired domain) AND another cause of CI',
                     "4 AD, Alzheimer's disease and NO other cause of CI (NINCDS PROB AD)",
                     "5 AD, Alzheimer's disease AND another cause of CI (NINCDS POSS AD)",
                     '6 Other dementia. Other primary cause of dementia']

        result = stats.query(args.gene)
        print 'Gene {} mean/stdev:'.format(args.gene)
        for i in xrange(len(result)):
            mean = result[i][0]
            stdev = result[i][1]
            print '{}, mean: {:.2f} stdev {:.2f}'.format(diagnoses[i], mean, stdev)


if __name__ == '__main__':
    main()
