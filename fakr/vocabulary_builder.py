import csv
import argparse
from fakr import version, package_name as main_package_name
from collections import Mapping
import sys

package_name=main_package_name + '-builder'


def main():
    args=dict(
        delimiter=',',
        quotechar='"'
    )
    args.update(__parse_args())
    vocabulary_data=list()
    for fp in args['files']:
        partition=list()
        reader=csv.DictReader(fp, delimiter=args['delimiter'], quotechar=args['quotechar'])
        for l in reader:
            partition.append(l)
        vocabulary_data.append(partition)

    from . import vocabulary

    vocabulary.write(args['output'], vocabulary_data)
    args['output'].close()

def __parse_args() -> Mapping:
    parser = argparse.ArgumentParser(
        prog=package_name,
        description='''
            {} takes a list of csv files and creates a vocabulary
        '''.format(package_name)
    )

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(version)
                        )

    parser.add_argument(metavar='FILENAME',
                        dest='output',
                        type=argparse.FileType('wb'),
                        help='Filename for output',
                        )

    parser.add_argument('-t', '--tables',
                        metavar='FILENAME',
                        dest='files',
                        type=argparse.FileType('r'),
                        help='Name of a csv file',
                        nargs='+',
                        default=[]
                        )

    return vars(parser.parse_args())