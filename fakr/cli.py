from collections import Mapping, Sequence
import argparse
import sys
import os
from .Jinja2Renderer import Jinja2Renderer
from .CompoundMappingSequence import CompoundMappingSequence
from .TemplatedMapping import templated_mapping
from .jinja import environment
import jinja2.exceptions
from . import version, package_name
from .Generator import Generator

ENV_FAKR_VOCABUALRY= 'FAKR_VOCABULARY'
ENV_FAKR_MIXIN= 'FAKR_MIXIN'


def main():
    j2env = environment()
    args = __parse_args()

    vocabulary_fps=[args['vocabulary']] + args['mixin']
    vocabulary = load_vocabulary(j2env, *vocabulary_fps)

    if args['list'] is True:
        print('\n'.join(sorted([v for v in list(vocabulary[0].keys()) + ['row']])))
        exit(0)

    if args['info'] is True:
        print('{} unique entries in\n{}'.format(len(vocabulary), '\n'.join(['\t- ' + os.path.realpath(fp.name) for fp in vocabulary_fps])))
        exit(0)

    try:
        generator = Generator(Jinja2Renderer(j2env, template_prefix=None), vocabulary, sys.stdin.read())
        for item in generator(args['count'], args['delay']):
            sys.stdout.write(item + '\n')
    except KeyboardInterrupt:
        exit(0)
    except jinja2.exceptions.TemplateError as e:
        sys.stderr.write('There was a problem with your templates: {}'.format(e.message))
    except OSError as e:
        sys.stderr.write(e.strerror)


def load_vocabulary(j2env, *fps) -> Sequence:
    from .vocabulary import read
    partitions=list()
    for fp in fps:
        partitions +=read(fp)

    mapping_factory=templated_mapping(Jinja2Renderer(j2env, template_prefix='%%'))
    return CompoundMappingSequence(mapping_factory, *partitions)


def __parse_args() -> Mapping:
    parser = argparse.ArgumentParser(
        prog=package_name,
        description='''
            {} reads a jinja2 template from STDIN or from a file, renders it with random values from the
            builtin us_top1000 vocabulary or from a custom file and writes the result to STDOUT
        '''.format(package_name)
    )

    meta_group=parser.add_argument_group('Information')

    meta_group.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(version)
                        )

    parser.add_argument('-c', '--count',
                        metavar='COUNT',
                        type=int,
                        default=-1,
                        help='Number of datasets to generate, defaults to 0 (unlimited)'
                        )

    parser.add_argument('-d', '--delay',
                        metavar='SECONDS',
                        type=float,
                        default=0,
                        help='Wait SECONDS between dataset generation, defaults to 0 (no waiting)'
                        )

    meta_group.add_argument('-l', '--list',
                        action='store_true',
                        help='show the available variables and exit'
                        )

    meta_group.add_argument('-i', '--info',
                        action='store_true',
                        help='show some vocabulary information and exit'
                        )

    parser.add_argument('-v', '--vocabulary',
                        metavar='FILENAME',
                        type=argparse.FileType('rb'),
                        help='Path to the vocabulary file. Defaults to the builtin us_top1000.fakr vocabulary. This setting overrides the vocabulary selection via the environment variable FAKR_VOCABULARY',
                        default=os.getenv(ENV_FAKR_VOCABUALRY, os.path.dirname(os.path.realpath(__file__)) + '/vocabularies/us_top1000.fakr'))

    parser.add_argument('-m', '--mixin',
                        metavar='FILENAME',
                        type=argparse.FileType('r'),
                        help='Additional vocabulary files to mix into the main vocabulary. This setting overrides the vocabulary selection via the environment variable FAKR_MIXIN',
                        nargs='*',
                        default=[open(v.strip(), 'r') for v in filter(None, os.getenv(ENV_FAKR_MIXIN, '').split(':'))]
                        )

    return vars(parser.parse_args())
